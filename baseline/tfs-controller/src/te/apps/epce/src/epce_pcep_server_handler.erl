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

-module(epce_pcep_server_handler).

-behaviour(gen_pcep_handler).


%%% INCLUDES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-include_lib("kernel/include/logger.hrl").
-include_lib("pcep_codec/include/pcep_codec_te.hrl").


%%% EXPORTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% API functions

% Behaviour gen_pcep_handler functions
-export([init/1]).
-export([opened/4]).
-export([flow_added/2]).
-export([flow_initiated/2]).
-export([ready/1]).
-export([request_route/2]).
-export([flow_delegated/2]).
-export([flow_status_changed/3]).
-export([terminate/2]).


%%% RECORDS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-record(state, {}).


%%% API FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%% BEHAVIOUR gen_pcep_handler FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

init([]) ->
    {ok, #{}, #state{}}.

opened(Id, Caps, Sess, State) ->
    case epce_server:session_opened(Id, Caps, Sess) of
        ok -> {ok, State};
        {error, Reason} -> {error, Reason}
    end.

flow_added(Flow, State) ->
    case epce_server:flow_added(Flow) of
        {error, _Reason} = Error -> Error;
        ok -> {ok, State}
    end.

flow_initiated(Flow, State) ->
    ok = epce_server:flow_initiated(Flow),
    {ok, State}.

ready(State) ->
    {ok, State}.

request_route(RouteReq, State) ->
    case epce_server:request_route(RouteReq) of
        {error, _Reason} = Error -> Error;
        {ok, Route} -> {ok, Route, State}
    end.

flow_delegated(_Flow, State) ->
    {ok, State}.

flow_status_changed(FlowId, NewStatus, State) ->
    epce_server:flow_status_changed(FlowId, NewStatus),
    {ok, State}.

terminate(_Reason, _State) ->
    ok.
