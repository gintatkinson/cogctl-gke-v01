# TeraFlowSDN Ztp service

This repository hosts the TeraFlowSDN Ztp service, also known as Zero-Touch Provisioning (ZTP) service.
Follow the instructions below to build, test, and run this service on your local environment.

## TeraFlowSDN Ztp service architecture

The TeraFlowSDN Ztp architecture consists of six (6) interfaces listed below:

Interfaces |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1. The `ZtpGateway` interface that implements all the RPC functions that are described in `ztp.proto` file. |
| 2. The `ContextGateway` interface that communicates with a `Context` Service gRPC client to invoke key RPC functions described in `context.proto` file. |
| 3. The `DeviceGateway` interface that communicates with a `Device` Service gRPC client to invoke key RPC functions described in `device.proto` file. |
| 4. The `ZtpService` interface that implements the `addDevice()`, `updateDevice()`, and `deleteDevice()` methods by communicating with a `Context` gRPC client and a `Device` gRPC client through the use of `ContextService` interface and `DeviceService` interface respectively. |
| 5. The `ContextService` interface that implements the `getDevice()` and `getDeviceEvents()` methods by communicating with a `Context` gRPC client through the use of `ContextGateway` interface. |
| 6. The `DeviceService` interface that implements the `getInitialConfiguration()`, `configureDevice()`, and `deleteDevice()` methods by communicating with a `Device` gRPC client through the use of `DeviceGateway` interface. |


## Prerequisites

The Ztp service is currently tested against Ubuntu 20.04 and Java 11.

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
kubectl apply -f "manifests/ztpservice.yaml"
```

## Maintainers

This TeraFlowSDN service is implemented by [UBITECH](https://www.ubitech.eu).

Feel free to contact Georgios Katsikas (gkatsikas at ubitech dot eu) in case you have questions.
