import azure.functions as func

app = func.FunctionApp()


# ---------------------------------------------------------
# MCP TOOL - Search Knowledge Base
# ---------------------------------------------------------

@app.mcp_tool()
def search_knowledge_base(query: str) -> str:

    query = query.lower()

    if "vpn" in query:
        return (
            "VPN Troubleshooting:\n"
            "1. Check internet connectivity.\n"
            "2. Restart the VPN client.\n"
            "3. Verify corporate credentials.\n"
            "4. Contact Network Support if required."
        )

    if "password" in query:
        return (
            "Password Reset:\n"
            "1. Open the password portal.\n"
            "2. Complete MFA verification.\n"
            "3. Create a new password."
        )

    return "No matching knowledge article found."


# ---------------------------------------------------------
# MCP TOOL - Create Ticket
# ---------------------------------------------------------

@app.mcp_tool()
def create_support_ticket(
    issue: str,
    priority: str = "Medium"
) -> str:

    return (
        "Support ticket created.\n"
        "Ticket ID: INC-1001\n"
        f"Issue: {issue}\n"
        f"Priority: {priority}"
    )


# ---------------------------------------------------------
# MCP TOOL - Ticket Status
# ---------------------------------------------------------

@app.mcp_tool()
def get_ticket_status(ticket_id: str) -> str:

    return (
        f"Ticket: {ticket_id}\n"
        "Status: In Progress\n"
        "Assigned Team: Network Support"
    )