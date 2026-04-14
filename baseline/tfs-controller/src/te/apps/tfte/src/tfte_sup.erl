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
%%
%% @doc tfte top level supervisor.
%% @end
%%%-----------------------------------------------------------------------------

-module(tfte_sup).

-behaviour(supervisor).


%%% EXPORTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% API Functions
-export([start_link/0]).

% Behaviour supervisor callback functions
-export([init/1]).


%%% MACROS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-define(SERVER, ?MODULE).
-define(ROOT_SERVER, tfte_server).


%%% API FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

start_link() ->
    supervisor:start_link({local, ?SERVER}, ?MODULE, []).


%%% BEHAVIOUR supervisor CALLBACK FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

init([]) ->
    SupFlags = #{strategy => one_for_all,
                 intensity => 0,
                 period => 1},
    ServiceSupSpec = #{
        id => service_sup,
        start => {tfte_service_sup, start_link, []},
        restart => permanent,
        type => supervisor,
        shutdown => brutal_kill
    },
    ServerSpec = #{
        id => ?ROOT_SERVER,
        start => {?ROOT_SERVER, start_link, []},
        restart => permanent,
        shutdown => brutal_kill
    },
    ChildSpecs = [ServerSpec, ServiceSupSpec],
    {ok, {SupFlags, ChildSpecs}}.
