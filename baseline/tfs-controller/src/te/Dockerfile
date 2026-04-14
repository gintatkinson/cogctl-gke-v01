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

# Multi-stage Docker image build

# Build stage 0
FROM erlang:24.3-alpine

RUN apk add --no-cache bash git

RUN mkdir /var/teraflow
WORKDIR /var/teraflow

COPY proto proto
RUN bash -c proto/generate_code_erlang.sh
RUN mkdir src
COPY src/te src/te
WORKDIR src/te
RUN rebar3 as prod release

# Build stage 1
FROM alpine

# Install some libs
RUN apk add --no-cache libgcc libstdc++ && \
    apk add --no-cache openssl && \
    apk add --no-cache libcrypto1.1 && \
    apk add --no-cache ncurses-libs

# Install the released application
COPY --from=0 /var/teraflow/src/te/_build/prod/rel/tfte /tfte

# Expose relevant ports
EXPOSE 10030
EXPOSE 4189

ARG ERLANG_LOGGER_LEVEL_DEFAULT=debug
ARG ERLANG_COOKIE_DEFAULT=tfte-unsafe-cookie
ARG ERLANG_NODE_IP_DEFAULT=127.0.0.1
ARG ERLANG_NODE_NAME_DEFAULT=tfte

ENV ERLANG_LOGGER_LEVEL=$ERLANG_LOGGER_LEVEL_DEFAULT
ENV ERLANG_COOKIE=$ERLANG_COOKIE_DEFAULT
ENV ERLANG_NODE_IP=$ERLANG_NODE_IP_DEFAULT
ENV ERLANG_NODE_NAME=$ERLANG_NODE_NAME_DEFAULT

ENTRYPOINT ["/tfte/bin/tfte"]
CMD ["foreground"]
