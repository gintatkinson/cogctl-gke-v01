%%%-----------------------------------------------------------------------------
%% Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
%%
%% Licensed under the Apache License, Version 2.0 (the "License");
%% you may not use this file except in compliance with the License.
%% You may obtain a copy of the License at
%%
%%      http://www.apache.org/licenses/LICENSE-2.0
%%
%% Unless required by applicable law or agreed to in writing, software
%% distributed under the License is distributed on an "AS IS" BASIS,
%% WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
%% See the License for the specific language governing permissions and
%% limitations under the License.
%%%-----------------------------------------------------------------------------

-module(tfte_topology).

-behaviour(gen_statem).


%%% INCLUDES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-include_lib("kernel/include/logger.hrl").


%%% EXPORTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% API functions
-export([start_link/0]).
-export([context_updated/0]).

% Behaviour gen_statem functions
-export([init/1]).
-export([callback_mode/0]).
-export([handle_event/4]).
-export([terminate/3]).
-export([code_change/4]).


%%% Records %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-record(data, {
    uuid :: map(),
    sub :: term() | undefined,
    obj :: map() | undefined,
    devices = #{} :: map(),
    links = #{} :: map(),
    names = #{} :: map()
}).


%%% MACROS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-define(SUBSCRIBE_RETRY_TIMEOUT, 1000).
-define(RETRIEVE_RETRY_TIMEOUT, 10000).


%%% API FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

start_link() ->
    gen_statem:start_link({local, ?MODULE}, ?MODULE, [], []).

context_updated() ->
    gen_statem:cast(?MODULE, context_updated).


%%% BEHAVIOUR gen_statem FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

init([]) ->
    {ok, ContextName} = application:get_env(tfte, context),
    {ok, TopoName} = application:get_env(tfte, topology),
    ContextUUID = #{context_uuid => #{uuid => ContextName}},
    TopoUUID = #{context_id => ContextUUID,
                 topology_uuid => #{uuid => TopoName}},
    ?LOG_INFO("Starting topology ~s service handler...", [TopoName]),
    {ok, retrieve, #data{uuid = TopoUUID}}.

callback_mode() -> [handle_event_function, state_enter].

%-- RETRIEVE STATE -------------------------------------------------------------
handle_event(enter, _, retrieve, _Data) ->
    {keep_state_and_data, [{state_timeout, 0, do_retrieve}]};
handle_event(state_timeout, do_retrieve, retrieve, #data{uuid = UUID} = Data) ->
    ?LOG_DEBUG("Retrieving topology ~p...", [UUID]),
    case get_object(UUID) of
        error ->
            {keep_state_and_data, [{state_timeout, ?RETRIEVE_RETRY_TIMEOUT, do_retrieve}]};
        {ok, #{device_ids := Devices, link_ids := Links } = Topology} ->
            case {length(Devices), length(Links)} of
                {D, L} when D =:= 0; L =:= 0 ->
                    ?LOG_WARNING("Got topology, but there is missing devices or links", []),
                    {keep_state_and_data, [{state_timeout, 1000, do_retrieve}]};
                _ ->
                    ?LOG_DEBUG("Got topology: ~p", [Topology]),
                    {next_state, subscribe, Data#data{obj = Topology}}
            end
    end;
handle_event(cast, context_updated, retrieve, _Data) ->
    {keep_state_and_data, [{state_timeout, 0, do_retrieve}]};
%-- SUBSCRIBE STATE ------------------------------------------------------------
handle_event(enter, _, subscribe, #data{sub = undefined}) ->
    {keep_state_and_data, [{state_timeout, 0, do_suscribe}]};
handle_event(enter, _, subscribe, Data) ->
    % We already have a topology subscription
    {next_state, ready, Data};
handle_event(state_timeout, do_suscribe, subscribe, #data{uuid = UUID} = Data) ->
    ?LOG_DEBUG("Subscribing to topology events...", []),
    case do_subscribe(UUID) of
        {ok, Sub} ->
            ?LOG_INFO("Subscribed to topology events", []),
            Data2 = #data{obj = Obj} = Data#data{sub = Sub},
            #{device_ids := DeviceIds, link_ids := LinkIds} = Obj,
            case update_topology(Data2, DeviceIds, LinkIds) of
                {ok, Data3} ->
                    tfte_server:topology_ready(Obj),
                    {next_state, ready, Data3};
                {error, Reason} ->
                    ?LOG_ERROR("Failed to load topology: ~p", [Reason]),
                    statem_rollback_to_retrieve(Data2)
            end;
        {error, Reason} ->
            ?LOG_ERROR("Failed to subscribe to topology service events: ~p", [Reason]),
            {next_state, retrieve, [{state_timeout, ?SUBSCRIBE_RETRY_TIMEOUT, do_retrieve}]}
    end;
%-- READY STATE ----------------------------------------------------------------
handle_event(enter, _, ready, _Data) ->
    keep_state_and_data;
handle_event(info, {headers, Id, Value}, ready,
             #data{sub = #{stream_id := Id}}) ->
    %TODO: Handle HTTP errors ???
    ?LOG_DEBUG("Received topology stream header: ~p", [Value]),
    keep_state_and_data;
handle_event(info, {data, Id, #{event := Event}}, ready,
             #data{sub = #{stream_id := Id}} = Data) ->
    ?LOG_DEBUG("Received topology event: ~p", [Event]),
    handle_topology_event(Data, Event);
handle_event(info, {'DOWN', Ref, process, Pid, Reason}, ready,
             #data{sub = #{stream_id := Id, monitor_ref := Ref, stream_pid := Pid}} = Data) ->
    ?LOG_DEBUG("Topology subscription is down: ~p", [Reason]),
    Data2 = Data#data{sub = undefined},
    Info = receive
        {trailers, Id, {Status, Message, Metadata}} ->
            {Reason, Status, Message, Metadata}
    after 0 ->
        Reason
    end,
    ?LOG_ERROR("Topology subscription error: ~p", [Info]),
    {next_state, retrieve, Data2};
handle_event(cast, context_updated, ready, _Data) ->
    keep_state_and_data;
%-- ANY STATE ------------------------------------------------------------------
handle_event(info, Msg, StateName, _Data) ->
    ?LOG_WARNING("Unexpected topology message in state ~w: ~p", [StateName, Msg]),
    keep_state_and_data.

terminate(Reason, _State, _Data) ->
    ?LOG_INFO("Topology service handler terminated: ~p", [Reason]),
    ok.

code_change(_OldVsn, OldState, OldData, _Extra) ->
    {ok, OldState, OldData}.


%%% INTERNAL FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

statem_rollback_to_retrieve(#data{sub = undefined} = Data) ->
    {next_state, retrieve, Data, [{state_timeout, ?RETRIEVE_RETRY_TIMEOUT, do_retrieve}]};
statem_rollback_to_retrieve(#data{sub = Sub} = Data) ->
    grpcbox_client:close_send_and_recv(Sub),
    Data2 = Data#data{sub = undefined},
    {next_state, retrieve, Data2, [{state_timeout, ?RETRIEVE_RETRY_TIMEOUT, do_retrieve}]}.

handle_topology_event(#data{uuid = UUID} = Data,
                      #{event_type := 'EVENTTYPE_UPDATE'} = Event) ->
    case get_object(UUID) of
        error ->
            statem_rollback_to_retrieve(Data);
        {ok, #{device_ids := DeviceIds, link_ids := LinkIds} = Topology} ->
            ?LOG_DEBUG("Got new topology: ~p", [Topology]),
            Data2 = Data#data{obj = Topology},
            case update_topology(Data2, DeviceIds, LinkIds) of
                {ok, Data3} ->
                    tfte_server:topology_event(Event),
                    {keep_state, Data3};
                {error, Reason} ->
                    ?LOG_ERROR("Failed to update topology: ~p", [Reason]),
                    statem_rollback_to_retrieve(Data2)
            end
    end;
handle_topology_event(_Data, Event) ->
    tfte_server:topology_event(Event),
    keep_state_and_data.

update_topology(Data, DeviceIds, LinkIds) ->
    try
        {Data2, Events} = update_devices(Data, DeviceIds, []),
        {Data3, Events2} = update_links(Data2, LinkIds, Events),
        post_topology_events(lists:reverse(Events2)),
        {ok, Data3}
    catch
        throw:Reason ->
            {error, Reason}
    end.

post_topology_events(Events) ->
    lists:foreach(fun post_topology_event/1, Events).

post_topology_event({device_added, Id, Device}) ->
    epce_ted:device_added(Id, Device);
post_topology_event({device_updated, Id, Device}) ->
    epce_ted:device_updated(Id, Device);
post_topology_event({device_deleted, Id}) ->
    epce_ted:device_deleted(Id);
post_topology_event({link_added, Id, Link}) ->
    epce_ted:link_added(Id, Link);
post_topology_event({link_updated, Id, Link}) ->
    epce_ted:link_updated(Id, Link);
post_topology_event({link_deleted, Id}) ->
    epce_ted:link_deleted(Id).

update_devices(#data{devices = OldDevices} = Data, DeviceIds, Events) ->
    update_devices(Data, OldDevices, #{}, DeviceIds, Events).

update_devices(Data, OldDevices, NewDevices, [], Events) ->
    #data{names = Names} = Data,
    Events2 = [{device_deleted, maps:get(I, Names, undefined)}
               || I <- maps:keys(OldDevices)] ++ Events,
    {Data#data{devices = NewDevices}, Events2};
update_devices(Data, OldDevices, NewDevices, [GivenId | Rest], Events) ->
    case get_device(GivenId) of
        error -> throw({device_retrieval_error, GivenId});
        {ok, Device} ->
            Device2 = #{id := Id, real_id := RealId} = post_process_device(Device),
            #data{names = Names} = Data,
            Data2 = Data#data{names = Names#{RealId => Id}},
            NewDevices2 = NewDevices#{Id => Device},
            case maps:take(Id, OldDevices) of
                error ->
                    % New device
                    Events2 = [{device_added, Id, Device2} | Events],
                    update_devices(Data2, OldDevices, NewDevices2, Rest, Events2);
                {Device, OldDevices2} ->
                    % Device did not change
                    update_devices(Data2, OldDevices2, NewDevices2, Rest, Events);
                {_OldDevice, OldDevices2} ->
                    % Device changed
                    Events2 = [{device_updated, Id, Device2} | Events],
                    update_devices(Data2, OldDevices2, NewDevices2, Rest, Events2)
            end
    end.

update_links(#data{links = OldLinks} = Data, LinksIds, Events) ->
    update_links(Data, OldLinks, #{}, LinksIds, Events).

update_links(Data, OldLinks, NewLinks, [], Events) ->
    Events2 = [{link_deleted, post_process_link_id(I)}
               || I <- maps:keys(OldLinks)] ++ Events,
    {Data#data{links = NewLinks}, Events2};
update_links(Data, OldLinks, NewLinks, [Id | Rest], Events) ->
    case get_link(Id) of
        error -> throw({link_retrieval_error, Id});
        {ok, Link} ->
            Id2 = post_process_link_id(Id),
            Link2 = post_process_link(Data, Link),
            NewLinks2 = NewLinks#{Id => Link},
            case maps:take(Id, OldLinks) of
                error ->
                    % New Link
                    Events2 = [{link_added, Id2, Link2} | Events],
                    update_links(Data, OldLinks, NewLinks2, Rest, Events2);
                {Link, OldLinks2} ->
                    % Link did not change
                    update_links(Data, OldLinks2, NewLinks2, Rest, Events);
                {_OldLink, OldLinks2} ->
                    % Link changed
                    Events2 = [{link_updated, Id2, Link2} | Events],
                    update_links(Data, OldLinks2, NewLinks2, Rest, Events2)
            end
    end.

post_process_device(#{device_id := Id, name :=  Name} = Device) ->
    #{id => Name,
      real_id => Id,
      type => device_type(Device),
      pcc_address => device_pcc_address(Device),
      mpls_label => device_mpls_label(Device),
      status => device_status(Device),
      endpoints => device_endpoints(Device)}.

device_type(#{device_type := Type}) ->
    Type.

device_status(#{device_operational_status := 'DEVICEOPERATIONALSTATUS_UNDEFINED'}) ->
    undefined;
device_status(#{device_operational_status := 'DEVICEOPERATIONALSTATUS_DISABLED'}) ->
    disabled;
device_status(#{device_operational_status := 'DEVICEOPERATIONALSTATUS_ENABLED'}) ->
    enabled.

device_mpls_label(Device) ->
    try device_config_value(<<"/te_data">>, Device) of
        Map when is_map(Map) -> maps:get(<<"mpls_label">>, Map, undefined);
        _ -> undefined
    catch error:badarg -> undefined
    end.

device_pcc_address(Device) ->
    try device_config_value(<<"/te_data">>, Device) of
        Map when is_map(Map) ->
            case maps:get(<<"pcc_address">>, Map, undefined) of
                AddressBin ->
                    case inet_parse:address(binary_to_list(AddressBin)) of
                        {ok, Address} -> Address;
                        {error,einval} -> undefined
                    end
            end;
        _ -> undefined
    catch
        error:badarg -> undefined
    end.

device_config_value(Key, #{device_config := Config}) ->
    tfte_util:custom_config(Config, Key).

device_endpoints(Device) ->
    device_endpoints(Device, []).

device_endpoints(#{device_endpoints := Endpoints}, Acc) ->
    device_endpoints(Endpoints, Acc);
device_endpoints([], Acc) ->
    lists:reverse(Acc);
device_endpoints([#{name := Name} | Rest], Acc) ->
    device_endpoints(Rest, [Name | Acc]).

post_process_link_id(#{link_uuid := #{uuid := Name}}) ->
    Name.

post_process_link(Data, Link) ->
    #{id => link_id(Link),
      endpoints => link_endpoints(Data, Link)}.

link_id(#{link_id := Id}) ->
    post_process_link_id(Id).

link_endpoints(Data, Link) ->
    link_endpoints(Data, Link, []).

link_endpoints(Data, #{link_endpoint_ids := Endpoints}, Acc) ->
    link_endpoints(Data, Endpoints, Acc);
link_endpoints(_Data, [], Acc) ->
    lists:reverse(Acc);
link_endpoints(Data, [#{device_id := RealId,
                        endpoint_uuid := #{uuid := EndpointName}} | Rest], Acc) ->
    #data{names = Names} = Data,
    Endpoint = #{
        device => maps:get(RealId, Names, undefined),
        endpoint => EndpointName
    },
    link_endpoints(Data, Rest, [Endpoint | Acc]).


%-- GRPC UNTILITY FUNCTION -----------------------------------------------------

grpc_opts() ->
    #{channel => context}.

do_subscribe(UUID) ->
    context_context_service_client:get_topology_events(UUID, grpc_opts()).

get_object(UUID) ->
    case context_context_service_client:get_topology(UUID, grpc_opts()) of
        {error, Reason} -> 
            ?LOG_ERROR("Local error while retrieving the topology object: ~p", [Reason]),
            error;
        {error, Reason, _Headers} ->
            ?LOG_ERROR("Remote error while retrieving the topology object: ~p", [Reason]),
            error;
        {ok, Result, _Headers} ->
            {ok, Result}
    end.

get_device(UUID) ->
    case context_context_service_client:get_device(UUID, grpc_opts()) of
        {error, Reason} -> 
            ?LOG_ERROR("Local error while retrieving a device object: ~p", [Reason]),
            error;
        {error, Reason, _Headers} ->
            ?LOG_ERROR("Remote error while retrieving a device object: ~p", [Reason]),
            error;
        {ok, Result, _Headers} ->
            {ok, Result}
    end.

get_link(UUID) ->
    case context_context_service_client:get_link(UUID, grpc_opts()) of
        {error, Reason} -> 
            ?LOG_ERROR("Local error while retrieving a link object: ~p", [Reason]),
            error;
        {error, Reason, _Headers} ->
            ?LOG_ERROR("Remote error while retrieving a link object: ~p", [Reason]),
            error;
        {ok, Result, _Headers} ->
            {ok, Result}
    end.
