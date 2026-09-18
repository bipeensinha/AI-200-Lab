import redis

# =========================================================
# Configuration
# =========================================================

# Replace with your Azure Managed Redis details
REDIS_HOST = "ai200-redis-bip.centralus.redis.azure.net"
REDIS_PORT = 10000
REDIS_PASSWORD = "MkomAitr2B1VCFTq3pp_SmpePxWYQdObDAZCAOZgs8Y="

REDIS_KEY = "ai200:ticket:T1001"

# =========================================================
# Redis Connection
# =========================================================

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    ssl=True,
    decode_responses=True
)

# =========================================================
# Test Connection
# =========================================================

print("=" * 50)
print("AZURE MANAGED REDIS LAB")
print("=" * 50)

print("\n1. Testing Redis connection...")
print("PING:", r.ping())

# ==========================================================
# Test Connection
# ==========================================================

print("=" * 60)
print("       AZURE MANAGED REDIS - DATA OPERATIONS LAB")
print("=" * 60)

print("\nTesting Redis connection...")

print("PING:", r.ping())


# ==========================================================
# Main Menu
# ==========================================================

while True:

    print("\n")
    print("-" * 60)
    print("Redis Operations")
    print("-" * 60)

    print("1. Create / Store Ticket")
    print("2. Read Ticket")
    print("3. Update Ticket")
    print("4. Set TTL")
    print("5. Check TTL")
    print("6. Delete Ticket")
    print("7. Check if Ticket Exists")
    print("8. Exit")

    choice = input("\nSelect an option: ").strip()


    # ======================================================
    # CREATE
    # ======================================================

    if choice == "1":

        ticket_id = input(
            "Enter ticket ID (example T1001): "
        ).strip()

        category = input(
            "Enter category: "
        ).strip()

        priority = input(
            "Enter priority: "
        ).strip()

        status = input(
            "Enter status: "
        ).strip()

        key = f"ai200:ticket:{ticket_id}"

        r.hset(
            key,
            mapping={
                "ticket_id": ticket_id,
                "category": category,
                "priority": priority,
                "status": status
            }
        )

        print("\nTicket stored successfully.")
        print("Redis Key:", key)


    # ======================================================
    # READ
    # ======================================================

    elif choice == "2":

        ticket_id = input(
            "Enter ticket ID: "
        ).strip()

        key = f"ai200:ticket:{ticket_id}"

        ticket = r.hgetall(key)

        if ticket:

            print("\nTicket information:")
            print(ticket)

        else:

            print("\nTicket not found.")


    # ======================================================
    # UPDATE
    # ======================================================

    elif choice == "3":

        ticket_id = input(
            "Enter ticket ID: "
        ).strip()

        key = f"ai200:ticket:{ticket_id}"

        if not r.exists(key):

            print("\nTicket does not exist.")

            continue

        print("\nWhat do you want to update?")

        print("1. Category")
        print("2. Priority")
        print("3. Status")

        field_choice = input(
            "Select field: "
        ).strip()

        if field_choice == "1":

            value = input(
                "Enter new category: "
            ).strip()

            r.hset(key, "category", value)

        elif field_choice == "2":

            value = input(
                "Enter new priority: "
            ).strip()

            r.hset(key, "priority", value)

        elif field_choice == "3":

            value = input(
                "Enter new status: "
            ).strip()

            r.hset(key, "status", value)

        else:

            print("Invalid option.")
            continue

        print("\nTicket updated successfully.")

        print(
            "Updated ticket:",
            r.hgetall(key)
        )


    # ======================================================
    # SET TTL
    # ======================================================

    elif choice == "4":

        ticket_id = input(
            "Enter ticket ID: "
        ).strip()

        key = f"ai200:ticket:{ticket_id}"

        if not r.exists(key):

            print("\nTicket does not exist.")

            continue

        seconds = int(
            input(
                "Enter TTL in seconds: "
            )
        )

        r.expire(key, seconds)

        print(
            f"\nExpiration set to {seconds} seconds."
        )


    # ======================================================
    # CHECK TTL
    # ======================================================

    elif choice == "5":

        ticket_id = input(
            "Enter ticket ID: "
        ).strip()

        key = f"ai200:ticket:{ticket_id}"

        ttl = r.ttl(key)

        if ttl == -2:

            print("\nTicket does not exist.")

        elif ttl == -1:

            print("\nTicket exists but has no expiration.")

        else:

            print(
                f"\nRemaining TTL: {ttl} seconds"
            )


    # ======================================================
    # DELETE
    # ======================================================

    elif choice == "6":

        ticket_id = input(
            "Enter ticket ID: "
        ).strip()

        key = f"ai200:ticket:{ticket_id}"

        if not r.exists(key):

            print("\nTicket does not exist.")

            continue

        try:

            result = r.delete(key)

            if result == 1:

                print("\nTicket deleted successfully.")

            else:

                print("\nTicket was not deleted.")

        except Exception as e:

            print("\nDelete operation failed.")
            print("Error:", e)


    # ======================================================
    # EXISTS
    # ======================================================

    elif choice == "7":

        ticket_id = input(
            "Enter ticket ID: "
        ).strip()

        key = f"ai200:ticket:{ticket_id}"

        exists = r.exists(key)

        print(
            "\nTicket exists:",
            bool(exists)
        )


    # ======================================================
    # EXIT
    # ======================================================

    elif choice == "8":

        print("\nExiting Redis lab...")

        break


    else:

        print("\nInvalid option. Please try again.")


print("\n" + "=" * 60)
print("LAB COMPLETED")
print("=" * 60)