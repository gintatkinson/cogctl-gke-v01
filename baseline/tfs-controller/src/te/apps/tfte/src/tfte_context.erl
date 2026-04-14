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

-module(tfte_context).

-behaviour(gen_statem).


%%% INCLUDES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-include_lib("kernel/include/logger.hrl").


%%% EXPORTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% API functions
-export([start_link/0]).
-export([is_ready/0]).

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
    obj :: map() | undefined
}).


%%% MACROS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-define(SUBSCRIBE_RETRY_TIMEOUT, 1000).
-define(RETRIEVE_RETRY_TIMEOUT, 10000).


%%% API FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

start_link() ->
    gen_statem:start_link({local, ?MODULE}, ?MODULE, [], []).

is_ready() ->
    case whereis(?MODULE) of
        undefined -> false;
        _ -> gen_statem:call(?MODULE, is_ready)
    end.


%%% BEHAVIOUR gen_statem FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

init([]) ->
    {ok, Name} = application:get_env(tfte, context),
    ?LOG_INFO("Starting context ~s service handler...", [Name]),
    UUID = #{context_uuid => #{uuid => Name}},
    {ok, subscribe, #data{uuid = UUID}}.

callback_mode() -> [handle_event_function, state_enter].

%-- SUBSCRIBE STATE ------------------------------------------------------------
handle_event(enter, _, subscribe, #data{sub = undefined}) ->
    {keep_state_and_data, [{state_timeout, 0, do_suscribe}]};
handle_event(enter, _, subscribe, Data) ->
    % We already have a context subscription
    {next_state, ready, Data};
handle_event(state_timeout, do_suscribe, subscribe, Data) ->
    ?LOG_DEBUG("Subscribing to context events...", []),
    case do_subscribe() of
        {ok, Sub} ->
            ?LOG_INFO("Subscribed to context events", []),
            Data2 = Data#data{sub = Sub},
            {next_state, retrieve, Data2};
        {error, Reason} ->
            ?LOG_ERROR("Failed to subscribe to context service events: ~p", [Reason]),
            {keep_state_and_data, [{state_timeout, ?SUBSCRIBE_RETRY_TIMEOUT, do_suscribe}]}
    end;
%-- RETRIEVE STATE -------------------------------------------------------------
handle_event(enter, _, retrieve, _Data) ->
    {keep_state_and_data, [{state_timeout, 0, do_retrieve}]};
handle_event(state_timeout, do_retrieve, retrieve, #data{uuid = UUID} = Data) ->
    ?LOG_DEBUG("Retrieving context ~p...", [UUID]),
    case get_object(UUID) of
        error ->
            {keep_state_and_data, [{state_timeout, ?RETRIEVE_RETRY_TIMEOUT, do_retrieve}]};
        {ok, Context} ->
            ?LOG_DEBUG("Got context: ~p", [Context]),
            tfte_server:context_ready(Context),
            {next_state, ready, Data#data{obj = Context}}
    end;
handle_event(info, {headers, Id, Value}, retrieve,
             #data{sub = #{stream_id := Id}}) ->
    %TODO: Handle HTTP errors ???
    ?LOG_DEBUG("Received context stream header: ~p", [Value]),
    keep_state_and_data;
handle_event(info, {data, Id, Value}, retrieve,
             #data{sub = #{stream_id := Id}}) ->
    ?LOG_DEBUG("Received context event, retrying context: ~p", [Value]),
    {keep_state_and_data, [{state_timeout, 0, do_retrieve}]};
handle_event(info, {'DOWN', Ref, process, Pid, Reason}, retrieve,
             #data{sub = #{stream_id := Id, monitor_ref := Ref, stream_pid := Pid}} = Data) ->
    ?LOG_DEBUG("Context subscription is down: ~p", [Reason]),
    Data2 = Data#data{sub = undefined},
    Info = receive
        {trailers, Id, {Status, Message, Metadata}} ->
            {Reason, Status, Message, Metadata}
    after 0 ->
        Reason
    end,
    ?LOG_ERROR("Context subscription error: ~p", [Info]),
    {next_state, subscribe, Data2};
%-- READY STATE ----------------------------------------------------------------
handle_event(enter, _, ready, _Data) ->
    keep_state_and_data;
handle_event(info, {headers, Id, Value}, ready,
             #data{sub = #{stream_id := Id}}) ->
    %TODO: Handle HTTP errors ???
    ?LOG_DEBUG("Received context stream header: ~p", [Value]),
    keep_state_and_data;
handle_event(info, {data, Id, #{context_id := UUID, event := Event}}, ready,
             #data{uuid = UUID, sub = #{stream_id := Id}}) ->
    ?LOG_DEBUG("Received context event: ~p", [Event]),
    tfte_server:context_event(Event),
    keep_state_and_data;
handle_event(info, {'DOWN', Ref, process, Pid, Reason}, ready,
             #data{sub = #{stream_id := Id, monitor_ref := Ref, stream_pid := Pid}} = Data) ->
    ?LOG_DEBUG("Context subscription is down: ~p", [Reason]),
    Data2 = Data#data{sub = undefined},
    Info = receive
        {trailers, Id, {Status, Message, Metadata}} ->
            {Reason, Status, Message, Metadata}
    after 0 ->
        Reason
    end,
    ?LOG_ERROR("Context subscription error: ~p", [Info]),
    {next_state, subscribe, Data2};
%-- ANY STATE ------------------------------------------------------------------
handle_event({call, _From}, is_ready, State, _Data) ->
    {keep_state_and_data, [{reply, State =:= ready}]};
handle_event(info, Msg, StateName, _Data) ->
    ?LOG_WARNING("Unexpected context message in state ~w: ~p", [StateName, Msg]),
    keep_state_and_data.

terminate(Reason, _State, _Data) ->
    ?LOG_INFO("Context service handler terminated: ~p", [Reason]),
    ok.

code_change(_OldVsn, OldState, OldData, _Extra) ->
    {ok, OldState, OldData}.


%%% INTERNAL FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

grpc_opts() ->
    #{channel => context}.

do_subscribe() ->
    context_context_service_client:get_context_events(#{}, grpc_opts()).

get_object(UUID) ->
    case context_context_service_client:get_context(UUID, grpc_opts()) of
        {error, Reason} -> 
            ?LOG_ERROR("Local error while retrieving the context object: ~p", [Reason]),
            error;
        {error, Reason, _Headers} ->
            ?LOG_ERROR("Remote error while retrieving the context object: ~p", [Reason]),
            error;
        {ok, Result, _Headers} ->
            {ok, Result}
    end.