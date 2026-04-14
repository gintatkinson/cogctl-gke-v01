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
%% @doc tfte public API
%% @end
%%%-----------------------------------------------------------------------------

-module(tfte_app).

-behaviour(application).


%%% INCLUDES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-include_lib("kernel/include/logger.hrl").


%%% EXPORTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Behaviour application callback functions
-export([start/2, stop/1]).


%%% BEHAVIOUR applicaation CALLBACK FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

start(_StartType, _StartArgs) ->
    case tfte_sup:start_link() of
        {ok, Pid} ->
            add_services(),
            {ok, Pid};
        Other ->
            Other
    end.

stop(_State) ->
    ok.


%%% INTERNAL FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

add_services() ->
    case application:get_env(tfte, services) of
        {ok, Services} -> add_services(Services);
        _ -> ok
    end.

add_services([]) -> ok;
add_services([{Name, EndpointsSpecs, GrpcOpts} | Rest]) ->
    try resolve_endpoints(Name, EndpointsSpecs, []) of
        Endpoints ->
            case grpcbox_channel_sup:start_child(Name, Endpoints, GrpcOpts) of
                {ok, _Pid} ->
                    ?LOG_INFO("GRPC channel to ~s service started", [Name]),
                    ok;
                {error, Reason} ->
                    ?LOG_WARNING("GRPC channel to ~s service failed to start: ~p",
                                 [Name, Reason]),
                    ok
            end
    catch
        throw:{Name, Reason, Extra} ->
            ?LOG_WARNING("Failed to resolve ~s service configuration: ~s ~p",
                         [Name, Reason, Extra])
    end,
    add_services(Rest).

resolve_endpoints(_Name, [], Acc) ->
    lists:reverse(Acc);
resolve_endpoints(Name, [{Transport, HostSpec, PortSpec, SslOpts} | Rest], Acc) ->
    Acc2 = [{Transport, resolve_host_spec(Name, HostSpec),
             resolve_port_spec(Name, PortSpec), SslOpts} | Acc],
    resolve_endpoints(Name, Rest, Acc2).

resolve_host_spec(_Name, Hostname) when is_list(Hostname) -> Hostname;
resolve_host_spec(Name, {env, Key}) when is_list(Key) ->
    try os:getenv(Key) of
        false -> throw({Name, service_hostname_not_found, Key});
        Hostname -> Hostname
    catch
        _:Reason ->
            throw({Name, service_hostname_error, Reason})
    end.

resolve_port_spec(_Name, Port) when is_integer(Port) -> Port;
resolve_port_spec(Name, {env, Key}) when is_list(Key) ->
    try os:getenv(Key) of
        false -> throw({Name, service_port_not_found, Key});
        PortStr ->
            try list_to_integer(PortStr) of
                Port -> Port
            catch
                _:Reason ->
                    throw({Name, service_port_error, Reason})
            end
    catch
        _:Reason ->
            throw({Name, service_port_error, Reason})
    end.
