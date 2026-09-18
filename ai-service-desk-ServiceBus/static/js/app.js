// =========================================================
// AI SERVICE DESK
// Frontend JavaScript
// =========================================================


// =========================================================
// SUBMIT AI INFERENCE REQUEST
// =========================================================

function submitRequest() {

    const issue =
        document.getElementById("issue").value;

    const category =
        document.getElementById("category").value;

    const priority =
        document.getElementById("priority").value;

    const button =
        document.getElementById("submitButton");

    const message =
        document.getElementById("message");


    // -----------------------------------------------------
    // Validate user input
    // -----------------------------------------------------

    if (issue.trim() === "") {

        message.style.display = "block";

        message.style.background = "#4b1e2b";

        message.style.color = "#ff8095";

        message.innerText =
            "Please describe your issue.";

        return;
    }


    // -----------------------------------------------------
    // Disable button while request is being submitted
    // -----------------------------------------------------

    button.disabled = true;

    button.innerText =
        "Submitting...";


    // -----------------------------------------------------
    // Send request to Flask
    // -----------------------------------------------------

    fetch("/api/submit", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            issue: issue,

            category: category,

            priority: priority

        })

    })


    // -----------------------------------------------------
    // Read Flask response
    // -----------------------------------------------------

    .then(response => {

        if (!response.ok) {
            throw new Error(
                "Request failed"
            );
        }

        return response.json();

    })


    // -----------------------------------------------------
    // Process response
    // -----------------------------------------------------

    .then(data => {

        if (data.success) {

            message.style.display = "block";

            message.style.background =
                "#073e35";

            message.style.color =
                "#3be0ae";

            message.innerText =
                "✓ Request " +
                data.requestId +
                " submitted successfully!";


            // Update the demo workflow

            updateWorkflow();


            // Add activity message

            addActivity(
                "📤",
                "Request Submitted",
                "New AI inference request received"
            );

        }

    })


    // -----------------------------------------------------
    // Handle errors
    // -----------------------------------------------------

    .catch(error => {

        console.error(error);

        message.style.display = "block";

        message.style.background =
            "#4b1e2b";

        message.style.color =
            "#ff8095";

        message.innerText =
            "Unable to submit request.";

    })


    // -----------------------------------------------------
    // Enable button again
    // -----------------------------------------------------

    .finally(() => {

        button.disabled = false;

        button.innerText =
            "➤ Submit Request";

    });

}


// =========================================================
// UPDATE AI AGENT WORKFLOW
// =========================================================

function updateWorkflow() {


    // -----------------------------------------------------
    // STEP 1
    // Request Received
    // -----------------------------------------------------

    setStep(
        "step1",
        "status1",
        "Completed",
        "done"
    );


    // -----------------------------------------------------
    // STEP 2
    // Service Bus Queue
    // -----------------------------------------------------

    setTimeout(() => {

        setStep(
            "step2",
            "status2",
            "In Progress",
            "processing"
        );

        addActivity(
            "📋",
            "Queued in Service Bus",
            "Request added to inference queue"
        );

    }, 1000);


    // -----------------------------------------------------
    // STEP 3
    // AI Processing
    // -----------------------------------------------------

    setTimeout(() => {

        setStep(
            "step2",
            "status2",
            "Completed",
            "done"
        );

        setStep(
            "step3",
            "status3",
            "In Progress",
            "processing"
        );

        addActivity(
            "⚙️",
            "AI Processing Started",
            "AI inference is processing the request"
        );

    }, 2500);


    // -----------------------------------------------------
    // STEP 4
    // Resolution Ready
    // -----------------------------------------------------

    setTimeout(() => {

        setStep(
            "step3",
            "status3",
            "Completed",
            "done"
        );

        setStep(
            "step4",
            "status4",
            "Completed",
            "done"
        );

        addActivity(
            "✓",
            "Resolution Ready",
            "AI processing completed"
        );

    }, 4500);

}


// =========================================================
// UPDATE INDIVIDUAL WORKFLOW STEP
// =========================================================

function setStep(
    stepId,
    statusId,
    text,
    className
) {

    const step =
        document.getElementById(stepId);

    const status =
        document.getElementById(statusId);


    // Remove previous state

    step.classList.remove(
        "active",
        "completed"
    );


    // Update status badge

    status.className =
        "status " + className;

    status.innerText =
        text;


    // Apply new state

    if (className === "done") {

        step.classList.add(
            "completed"
        );

    }
    else {

        step.classList.add(
            "active"
        );

    }

}


// =========================================================
// ADD ACTIVITY FEED MESSAGE
// =========================================================

function addActivity(
    icon,
    title,
    description
) {

    const feed =
        document.getElementById(
            "activityFeed"
        );


    const item =
        document.createElement("div");

    item.className =
        "activity-item";


    // Current time

    const time =
        new Date().toLocaleTimeString();


    // Create activity HTML

    item.innerHTML = `

        <div class="activity-icon">
            ${icon}
        </div>

        <div class="activity-text">

            <strong>
                ${title}
            </strong>

            <p>
                ${description}
            </p>

            <time>
                ${time}
            </time>

        </div>

    `;


    // Add newest activity at the top

    feed.prepend(item);

}