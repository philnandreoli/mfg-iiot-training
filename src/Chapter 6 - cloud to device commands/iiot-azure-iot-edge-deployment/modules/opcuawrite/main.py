# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.
import asyncio
import sys
import signal
import threading
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import Message, MethodResponse
from opcua import Client
from opcua import ua

# Event indicating client stop
stop_event = threading.Event()


def create_client():
    client = IoTHubModuleClient.create_from_edge_environment()

    #Define a method request handler 
    async def method_request_handler(method_request):
        if method_request.name == "UpdateOpcUaTag":
            try:
                print("Method Received: In Here!")
                print("Method Request: {}".format(method_request))
                print("Method Request Payload: {}".format(method_request.payload))

                opcua_server = method_request.payload["opcUaServer"]
                node = method_request.payload["node"]
                value = method_request.payload["value"]
                print("OPC UA SERVER: {}".format(opcua_server))
                print("NODE: {}".format(node))
                print("VALUE: {}".format(value))
                
                # Create a connection the opc ua server that is used for the tag
                opcua_client = Client(opcua_server)
                opcua_client.application_uri = "urn:OpcTwinIoTEdgeModule:OpcUaTwin:python-opcua"
                opcua_client.secure_channel_timeout = 10000
                opcua_client.session_timeout = 10000

                # Connect to the opc ua server 
                opcua_client.connect()

                # Get the specific tag for the opc ua server 
                tag = opcua_client.get_node(node)

                # Set the new value
                data_value = ua.DataValue(value)
                data_value.ServerTimestamp = None
                data_value.SourceTimestamp = None

                tag.set_value(data_value)

            except ValueError:
                response_payload = {"Response": "Invalid parameter"}
                response_status = 500
            except TypeError as e:
                response_payload = {"Response": "Type Error: {}".format(str(e)) }
                response_status = 500
            else:
                response_payload = {"Response": "Executed direct method {}".format(method_request.name)}
                response_status = 200
            finally:
                opcua_client.disconnect()
        else:
            response_payload = {"Response": "Direct method {} not defined".format(method_request.name)}
            response_status = 404

        method_response = MethodResponse.create_from_method_request(method_request, response_status, response_payload)
        await client.send_method_response(method_response)
            
            
    try:
        # Set handler on the client
        client.on_method_request_received = method_request_handler
    except:
        # Cleanup if failure occurs
        client.shutdown()
        raise

    return client


async def run_telemetry(client):
    while True:
        await asyncio.sleep(1000)


def main():
    if not sys.version >= "3.5.3":
        raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
    print ( "IoT Hub Client for Python" )

    # NOTE: Client is implicitly connected due to the handler being set on it
    client = create_client()

    # Define a handler to cleanup when module is is terminated by Edge
    def module_termination_handler(signal, frame):
        print ("IoTHubClient sample stopped by Edge")
        stop_event.set()

    # Set the Edge termination handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    # Run the sample
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_telemetry(client))
    except Exception as e:
        print("Unexpected error %s " % e)
        raise
    finally:
        print("Shutting down IoT Hub Client...")
        loop.run_until_complete(client.shutdown())
        loop.close()


if __name__ == "__main__":
    main()
