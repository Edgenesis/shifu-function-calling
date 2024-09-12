# Shifu Function Calling Demo

## Prepare

Before running the demo, you need to install the following tools:
- [Docker](https://docs.docker.com/get-docker/)
- [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

Make sure Docker is running before proceeding by running the following command.

```bash
docker ps
```

## Setup deviceShifu

Create a Kind cluster and deploy the Ingress controller and Shifu.

```bash
kind create cluster --config=config.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl apply -f https://raw.githubusercontent.com/Edgenesis/shifu/v0.52.0/pkg/k8s/crd/install/shifu_install.yml
```

Deploy deviceShifu for Camera (RTSP), Siemens PLC (S7) and LED (OPC UA).

```bash
kubectl create secret -n deviceshifu generic camera-secret  --from-literal=IP_CAMERA_PASSWORD={CAMERA_PASSWORD}
kubectl apply -f deviceshifu
kubectl apply -f ingress.yaml
```

To view the camera stream, open the following URL in the browser.

```bash
http://localhost:30080/deviceshifu-camera/stream?timeout=0
```

To send a single bit to the PLC, run the following command.

```bash
curl "localhost:30080/deviceshifu-plc/sendsinglebit?rootaddress=Q&address=0&start=0&digit=1&value=0"; echo
curl "localhost:30080/deviceshifu-plc/sendsinglebit?rootaddress=Q&address=0&start=0&digit=1&value=1"; echo
```

To read from LED, run the following command.

```bash
curl "localhost:30080/deviceshifu-led/number"
``` 

To write to LED, run the following command.

```bash
curl -XPOST -d '{"value":2999}' "localhost:30080/deviceshifu-led/number"
```

## Run function calling demo