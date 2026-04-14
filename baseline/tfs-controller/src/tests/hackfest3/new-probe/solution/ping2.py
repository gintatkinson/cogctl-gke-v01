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

socket_path = "/tmp/sock"
#socket_path = "./tmp/sock"

def main():
    hostname = sys.argv[1]
    count = 1
    wait = 5

    total_pings = 0
    successful_pings = 0
    try:
        while True:
            start_time = time.time()

            try:
                # Run the ping command and capture the output
                result = subprocess.check_output(["ping", "-W", str(wait), "-c", str(count), hostname], universal_newlines=True)

                response_time = float(re.findall(r"time=([0-9.]+) ms", result)[0])

            except subprocess.CalledProcessError as e:
                # If ping fails return negative response_time
                response_time = -1

            # Calculate new loss_ratio
            if response_time != -1:
                successful_pings += 1
            total_pings += 1
            moving_loss_ratio = round(((total_pings - successful_pings) / float(total_pings) * 100), 2)

            print("Total pings: {}".format(total_pings))
            print("Successful pings: {}".format(successful_pings))

            print("Packet loss: {}%".format(moving_loss_ratio))
            print("Latency: {} ms".format(response_time))

            data = str(response_time)

            # Write results in socket
            try:
                client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                client_socket.connect(socket_path)
                client_socket.send(data.encode())
                client_socket.close()
            except Exception as e:
                print(e)

            # Calculate the time taken by ping
            execution_time = time.time() - start_time
            # Wait the rest of the time
            wait_time = max(0, 6 - execution_time)
            time.sleep(wait_time)

    except KeyboardInterrupt:
        print("Script terminated.")

if __name__ == "__main__":
    main()

