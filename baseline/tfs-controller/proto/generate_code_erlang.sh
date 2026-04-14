#!/bin/bash -eu
# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e

FORCE=0
DEFAULT_ACTION="generate"

usage() {
    echo "Usage: $0 [-f] [clean|generate]" 1>&2
    echo "Options:"
    echo "  -f: Force regeneration of all protocol buffers"
    exit 1;
}

while getopts "fc" o; do
    case "${o}" in
        f)
            FORCE=1
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

ACTION=${1:-$DEFAULT_ACTION}
cd $(dirname $0)
ROOT=$(pwd)
ERLANG_PROTO_DIR="$ROOT/src/erlang"
BUILD_CHECK="$ERLANG_PROTO_DIR/.generated"

tfpb_clean() {
    rm -f "$BUILD_CHECK"
    rm -rf "$ERLANG_PROTO_DIR/src/"*.erl
    rm -rf "$ERLANG_PROTO_DIR/src/erlang/_build"
}

tfpb_generate() {
    if [[ -f "$BUILD_CHECK" && $FORCE != 1 ]]; then
        echo "Protocol buffer code for Erlang already generated, use -f to force"
        exit 0
    fi

    tfpb_clean
    mkdir -p "$ERLANG_PROTO_DIR"
    cd "$ERLANG_PROTO_DIR"
    rebar3 compile
    rebar3 grpc gen
    rebar3 compile
    touch "$BUILD_CHECK"

    echo "Protocol buffer code for Erlang generated"
}

case "$ACTION" in
    clean) tfpb_clean;;
    generate) tfpb_generate;;
    *) usage;;
esac

