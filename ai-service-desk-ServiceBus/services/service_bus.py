import os

from azure.servicebus import (
    ServiceBusClient,
    ServiceBusMessage
)

from dotenv import load_dotenv


# =========================================================
# Load environment variables
# =========================================================

load_dotenv()


# =========================================================
# Azure Service Bus Configuration
# =========================================================

SERVICE_BUS_CONNECTION_STRING = os.getenv(
    "SERVICE_BUS_CONNECTION_STRING"
)

QUEUE_NAME = os.getenv(
    "SERVICE_BUS_QUEUE_NAME",
    "ai-inference-queue"
)


# =========================================================
# Send AI Inference Request
# =========================================================

def send_message(
    request_id,
    issue,
    category,
    priority
):

    # Create the message body

    message_body = {

        "requestId": request_id,

        "issue": issue,

        "category": category,

        "priority": priority

    }


    # Convert dictionary to JSON

    import json

    message_json = json.dumps(
        message_body
    )


    # Create Service Bus client

    with ServiceBusClient.from_connection_string(
        conn_str=SERVICE_BUS_CONNECTION_STRING
    ) as client:

        # Create queue sender

        with client.get_queue_sender(
            queue_name=QUEUE_NAME
        ) as sender:

            # Create Service Bus message

            message = ServiceBusMessage(
                message_json
            )


            # Send message

            sender.send_messages(
                message
            )


    print(
        f"Message sent successfully: {request_id}"
    )

    return True