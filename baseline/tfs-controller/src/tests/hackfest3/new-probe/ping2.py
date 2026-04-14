# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import socket, re, time, subprocess, sys

# Path of the socket inside mininet container
socket_path = "/tmp/sock"

def main():
    hostname = sys.argv[1]

    try:
        while True:
            start_time = time.time()

            try:
                # Run the ping command once and capture the output
                response_time = 0
            except subprocess.CalledProcessError as e:
                # If ping fails (even if it does not reach destination)
                # This part is executed 
                response_time = -1

            print("Latency: {} ms".format(response_time))

            # Uncomment the following when ready to write to socket
            #data = str(response_time)
            #
            # Write results in socket
            #try:
            #    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            #    client_socket.connect(socket_path)
            #    client_socket.send(data.encode())
            #    client_socket.close()
            #except Exception as e:
            #    print(e)

            # The following is to make sure that we ping at least
            # every 6 seconds regardless of how much time ping took.
            # Calculate the time taken by ping
            execution_time = time.time() - start_time
            # Wait the rest of the time
            wait_time = max(0, 6 - execution_time)
            time.sleep(wait_time)

    except KeyboardInterrupt:
        print("Script terminated.")

if __name__ == "__main__":
    main()

