from mcp.server.mcpserver import MCPServer


# ---------------------------------------------------------
# Create MCP Server
# ---------------------------------------------------------

mcp = MCPServer("AI Service Desk")


# ---------------------------------------------------------
# Knowledge Base
# ---------------------------------------------------------

KNOWLEDGE_BASE = {
    "vpn": {
        "title": "VPN Connection Problems",
        "solution": (
            "If the company VPN is not connecting, first verify "
            "your internet connection. Restart the VPN client and "
            "try connecting again. If the problem continues, "
            "restart the laptop and retry."
        )
    },

    "password": {
        "title": "Password Reset",
        "solution": (
            "Use the company password reset portal to change "
            "your password. After resetting it, sign in again "
            "to the required applications."
        )
    },

    "laptop": {
        "title": "Laptop Performance",
        "solution": (
            "Restart the laptop, close unnecessary applications, "
            "and check available disk space."
        )
    }
}


# ---------------------------------------------------------
# MCP Tool
# ---------------------------------------------------------

@mcp.tool()
def search_knowledge_base(query: str) -> str:
    """
    Search the IT knowledge base for common support problems.
    """

    query = query.lower()

    for keyword, article in KNOWLEDGE_BASE.items():

        if keyword in query:

            return (
                f"Knowledge Base Article: {article['title']}\n\n"
                f"Recommended Solution:\n"
                f"{article['solution']}"
            )

    return (
        "No matching knowledge-base article was found. "
        "Please create a support ticket for further assistance."
    )


# ---------------------------------------------------------
# MCP Tool - Ticket Status
# ---------------------------------------------------------

@mcp.tool()
def get_ticket_status(ticket_id: str) -> str:
    """
    Get the status of an IT support ticket.
    """

    tickets = {
        "T1001": {
            "status": "In Progress",
            "team": "Network Team",
            "message": "Network team is investigating the VPN issue."
        },
        "T1002": {
            "status": "Resolved",
            "team": "Identity Team",
            "message": "Password reset request has been completed."
        },
        "T1003": {
            "status": "Waiting for Approval",
            "team": "Endpoint Team",
            "message": "Laptop replacement request is awaiting approval."
        }
    }

    ticket = tickets.get(ticket_id.upper())

    if not ticket:
        return f"Ticket {ticket_id} was not found."

    return (
        f"Ticket ID: {ticket_id.upper()}\n"
        f"Status: {ticket['status']}\n"
        f"Assigned Team: {ticket['team']}\n"
        f"Details: {ticket['message']}"
    )


# ---------------------------------------------------------
# MCP Tool - Create Ticket
# ---------------------------------------------------------

@mcp.tool()
def create_support_ticket(
    issue: str,
    priority: str = "Medium"
) -> str:
    """
    Create a simple IT support ticket.
    """

    ticket_id = "T2001"

    return (
        f"Support ticket created successfully.\n\n"
        f"Ticket ID: {ticket_id}\n"
        f"Priority: {priority}\n"
        f"Issue: {issue}"
    )


# ---------------------------------------------------------
# Start MCP Server
# ---------------------------------------------------------

if __name__ == "__main__":
    mcp.run()