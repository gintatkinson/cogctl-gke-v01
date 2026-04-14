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

-module(tfte_server).

-behaviour(gen_statem).


%%% INCLUDES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-include_lib("kernel/include/logger.hrl").


%%% EXPORTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% API functions
-export([start_link/0]).
-export([context_ready/1]).
-export([context_event/1]).
-export([topology_ready/1]).
-export([topology_event/1]).
-export([request_lsp/1]).
-export([delete_lsp/1]).

% Behaviour gen_statem functions
-export([init/1]).
-export([callback_mode/0]).
-export([handle_event/4]).
-export([terminate/3]).
-export([code_change/4]).


%%% Records %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-record(data, {
    services = #{}
}).


%%% MACROS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%% API FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

start_link() ->
    gen_statem:start_link({local, ?MODULE}, ?MODULE, [], []).

context_ready(Context) ->
    gen_statem:cast(?MODULE, {context_ready, Context}).

context_event(Event) ->
    gen_statem:cast(?MODULE, {context_event, Event}).

topology_ready(Topology) ->
    gen_statem:cast(?MODULE, {topology_ready, Topology}).

topology_event(Event) ->
    gen_statem:cast(?MODULE, {topology_event, Event}).

request_lsp(ServiceMap) ->
    gen_statem:call(?MODULE, {request_lsp, ServiceMap}).

delete_lsp(ServiceId) ->
    gen_statem:call(?MODULE, {delete_lsp, ServiceId}).


%%% BEHAVIOUR gen_statem FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

init([]) ->
    ?LOG_INFO("Starting server...", []),
    case tfte_context:is_ready() of
        false -> {ok, wait_context, #data{}};
        true -> {ok, ready, #data{}}
    end.

callback_mode() -> [handle_event_function, state_enter].

%-- WAIT_CONTEXT STATE ---------------------------------------------------------
handle_event(enter, _, wait_context, _Data) ->
    keep_state_and_data;
handle_event(cast, {context_ready, _Context}, wait_context, Data) ->
    ?LOG_DEBUG("Teraflow context initialized: ~p", [_Context]),
    tfte_topology:context_updated(),
    {next_state, ready, Data};
%-- READY STATE ----------------------------------------------------------------
handle_event(enter, _, ready, _Data) ->
    keep_state_and_data;
handle_event(cast, {context_ready, _Context}, ready, _Data) ->
    ?LOG_DEBUG("Teraflow context updated: ~p", [_Context]),
    tfte_topology:context_updated(),
    keep_state_and_data;
handle_event(cast, {context_event, _Event}, ready, _Data) ->
    ?LOG_DEBUG("Teraflow context event: ~p", [_Event]),
    keep_state_and_data;
handle_event(cast, {topology_ready, _Topology}, ready, _Data) ->
    ?LOG_DEBUG("Teraflow topology updated: ~p", [_Topology]),
    keep_state_and_data;
handle_event(cast, {topology_event, _Event}, ready, _Data) ->
    ?LOG_DEBUG("Teraflow topology event: ~p", [_Event]),
    keep_state_and_data;
handle_event({call, From}, {request_lsp, ServiceMap}, ready, Data) ->
    ?LOG_DEBUG("Teraflow service ~s requested its LSPs",
               [format_service_id(maps:get(service_id, ServiceMap, undefined))]),
    {Result, Data2} = do_request_lsp(Data, ServiceMap),
    {keep_state, Data2, [{reply, From, Result}]};
handle_event({call, From}, {delete_lsp, ServiceId}, ready, Data) ->
    ?LOG_DEBUG("Teraflow service ~s delete its LSPs",
              [format_service_id(ServiceId)]),
    {Result, Data2} = do_delete_lsp(Data, ServiceId),
    {keep_state, Data2, [{reply, From, Result}]};
%-- ANY STATE ------------------------------------------------------------------
handle_event(EventType, EventContent, State, _Data) ->
    ?LOG_WARNING("Unexpected tfte_server ~w event in state ~w: ~w",
                 [EventType, State, EventContent]),
    keep_state_and_data.

terminate(Reason, _State, _Data) ->
    ?LOG_INFO("Server terminated: ~p", [Reason]),
    ok.

code_change(_OldVsn, OldState, OldData, _Extra) ->
    {ok, OldState, OldData}.


%%% INTERNAL FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

format_service_id(undefined) -> <<"undefined">>;
format_service_id(#{context_id := #{context_uuid := #{uuid := ContextName}},
                    service_uuid := #{uuid := ServiceUUID}}) ->
    iolist_to_binary(io_lib:format("~s:~s", [ContextName, ServiceUUID])).

do_request_lsp(#data{services = Services} = Data,
               #{service_type := 'SERVICETYPE_TE'} = ServiceMap) ->
    try

    #{service_config := Config,
      service_endpoint_ids := Endpoints,
      service_id := ServiceId} = ServiceMap,
    #{<<"binding_label">> := BindingLabel1, <<"symbolic_name">> := SymbolicName1}
        = tfte_util:custom_config(Config, <<"/lsp-fw">>),
    #{<<"binding_label">> := BindingLabel2, <<"symbolic_name">> := SymbolicName2}
        = tfte_util:custom_config(Config, <<"/lsp-bw">>),
    [#{device_id := #{device_uuid := #{uuid := Id1}}},
     #{device_id := #{device_uuid := #{uuid := Id2}}}] = Endpoints,
    case epce_server:initiate_flow(SymbolicName1, Id1, Id2, BindingLabel1) of
        {error, Reason} ->
            ?LOG_ERROR("Error while setting up service ~s forward LSP: ~p",
                       [format_service_id(ServiceId), Reason]),
            {{error, Reason}, Data};
        {ok, ForwardFlow} ->
            case epce_server:initiate_flow(SymbolicName2, Id2, Id1, BindingLabel2) of
                {error, Reason} ->
                    ?LOG_ERROR("Error while setting up service ~s backward LSP: ~p",
                               [format_service_id(ServiceId), Reason]),
                    %TODO: Cleanup forward flow ?
                    {{error, Reason}, Data};
                {ok, BackwardFlow} ->
                    ServiceData = {ServiceMap, ForwardFlow, BackwardFlow},
                    Services2 = Services#{ServiceId => ServiceData},
                    Data2 = Data#data{services = Services2},
                    {{ok, 'SERVICESTATUS_ACTIVE'}, Data2}
            end
    end

    catch T:E:S ->
        ?LOG_ERROR("Error while requesintg LSP: ~p:~p", [T, E]),
        ?LOG_ERROR("Stacktrace: ~p", [S]),
        {{error, internal_error}, Data}
    end;
do_request_lsp(Data, ServiceMap) ->
    ?LOG_ERROR("Invalid arguments to RequestLSP call: ~p", [ServiceMap]),
    {{error, badarg}, Data}.

do_delete_lsp(Data, ServiceId) ->
    ?LOG_INFO("LSP DELETION REQUESTED ~p", [ServiceId]),
    {{error, not_implemented}, Data}.