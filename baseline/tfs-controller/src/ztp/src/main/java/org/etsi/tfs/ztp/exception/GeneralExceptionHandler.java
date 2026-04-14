/*
* Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

package org.etsi.tfs.ztp.exception;

import io.grpc.Metadata;
import io.grpc.ServerCall;
import io.grpc.Status;
import io.grpc.StatusRuntimeException;
import io.quarkus.grpc.ExceptionHandlerProvider;
import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class GeneralExceptionHandler implements ExceptionHandlerProvider {
    @Override
    public <ReqT, RespT> io.quarkus.grpc.ExceptionHandler<ReqT, RespT> createHandler(
            ServerCall.Listener<ReqT> listener, ServerCall<ReqT, RespT> serverCall, Metadata metadata) {
        return new HelloExceptionHandler<>(listener, serverCall, metadata);
    }

    @Override
    public Throwable transform(Throwable t) {
        if (t instanceof ExternalServiceFailureException) {
            return new StatusRuntimeException(Status.INTERNAL.withDescription(t.getMessage()));
        } else {
            return ExceptionHandlerProvider.toStatusException(t, true);
        }
    }

    private static class HelloExceptionHandler<A, B> extends io.quarkus.grpc.ExceptionHandler<A, B> {
        public HelloExceptionHandler(
                ServerCall.Listener<A> listener, ServerCall<A, B> call, Metadata metadata) {
            super(listener, call, metadata);
        }

        @Override
        protected void handleException(Throwable t, ServerCall<A, B> call, Metadata metadata) {
            StatusRuntimeException sre =
                    (StatusRuntimeException) ExceptionHandlerProvider.toStatusException(t, true);
            Metadata trailers = sre.getTrailers() != null ? sre.getTrailers() : metadata;
            call.close(sre.getStatus(), trailers);
        }
    }
}
