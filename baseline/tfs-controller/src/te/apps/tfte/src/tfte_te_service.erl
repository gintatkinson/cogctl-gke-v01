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

-module(tfte_te_service).

-behaviour(te_te_service_bhvr).


%%% INCLUDES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-include_lib("grpcbox/include/grpcbox.hrl").
-include_lib("kernel/include/logger.hrl").


%%% EXPORTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Behaviour te_te_service_bhvr callback functions
-export([request_lsp/2]).
-export([update_lsp/2]).
-export([delete_lsp/2]).


%%% BEHAVIOUR te_te_service_bhvr CALLBACK FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%

request_lsp(Ctx, Service) ->
    ?LOG_INFO("Requesting LSP: ~p", [Service]),
    try tfte_server:request_lsp(Service) of
        {ok, Status} ->
            {ok, #{service_status => Status}, Ctx};
        {error, Reason} ->
            ?LOG_INFO("Error while requesting LSP: ~p", [Reason]),
            {ok, #{service_status => 'SERVICESTATUS_UNDEFINED'}, Ctx}
    catch E:R:S ->
        ?LOG_ERROR("Error while requesting LSP: ~p:~p ~p", [E, R, S]),
        {ok, #{service_status => 'SERVICESTATUS_UNDEFINED'}, Ctx}
    end.

update_lsp(_Ctx, _ServiceId) ->
    {error, {?GRPC_STATUS_UNIMPLEMENTED, <<"Not yet implemented">>},
             #{headers => #{}, trailers => #{}}}.

delete_lsp(Ctx, ServiceId) ->
    ?LOG_ERROR("Deleting LSP: ~p", [ServiceId]),
    try tfte_server:delete_lsp(ServiceId) of
        {ok, Status} ->
            {ok, Status, Ctx};
        {error, Reason} ->
            ?LOG_INFO("Error while deleting LSP: ~p", [Reason]),
            {ok, #{service_status => 'SERVICESTATUS_UNDEFINED'}, Ctx}
    catch E:R:S ->
        ?LOG_ERROR("Error while deleting LSP: ~p:~p ~p", [E, R, S]),
        {ok, #{service_status => 'SERVICESTATUS_UNDEFINED'}, Ctx}
    end.
