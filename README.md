# Industrial Internet of Things (IIoT) Training Modules

This will be a multi-chapter training that will conver the following topics:

# Prerequisites

## On-Premises Prequisites
- OPC UA Server
- A Virtual Machine that has network access to the OPC UA Server. 

## Azure Prerequisites
- [Azure Subscription](https://azure.microsoft.com/en-us/free/)
- Following Azure Services
  - [Azure IoT Hub](https://docs.microsoft.com/en-us/azure/iot-hub/)
  - [Azure Data Explorer](https://docs.microsoft.com/en-us/azure/data-explorer/)
  - [Azure Blob Storage](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction) & [Azure Data Lake Store Gen 2](https://docs.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction)
  - [Azure Digital Twin](https://docs.microsoft.com/en-us/azure/digital-twins/)
  - [Azure Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/)
  - [Azure Event Grid](https://docs.microsoft.com/en-us/azure/event-grid/)


## Developer Desktop Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [VS Code](https://code.visualstudio.com/Download)

|Deployment Location|Module #|Module Name|Description|
|-------------------|:------:|-----------|-----------|
|Edge               |1       |Azure IoT Edge Deployment|You will learn how to deploy Azure IoT Edge on a Linux VM|
|Edge               |2       |OPC Publisher|Learn how to configure OPC Publisher to connect to an OPC UA Server and pull tags from that server|
|Edge               |3       |SQL|Learn how to ingest data from IoT Edge into a Azure SQL Edge Database|
|Edge               |4       |Dashboarding|How to build dashboards that are consumable at the edge|
|Edge               |5       |Monitoring|Monitoring different azure iot edge modules|
|Cloud              |6       |Cloud to Device Commands|Learn how to send commands from Cloud to the Device|
|Cloud              |7       |Azure Digital Twins|Learn how to publish OPC UA data to Azure Digital Twins|
|Cloud              |8       |Warm Path Analytics|Ingesting data with IoT Data Explorer and Dashboarding|
|Cloud              |9       |Cold Path Analytics|Set up routing of Telemetry to Azure Data Lake Store|

