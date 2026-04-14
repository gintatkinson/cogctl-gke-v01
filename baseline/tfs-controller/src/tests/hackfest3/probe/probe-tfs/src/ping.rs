/**
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
 *
 * Program that starts the ping probe and reports it to the Unix socket.
 *
 * Author: Carlos Natalino <carlos.natalino@chalmers.se>
 */
// standard library
use std::io;
use std::path::Path;

// external libraries
use tokio::net::UnixStream;
use tokio::time::{sleep, Duration};

async fn send_value(path: &Path, value: i32) -> Result<(), Box<dyn std::error::Error>> {
    let stream = UnixStream::connect(path).await?;
    stream.writable().await;
    // if ready.is_writable() {
    match stream.try_write(&i32::to_be_bytes(value)) {
        Ok(n) => {
            println!("\twrite {} bytes\t{}", n, value);
        }
        Err(ref e) if e.kind() == io::ErrorKind::WouldBlock => {
            println!("Error would block!");
        }
        Err(e) => {
            println!("error into()");
            return Err(e.into());
        }
    }
    // }
    Ok(())
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let path = Path::new("/tmp/tfsping");

    loop {
        let payload = [0; 1024];

        let result = surge_ping::ping("10.0.0.2".parse()?, &payload).await;

        // let (_packet, duration) = result.unwra

        if let Ok((_packet, duration)) = result {
            println!("Ping took {:.3?}\t{:?}", duration, _packet.get_identifier());
            send_value(&path, duration.as_micros() as i32).await?;
        } else {
            println!("Error!");
            send_value(&path, -1).await?;
        }

        sleep(Duration::from_secs(2)).await;
    }

    // Ok(())  // unreachable
}
