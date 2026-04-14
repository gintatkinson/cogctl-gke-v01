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

-module(epce_server).

-behaviour(gen_server).


%%% INCLUDES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-include_lib("kernel/include/logger.hrl").
-include_lib("pcep_server/include/pcep_server.hrl").


%%% EXPORTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% API Functions
-export([start_link/0]).
-export([get_flows/0]).
-export([update_flow/2]).
-export([initiate_flow/4]).

% Handler Functions
-export([session_opened/3]).
-export([flow_added/1]).
-export([flow_initiated/1]).
-export([request_route/1]).
-export([flow_status_changed/2]).

% Behaviour gen_server functions
-export([init/1]).
-export([handle_call/3]).
-export([handle_cast/2]).
-export([handle_continue/2]).
-export([handle_info/2]).
-export([code_change/3]).
-export([terminate/2]).


%%% MACROS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-define(LARGE_TIMEOUT, infinity).


%%% RECORDS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-record(sess, {
        id,
        caps,
        monref,
        pid
}).

-record(state, {
        bouncer,
        sessions = #{},
        sess_pids = #{},
        flows = #{}
}).


%%% API FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

get_flows() ->
    gen_server:call(?MODULE, get_flows).

update_flow(FlowId, LabelStack) ->
    gen_server:call(?MODULE, {update_flow, FlowId, LabelStack}).

initiate_flow(Name, From, To, BindingLabel) ->
    gen_server:call(?MODULE, {initiate_flow, Name, From, To,
                              BindingLabel}, ?LARGE_TIMEOUT).


%%% HANDLER FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

session_opened(Id, Caps, Pid) ->
    gen_server:call(?MODULE, {session_opened, Id, Caps, Pid}).

flow_added(Flow) ->
    gen_server:call(?MODULE, {flow_added, Flow}).

flow_initiated(Flow) ->
    gen_server:call(?MODULE, {flow_initiated, Flow}).

request_route(RouteReq) ->
    gen_server:call(?MODULE, {request_route, RouteReq}).

flow_status_changed(FlowId, NewStatus) ->
    gen_server:call(?MODULE, {flow_status_changed, FlowId, NewStatus}).


%%% BEHAVIOUR gen_server FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

init([]) ->
    {ok, bouncer_start(#state{})}.

handle_call(get_flows, _From, #state{flows = Flows} = State) ->
    {reply, {ok, Flows}, State};
handle_call({update_flow, FlowId, Labels}, From,
            #state{flows = Flows, sessions = SessMap} = State) ->
    case maps:find(FlowId, Flows) of
        error -> {reply, {error, flow_not_found}, State};
        {ok, #{owner := Owner, route := #{} = R}} ->
            case maps:find(Owner, SessMap) of
                error -> {reply, {error, session_not_found}, State};
                {ok, #sess{pid = Pid}} ->
                    #{source := S, destination := D, constraints := C} = R,
                    ReqRoute = routereq_from_labels(S, D, C, Labels),
                    session_update_flow(State, Pid, FlowId, ReqRoute, From),
                    {noreply, State}
            end
    end;
handle_call({initiate_flow, Name, FromKey, ToKey, Binding}, From,
            #state{sessions = SessMap} = State) ->
    case {pcc_address(FromKey), pcc_address(ToKey)} of
        {{error, Reason}, _} ->
            {reply, {error, Reason}, State};
        {_, {error, Reason}} ->
            {reply, {error, Reason}, State};
        {{ok, FromAddr}, {ok, ToAddr}} ->
            case maps:find(FromAddr, SessMap) of
                error -> {reply, {error, session_not_found}, State};
                {ok, #sess{pid = Pid}} ->
                    case compute_path(FromAddr, ToAddr) of
                        {error, Reason} ->
                            {reply, {error, Reason}, State};
                        {ok, Labels} ->
                            InitRoute = routeinit_from_labels(Name, FromAddr,
                                            ToAddr, [], Binding, Labels),
                            session_initiate_flow(State, Pid, InitRoute, From),
                            {noreply, State}
                    end
            end
    end;
handle_call({session_opened, Id, Caps, Pid}, _From,
            #state{sessions = SessMap, sess_pids = SessPids} = State) ->
    logger:debug("Session with capabilities ~w open to ~w", [Caps, Id]),
    case maps:find(Id, SessMap) of
        {ok, _} -> {reply, {error, already_opened}, State};
        error ->
            MonRef = erlang:monitor(process, Pid),
            SessRec = #sess{id = Id, caps = Caps, monref = MonRef, pid = Pid},
            {reply, ok, State#state{
                sessions = SessMap#{Id => SessRec},
                sess_pids = SessPids#{Pid => SessRec}
            }}
    end;
handle_call({flow_added, #{id := Id, route := Route} = Flow},
            _From, #state{flows = Flows} = State) ->
    logger:debug("Flow ~w with route ~w added", [Id, route_to_labels(Route)]),
    {reply, ok, State#state{flows = Flows#{Id => Flow}}};
handle_call({flow_initiated, #{id := Id, route := Route} = Flow},
            _From, #state{flows = Flows} = State) ->
    logger:debug("Flow ~w with route ~p initiated",
                 [Id, route_to_labels(Route)]),
    {reply, ok, State#state{flows = Flows#{Id => Flow}}};
handle_call({request_route, RouteReq}, _From, State) ->
    logger:info("Route from ~w to ~w requested",
                [maps:get(source, RouteReq), maps:get(destination, RouteReq)]),
    #{source := S, destination := D, constraints := C} = RouteReq,
    case compute_path(S, D) of
        {error, _Reason} = Error ->
            {reply, Error, State};
        {ok, Labels} ->
            Route = routereq_from_labels(S, D, C, Labels),
            {reply, {ok, Route}, State}
    end;
handle_call({flow_status_changed, FlowId, NewStatus}, _From,
            #state{flows = Flows} = State) ->
    logger:info("Flow ~w status changed to ~w", [FlowId, NewStatus]),
    Flow = maps:get(FlowId, Flows),
    {reply, ok, State#state{
        flows = maps:put(FlowId, Flow#{status := NewStatus}, Flows)}};
handle_call(Request, From, State) ->
    logger:warning("Unexpected call from ~w: ~p", [From, Request]),
    {reply, {error, unexpected_call}, State}.


handle_cast(Request, State) ->
    logger:warning("Unexpected cast: ~p", [Request]),
    {noreply, State}.

handle_continue(_Continue, State) ->
    {noreply, State}.

handle_info({flow_updated, FlowId, NewRoute, From},
            #state{flows = Flows} = State) ->
    logger:info("Flow ~w updated to ~w", [FlowId, route_to_labels(NewRoute)]),
    case maps:find(FlowId, Flows) of
        error -> {noreply, State};
        {ok, Flow} ->
            Flows2 = Flows#{FlowId => Flow#{route => NewRoute}},
            gen_server:reply(From, ok),
            {noreply, State#state{flows = Flows2}}
    end;
handle_info({flow_update_error, FlowId, Reason, From}, State) ->
    logger:error("Flow ~w updated error: ~p", [FlowId, Reason]),
    gen_server:reply(From, {error, Reason}),
    {noreply, State};
handle_info({flow_initiated, #{id := FlowId, route := Route} = Flow, From},
            #state{flows = Flows} = State) ->
    logger:info("Flow ~w initiated to ~p",
                [FlowId, route_to_labels(Route)]),
    gen_server:reply(From, {ok, FlowId}),
    {noreply, State#state{flows = Flows#{FlowId => Flow}}};
handle_info({flow_init_error, Reason, From}, State) ->
    logger:error("Flow initialisation error: ~p", [Reason]),
    gen_server:reply(From, {error, Reason}),
    {noreply, State};
handle_info({'DOWN', MonRef, process, Pid, _Reason},
            #state{sessions = SessMap, sess_pids = PidMap} = State) ->
    case maps:take(Pid, PidMap) of
        {#sess{id = Id, monref = MonRef}, PidMap2} ->
            SessMap2 = maps:remove(Id, SessMap),
            %TODO: Do something about the flows from this session ?
            {noreply, State#state{
                sessions = SessMap2,
                sess_pids = PidMap2
            }};
        _X ->
            {noreply, State}
    end;
handle_info(Info, State) ->
    logger:warning("Unexpected message: ~p", [Info]),
    {noreply, State}.

code_change(_OldVsn, State, _Extra) ->
    {ok, State}.

terminate(_Reason, _State) ->
    ok.


%%% INTERNAL FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

ted_index(Id) when is_binary(Id) -> id;
ted_index({_, _, _, _}) -> pcc_address.

pcc_address(Key) ->
    case epce_ted:lookup(ted_index(Key), Key) of
        {error, Reason} ->
            logger:warning("Failed to find a PCC address for router ~p: ~p",
                           [Key, Reason]),
            {error, router_not_found};
        {ok, #{pcc_address := Addr}} ->
            {ok, Addr}
    end.

compute_path(From, To) when is_binary(From), is_binary(To) ->
    compute_path_result(From, To, epce_ted:compute_path(id, From, To));
compute_path({_, _, _, _} = From, {_, _, _, _} = To) ->
    compute_path_result(From, To, epce_ted:compute_path(pcc_address, From, To)).

compute_path_result(From, To, {error, Reason}) ->
    logger:warning("Failed to find a route from ~p to ~p: ~p",
                   [From, To, Reason]),
    {error, route_not_found};
compute_path_result(From, To, {ok, Devices}) ->
    Labels = tl([L || #{mpls_label := L} <- Devices, L =/= undefined]),
    logger:debug("Route from ~p to ~p: ~p", [From, To, Labels]),
    {ok, Labels}.

routereq_from_labels(Source, Destination, Constraints, Labels) ->
    #{
        source => Source,
        destination => Destination,
        constraints => Constraints,
        steps => [
            #{
                is_loose => false,
                nai_type => absent,
                sid => #mpls_stack_entry{label = L}
            }
          || L <- Labels
        ]
    }.

routeinit_from_labels(Name, Source, Destination, Constraints, Binding, Labels) ->
    Route = routereq_from_labels(Source, Destination, Constraints, Labels),
    Route#{
        name => Name,
        binding_label => Binding
    }.

route_to_labels(#{steps := Steps}) ->
    [Sid#mpls_stack_entry.label || #{sid := Sid} <- Steps].


%-- Session Interface Functions ------------------------------------------------

session_update_flow(#state{bouncer = Pid}, SessPid, FlowId, Route, Args) ->
    Pid ! {update_flow, SessPid, FlowId, Route, Args}.

session_initiate_flow(#state{bouncer = Pid}, SessPid, Route, Args) ->
    Pid ! {initiate_flow, SessPid, Route, Args}.

bouncer_start(#state{bouncer = undefined} = State) ->
    Self = self(),
    Pid = erlang:spawn_link(fun() ->
        bouncer_bootstrap(Self)
    end),
    receive bouncer_ready -> ok end,
    State#state{bouncer = Pid}.

bouncer_bootstrap(Parent) ->
    Parent ! bouncer_ready,
    bouncer_loop(Parent).

bouncer_loop(Parent) ->
    receive
        {update_flow, SessPid, FlowId, ReqRoute, Args} ->
            case pcep_server_session:update_flow(SessPid, FlowId, ReqRoute) of
                {ok, NewRoute} ->
                    Parent ! {flow_updated, FlowId, NewRoute, Args},
                    bouncer_loop(Parent);
                {error, Reason} ->
                    Parent ! {flow_update_error, FlowId, Reason, Args},
                    bouncer_loop(Parent)
            end;
        {initiate_flow, SessPid, InitRoute, Args} ->
            case pcep_server_session:initiate_flow(SessPid, InitRoute) of
                {ok, Flow} ->
                    Parent ! {flow_initiated, Flow, Args},
                    bouncer_loop(Parent);
                {error, Reason} ->
                    Parent ! {flow_init_error, Reason, Args},
                    bouncer_loop(Parent)
            end
    end.
