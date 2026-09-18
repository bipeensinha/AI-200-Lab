import os
import json

from dotenv import load_dotenv

from azure.servicebus import ServiceBusClient


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Azure Service Bus Configuration
# ---------------------------------------------------------

CONNECTION_STRING = os.getenv(
    "SERVICE_BUS_CONNECTION_STRING"
)

QUEUE_NAME = os.getenv(
    "SERVICE_BUS_QUEUE_NAME",
    "ai-inference-queue"
)


# ---------------------------------------------------------
# Receive Messages
# ---------------------------------------------------------

def receive_messages():

    print("\n===================================")
    print("AI WORKER STARTED")
    print("===================================")
    print("Listening to queue:", QUEUE_NAME)
    print("Waiting for messages...\n")


    with ServiceBusClient.from_connection_string(
        conn_str=CONNECTION_STRING
    ) as client:

        with client.get_queue_receiver(
            queue_name=QUEUE_NAME,
            max_wait_time=10
        ) as receiver:

            for message in receiver:

                print("-----------------------------------")
                print("MESSAGE RECEIVED")
                print("-----------------------------------")


                # Convert message to text

                message_text = str(message)


                # Convert JSON text to Python object

                data = json.loads(message_text)


                print("Request ID :", data["requestId"])
                print("Issue      :", data["issue"])
                print("Category   :", data["category"])
                print("Priority   :", data["priority"])


                # -----------------------------------------
                # Simulate AI processing
                # -----------------------------------------

                print("\nAI Worker is processing request...")


                # -----------------------------------------
                # Complete message
                # -----------------------------------------

                receiver.complete_message(message)


                print("Message completed successfully.")
                print("-----------------------------------\n")


if __name__ == "__main__":

    receive_messages()