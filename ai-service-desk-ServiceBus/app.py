from flask import Flask, render_template, request, jsonify
from datetime import datetime

# Azure Service Bus
from services.service_bus import send_message


app = Flask(__name__)


# ---------------------------------------------------------
# Home Page
# ---------------------------------------------------------
@app.route("/")
def dashboard():
    return render_template("index.html")


# ---------------------------------------------------------
# Submit AI Request
# ---------------------------------------------------------
@app.route("/api/submit", methods=["POST"])
def submit_request():

    data = request.get_json()

    issue = data.get("issue", "")
    category = data.get("category", "General")
    priority = data.get("priority", "Medium")

    # -----------------------------------------------------
    # Basic validation
    # -----------------------------------------------------
    if not issue.strip():

        return jsonify({
            "success": False,
            "message": "Please describe your issue."
        }), 400


    # -----------------------------------------------------
    # Create Request ID
    # -----------------------------------------------------
    request_id = "REQ-" + datetime.now().strftime("%H%M%S")


    # -----------------------------------------------------
    # Display request in terminal
    # -----------------------------------------------------
    print("\n===================================")
    print("AI INFERENCE REQUEST")
    print("===================================")
    print("Request ID :", request_id)
    print("Issue      :", issue)
    print("Category   :", category)
    print("Priority   :", priority)
    print("===================================")


    # -----------------------------------------------------
    # Send request to Azure Service Bus
    # -----------------------------------------------------
    try:

        send_message(
            request_id=request_id,
            issue=issue,
            category=category,
            priority=priority
        )

        print("Status     : Message sent to Service Bus")
        print("===================================\n")


        return jsonify({

            "success": True,

            "requestId": request_id,

            "message":
                "AI request sent to Azure Service Bus.",

            "status":
                "Queued"

        })


    except Exception as e:

        print("\nERROR: Unable to send message")
        print(e)
        print("===================================\n")


        return jsonify({

            "success": False,

            "message":
                "Unable to send request to Azure Service Bus.",

            "error":
                str(e)

        }), 500


# ---------------------------------------------------------
# Run Flask Application
# ---------------------------------------------------------
if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=8000,
        debug=True
    )