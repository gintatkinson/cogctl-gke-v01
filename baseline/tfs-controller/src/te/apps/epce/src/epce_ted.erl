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

-module(epce_ted).

-behaviour(gen_server).


%%% INCLUDES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-include_lib("kernel/include/logger.hrl").


%%% EXPORTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% API Functions
-export([start_link/0]).
-export([device_added/2]).
-export([device_updated/2]).
-export([device_deleted/1]).
-export([link_added/2]).
-export([link_updated/2]).
-export([link_deleted/1]).
-export([compute_path/3]).
-export([lookup/2]).

-export([get_graph/0]).

% Behaviour gen_server functions
-export([init/1]).
-export([handle_call/3]).
-export([handle_cast/2]).
-export([handle_continue/2]).
-export([handle_info/2]).
-export([code_change/3]).
-export([terminate/2]).


%%% RECORDS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-record(state, {
    graph :: diagraph:graph(),
    pcc_address_to_id = #{} :: map()
}).


%%% API FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

device_added(Id, Device) ->
    gen_server:call(?MODULE, {device_added, Id, Device}).

device_updated(Id, Device) ->
    gen_server:call(?MODULE, {device_updated, Id, Device}).

device_deleted(Id) ->
    gen_server:call(?MODULE, {device_deleted, Id}).

link_added(Id, Link) ->
    gen_server:call(?MODULE, {link_added, Id, Link}).

link_updated(Id, Link) ->
    gen_server:call(?MODULE, {link_updated, Id, Link}).

link_deleted(Id) ->
    gen_server:call(?MODULE, {link_deleted, Id}).

compute_path(Index, From, To)
  when Index =:= id; Index =:= pcc_address ->
    gen_server:call(?MODULE, {compute_path, Index, From, To});
compute_path(Index, _From, _To) ->
    {error, {invalid_index, Index}}.

lookup(Index, Key)
  when Index =:= id; Index =:= pcc_address ->
    gen_server:call(?MODULE, {lookup, Index, Key});
lookup(Index, _Key) ->
    {error, {invalid_index, Index}}.


get_graph() ->
    gen_server:call(?MODULE, get_graph).


%%% BEHAVIOUR gen_server FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

init([]) ->
    ?LOG_INFO("Starting TED process...", []),
    % {ok, #state{graph = digraph:new([private, cyclic])}}.
    {ok, #state{graph = digraph:new([protected, cyclic])}}.

handle_call({device_added, Id, Device}, _From, State) ->
    ?LOG_DEBUG("Adding TED device ~p: ~p", [Id, Device]),
    {reply, ok, do_update_device(State, Id, Device)};
handle_call({device_updated, Id, Device}, _From, State) ->
    ?LOG_DEBUG("Updating TED device ~p: ~p", [Id, Device]),
    {reply, ok, do_update_device(State, Id, Device)};
handle_call({device_deleted, Id}, _From, State) ->
    ?LOG_DEBUG("Deleting TED device ~p", [Id]),
    {reply, ok, do_delete_device(State, Id)};
handle_call({link_added, Id, Link}, _From, State) ->
    ?LOG_DEBUG("Adding TED link ~p: ~p", [Id, Link]),
    {reply, ok, do_update_link(State, Id, Link)};
handle_call({link_updated, Id, Link}, _From, State) ->
    ?LOG_DEBUG("Updating TED link ~p: ~p", [Id, Link]),
    {reply, ok, do_update_link(State, Id, Link)};
handle_call({link_deleted, Id}, _From, State) ->
    ?LOG_DEBUG("Deleting TED link ~p", [Id]),
    {reply, ok, do_delete_link(State, Id)};
handle_call({compute_path, Index, From, To}, _From, #state{graph = G} = State) ->
    case as_ids(State, Index, [From, To]) of
        {ok, [FromId, ToId]} ->
            {reply, do_compute_path(G, FromId, ToId), State};
        {error, Reason} ->
            {reply, {error, Reason}, State}
    end;
handle_call({lookup, Index, Key}, _From, #state{graph = G} = State) ->
    case as_ids(State, Index, [Key]) of
        {ok, [Id]} ->
            {reply, do_lookup(G, Id), State};
        {error, Reason} ->
            {reply, {error, Reason}, State}
    end;
handle_call(get_graph, _From, #state{graph = G} = State) ->
    {reply, G, State};
handle_call(Request, _From, State) ->
    logger:warning("Unexpected call to TED process ~w", [Request]),
    {reply, {error, unexpected_call}, State}.

handle_cast(Request, State) ->
    logger:warning("Unexpected cast to TED process ~w", [Request]),
    {noreply, State}.

handle_continue(_Continue, State) ->
    {noreply, State}.

handle_info(Info, State) ->
    logger:warning("Unexpected message to TED process ~w", [Info]),
    {noreply, State}.

code_change(_OldVsn, State, _Extra) ->
    {ok, State}.

terminate(_Reason, _State) ->
    ?LOG_INFO("Terminating TED process...", []),
    ok.


%%% INTERNAL FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

as_ids(_State, id, Keys) ->
    {ok, Keys};
as_ids(State, IndexType, Keys) ->
    as_ids(State, IndexType, Keys, []).

as_ids(_State, _IndexType, [], Acc) ->
    {ok, lists:reverse(Acc)};
as_ids(#state{pcc_address_to_id = Index} = State, pcc_address, [Key | Rest], Acc) ->
    case maps:find(Key, Index) of
        error -> {error, {unknown_key, Key}};
        {ok, Id} -> as_ids(State, pcc_address, Rest, [Id | Acc])
    end.

do_update_device(#state{graph = G} = State, Id, NewDevice) ->
    State2 = case digraph:vertex(G, Id) of
        false -> State;
        {Id, OldDevice} -> index_remove_device(State, OldDevice)
    end,
    digraph:add_vertex(G, Id, NewDevice),
    index_add_device(State2, NewDevice).

do_delete_device(#state{graph = G} = State, Id) ->
    case digraph:vertex(G, Id) of
        false -> State;
        {Id, OldDevice} ->
            digraph:del_vertex(G, Id),
            index_remove_device(State, OldDevice)
    end.

index_remove_device(#state{pcc_address_to_id = Index} = State,
                    #{pcc_address := OldAddress}) ->
    Index2 = maps:remove(OldAddress, Index),
    State#state{pcc_address_to_id = Index2}.

index_add_device(State, #{pcc_address := undefined}) ->
    State;
index_add_device(#state{pcc_address_to_id = Index} = State,
                 #{id := Id, pcc_address := NewAddress}) ->
    Index2 = Index#{NewAddress => Id},
    State#state{pcc_address_to_id = Index2}.

do_update_link(#state{graph = G} = State, Id, Link) ->
    #{endpoints := [EP1, EP2]} = Link,
    #{device := D1} = EP1,
    #{device := D2} = EP2,
    digraph:add_edge(G, {Id, a}, D1, D2, Link),
    digraph:add_edge(G, {Id, b}, D2, D1, Link),
    State.

do_delete_link(#state{graph = G} = State, Id) ->
    digraph:del_edge(G, {Id, a}),
    digraph:del_edge(G, {Id, b}),
    State.

do_compute_path(G, FromId, ToId) ->
    case digraph:get_short_path(G, FromId, ToId) of
        false -> {error, not_found};
        Ids -> {ok, retrieve_devices(G, Ids, [])}
    end.

do_lookup(G, Id) ->
    case digraph:vertex(G, Id) of
        {_, Info} -> {ok, Info};
        false -> {error, not_found}
    end.

retrieve_devices(_G, [], Acc) ->
    lists:reverse(Acc);
retrieve_devices(G, [Id | Rest], Acc) ->
    case digraph:vertex(G, Id) of
        false -> {error, invalid_path};
        {Id, Device} ->
            retrieve_devices(G, Rest, [Device | Acc])
    end.
