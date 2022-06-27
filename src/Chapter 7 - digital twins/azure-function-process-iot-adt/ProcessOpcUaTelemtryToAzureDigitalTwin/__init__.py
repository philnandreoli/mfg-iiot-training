import json
import logging
import os
import urllib
import sys
import azure.functions as func

from azure.digitaltwins.core import DigitalTwinsClient
from azure.identity import DefaultAzureCredential

def getUrlResponse(url):
    response = urllib.request.urlopen(url)
    if (response.getcode()==200):
        data = response.read()
    else:
        print("Error receiving data", response.getcode())
   
    return data

def main(event: func.EventGridEvent):   
    
    logger = logging.getLogger('azure')
  
    # set the logging level of the runtime
    if(os.getenv("LOGGING_LEVEL") == "DEBUG"):
        logger.setLevel(logging.DEBUG)
    elif (os.getenv("LOGGING_LEVEL") == "INFO"):
        logger.setLevel(logging.INFO)
    elif (os.getenv("LOGGING_LEVEL") == "CRITICAL"):
        logger.setLevel(logging.CRITICAL)
    elif (os.getenv("LOGGING_LEVEL") == "WARNING"):
        logger.setLevel(logging.WARNING)
    elif (os.getenv("LOGGING_LEVEL") == "WARN"):
        logger.setLevel(logging.WARN)
    else:
        logger.setLevel(logging.ERROR)
        
    handler = logging.StreamHandler(stream=sys.stdout)
    logger.addHandler(handler)

    # get the azure digital twin url from the environment variable
    adt_url = os.getenv("AZURE_ADT_URL")
    
    # get the mapping file from the environment varibale
    mapping_file = eval(getUrlResponse(os.getenv("JSON_MAPPING_URL")))

    data = event.get_json()
    event_body = data['body']
    
    logging.info("Node Id: {}".format(event_body['NodeId']))

    try:
        for i in mapping_file:
            if(i['NodeId'] == event_body['NodeId']): 
                twin_id = i['TwinId']
                twin_property = i['Property']
                model_id = i['ModelId']
                node_id = i['NodeId']

                logging.info("Twin Id: {}".format(twin_id))
                logging.info("Twin Property: {}".format(twin_property))
                logging.info("Model Id: {}".format(model_id))

                # Create the credential that will be used to authenticate with the ADT service
                credential = DefaultAzureCredential()
                # Create the adt client
                adt_client = DigitalTwinsClient(endpoint=adt_url, credential=credential, logging_enable=True)

                current_value = event_body['Value']['Body']

                logging.info("Current Value: {}".format(current_value))

                patch = [
                    {
                        "op": "replace",
					    "path": "/{}".format(twin_property),
					    "value": current_value
                    }
                ]

                test = adt_client.update_digital_twin(twin_id, patch, logging_enable=True)
                print("What was the response: {}".format(test))
    except Exception as e:
        print("Error: {}".format(str(e)))

