# TeraFlowSDN Policy Management service

This repository hosts the TeraFlowSDN Policy Management service.
Follow the instructions below to build, test, and run this service on your local environment.

## TeraFlowSDN Policy Management service architecture

The TeraFlowSDN Policy Management service architecture consists of ten (10) interfaces listed below:

Interfaces |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  1. The `PolicyGateway` interface that implements all the RPC functions that are described in `policy.proto` file. |
|  2. The `MonitoringGateway` interface that communicates with a `Monitoring` service gRPC client to invoke key RPC functions described in `monitoring.proto` file. |
|  3. The `ContextGateway` interface that communicates with a `Context` service gRPC client to invoke key RPC functions described in `context.proto` file. |
|  4. The `ServiceGateway` interface that communicates with a `Service` service gRPC client to invoke key RPC functions described in `service.proto` file. |
|  5. The `DeviceGateway` interface that communicates with a `Device` service gRPC client to invoke key RPC functions described in `device.proto` file. |
|  6. The `PolicyService` interface that implements the Policy RPC methods by communicating with a `Monitoring` gRPC client, a `Context` gRPC client, a `Service` gRPC client, and a `Device` gRPC client through the `MonitoringService`, `ContextService`, `ServiceService`, and `DeviceService` interfaces respectively. |
|  7. The `MonitoringService` interface that implements the `SetKpiAlarm()` and `GetAlarmResponseStream()` methods by communicating with a `Monitoring` gRPC client through the use of the `MonitoringGateway` interface. |
|  8. The `ContextService` interface that implements the `GetService()`, `GetDevice()`, `GetPolicyRule`, `SetPolicyRule`, and `DeletePolicyRule` methods by communicating with a `Context` gRPC client through the use of the `ContextGateway` interface. |
|  9. The `ServiceService` interface that implements the `UpdateService()` method by communicating with a `Service` gRPC client through the use of the `ServiceGateway` interface. |
| 10. The `DeviceService` interface that implements the `ConfigureDevice()` method by communicating with a `Device` gRPC client through the use of the `DeviceGateway` interface. |

## Prerequisites

The TeraFlowSDN Policy Management service is currently tested against Ubuntu 20.04 and Java 11.

To quickly install Java 11 on a Debian-based Linux distro do:

```bash
sudo apt-get install openjdk-11-jdk -y
```

Feel free to try more recent Java versions.

## Compile

```bash
./mvnw compile
```

## Run tests

```bash
./mvnw test
```

## Run service

```bash
./mvnw quarkus:dev
````

## Clean

```bash
./mvnw clean
```

## Deploying on a Kubernetes cluster

To create the K8s manifest file under `target/kubernetes/kubernetes.yml` to be used run

```bash
./mvnw clean package -DskipUTs -DskipITs
```

To deploy the application in a K8s cluster run

```bash
kubectl apply -f "manifests/policyservice.yaml"
```

## Maintainers

This TeraFlowSDN service is implemented by [UBITECH](https://www.ubitech.eu).

Feel free to contact Georgios Katsikas (gkatsikas at ubitech dot eu) in case you have questions.
