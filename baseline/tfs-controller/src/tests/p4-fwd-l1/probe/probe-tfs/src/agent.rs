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

/************** Modules needed to communicate with TeraFlowSDN ***************/
pub mod kpi_sample_types {
    tonic::include_proto!("kpi_sample_types");
}

pub mod acl {
    tonic::include_proto!("acl");
}

pub mod context {
    // tonic::include_proto!();
    tonic::include_proto!("context");
}

pub mod monitoring {
    tonic::include_proto!("monitoring");
}

/********************************** Imports **********************************/
// standard library
use std::env;
use std::path::Path;
use std::sync::Arc;
use std::time::SystemTime;
use std::{fs, io};

// external libraries
use dotenv::dotenv;
use futures;
use futures::lock::Mutex;
use tokio::net::UnixListener;

// proto
use context::context_service_client::ContextServiceClient;
use context::{Empty, Timestamp};
use kpi_sample_types::KpiSampleType;
use monitoring::monitoring_service_client::MonitoringServiceClient;
use monitoring::{Kpi, KpiDescriptor, KpiValue};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    dotenv().ok(); // load the environment variables from the .env file

    let path = Path::new("/tmp/tfsping");

    if path.exists() {
        fs::remove_file(path)?; // removes the socket in case it exists
    }

    let listener = UnixListener::bind(path).unwrap();
    println!("Bound to the path {:?}", path);

    // ARC Mutex that tells whether or not to send the results to the monitoring component
    let send_ping = Arc::new(Mutex::new(false));
    // copy used by the task that receives data from the probe
    let ping_probe = send_ping.clone();
    // copy used by the task that receives stream data from TFS
    let ping_trigger = send_ping.clone();

    // ARC mutex that hosts the KPI ID to be used as the monitoring KPI
    let kpi_id: Arc<Mutex<Option<monitoring::KpiId>>> = Arc::new(Mutex::new(None));
    let kpi_id_probe = kpi_id.clone();
    let kpi_id_trigger = kpi_id.clone();

    let t1 = tokio::spawn(async move {
        let monitoring_host = env::var("MONITORINGSERVICE_SERVICE_HOST")
            .unwrap_or_else(|_| panic!("receiver: Could not find monitoring host!"));
        let monitoring_port = env::var("MONITORINGSERVICE_SERVICE_PORT_GRPC")
            .unwrap_or_else(|_| panic!("receiver: Could not find monitoring port!"));

        let mut monitoring_client = MonitoringServiceClient::connect(format!(
            "http://{}:{}",
            monitoring_host, monitoring_port
        ))
        .await
        .unwrap();
        println!("receiver: Connected to the monitoring service!");
        loop {
            println!("receiver: Awaiting for new connection!");
            let (stream, _socket) = listener.accept().await.unwrap();

            stream.readable().await.unwrap();

            let mut buf = [0; 4];

            match stream.try_read(&mut buf) {
                Ok(n) => {
                    let num = u32::from_be_bytes(buf);
                    println!("receiver: read {} bytes -- {:?}", n, num);

                    let should_ping = ping_probe.lock().await;

                    if *should_ping {
                        // only send the value to monitoring if needed
                        // send the value to the monitoring component
                        println!("receiver: Send value to monitoring");

                        let kpi_id = kpi_id_probe.lock().await;
                        println!("receiver: kpi id: {:?}", kpi_id);

                        let now = SystemTime::now()
                            .duration_since(SystemTime::UNIX_EPOCH)
                            .unwrap()
                            .as_secs(); // See struct std::time::Duration methods

                        let kpi = Kpi {
                            kpi_id: kpi_id.clone(),
                            timestamp: Some(Timestamp {
                                timestamp: now as f64,
                            }),
                            kpi_value: Some(KpiValue {
                                value: Some(monitoring::kpi_value::Value::Int32Val(num as i32)),
                            }),
                        };
                        // println!("Request: {:?}", kpi);
                        let response = monitoring_client
                            .include_kpi(tonic::Request::new(kpi))
                            .await;
                        // println!("Response: {:?}", response);
                        if response.is_err() {
                            println!("receiver: Issue with the response from monitoring!");
                        }
                    }
                }
                Err(ref e) if e.kind() == io::ErrorKind::WouldBlock => {
                    continue;
                }
                Err(e) => {
                    println!("receiver: {:?}", e);
                }
            }
        }
    });

    let t2 = tokio::spawn(async move {
        // let server_address = "129.16.37.136";
        let context_host = env::var("CONTEXTSERVICE_SERVICE_HOST")
            .unwrap_or_else(|_| panic!("stream: Could not find context host!"));
        let context_port = env::var("CONTEXTSERVICE_SERVICE_PORT_GRPC")
            .unwrap_or_else(|_| panic!("stream: Could not find context port!"));

        let monitoring_host = env::var("MONITORINGSERVICE_SERVICE_HOST")
            .unwrap_or_else(|_| panic!("stream: Could not find monitoring host!"));
        let monitoring_port = env::var("MONITORINGSERVICE_SERVICE_PORT_GRPC")
            .unwrap_or_else(|_| panic!("stream: Could not find monitoring port!"));

        let mut context_client =
            ContextServiceClient::connect(format!("http://{}:{}", context_host, context_port))
                .await
                .unwrap();
        println!("stream: Connected to the context service!");

        let mut monitoring_client = MonitoringServiceClient::connect(format!(
            "http://{}:{}",
            monitoring_host, monitoring_port
        ))
        .await
        .unwrap();
        println!("stream: Connected to the monitoring service!");

        let mut service_event_stream = context_client
            .get_service_events(tonic::Request::new(Empty {}))
            .await
            .unwrap()
            .into_inner();
        while let Some(event) = service_event_stream.message().await.unwrap() {
            let event_service = event.clone().service_id.unwrap();
            if event.event.clone().unwrap().event_type == 1 {
                println!("stream: New CREATE event:\n{:?}", event_service);

                let kpi_descriptor = KpiDescriptor {
                    kpi_id: None,
                    kpi_id_list: vec![],
                    device_id: None,
                    endpoint_id: None,
                    slice_id: None,
                    connection_id: None,
                    link_id: None,
                    kpi_description: format!(
                        "Latency value for service {}",
                        event_service.service_uuid.unwrap().uuid
                    ),
                    service_id: Some(event.clone().service_id.clone().unwrap().clone()),
                    kpi_sample_type: KpiSampleType::KpisampletypeUnknown.into(),
                };

                let _response = monitoring_client
                    .set_kpi(tonic::Request::new(kpi_descriptor))
                    .await
                    .unwrap()
                    .into_inner();
                let mut kpi_id = kpi_id_trigger.lock().await;
                println!("stream: KPI ID: {:?}", _response);
                *kpi_id = Some(_response.clone());
                let mut should_ping = ping_trigger.lock().await;
                *should_ping = true;
            } else if event.event.clone().unwrap().event_type == 3 {
                println!("stream: New REMOVE event:\n{:?}", event);
                let mut should_ping = ping_trigger.lock().await;
                *should_ping = false;
            }
        }
    });

    futures::future::join_all(vec![t1, t2]).await;

    // let addr = "10.0.0.2".parse().unwrap();
    // let timeout = Duration::from_secs(1);
    // ping::ping(addr, Some(timeout), Some(166), Some(3), Some(5), Some(&random())).unwrap();

    // let server_address = env::var("CONTEXTSERVICE_SERVICE_HOST").unwrap();

    // let contexts = grpc_client.list_context_ids(tonic::Request::new(Empty {  })).await?;

    // println!("{:?}", contexts.into_inner());
    // let current_context = contexts.into_inner().context_ids[0].clone();

    // if let Some(current_context) = contexts.into_inner().context_ids[0] {

    // }
    // else {
    //     panic!("No context available!");
    // }

    // for context in contexts.into_inner().context_ids {
    //     println!("{:?}", context);
    // }

    // let services = grpc_client.list_services(tonic::Request::new(current_context)).await?;
    // println!("{:?}", services.into_inner());

    println!("Hello, world!");

    Ok(())
}
