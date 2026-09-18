import os
import time

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


# =========================================================
# Configuration
# =========================================================

KEY_VAULT_NAME = os.environ["KEY_VAULT_NAME"]

KEY_VAULT_URL = (
    f"https://{KEY_VAULT_NAME}.vault.azure.net/"
)


# =========================================================
# Azure Authentication
# =========================================================

credential = DefaultAzureCredential()

client = SecretClient(
    vault_url=KEY_VAULT_URL,
    credential=credential
)


# =========================================================
# Retrieve Secret
# =========================================================

def get_secret(secret_name):

    print(f"\nRetrieving secret: {secret_name}")

    secret = client.get_secret(secret_name)

    print("Secret retrieved successfully.")

    return secret.value


# =========================================================
# List Secret Metadata
# =========================================================

def list_secrets():

    print("\nAvailable secrets:")

    for secret in client.list_properties_of_secrets():

        print(
            f"- {secret.name}"
            f" | Enabled: {secret.enabled}"
        )


# =========================================================
# Secret Version
# =========================================================

def show_secret_version(secret_name):

    secret = client.get_secret(secret_name)

    print("\nSecret information")
    print("------------------")
    print("Name   :", secret.name)
    print("Version:", secret.properties.version)
    print("Created:", secret.properties.created_on)


# =========================================================
# Simple Cache
# =========================================================

cache = {}

CACHE_SECONDS = 60


def get_secret_cached(secret_name):

    current_time = time.time()

    if secret_name in cache:

        cached_value, timestamp = cache[secret_name]

        if current_time - timestamp < CACHE_SECONDS:

            print("Returning secret from cache.")

            return cached_value

    print("Retrieving secret from Key Vault.")

    value = get_secret(secret_name)

    cache[secret_name] = (
        value,
        current_time
    )

    return value


# =========================================================
# Main
# =========================================================

if __name__ == "__main__":

    print("=" * 50)
    print("AI SERVICE DESK - KEY VAULT DEMO")
    print("=" * 50)

    # 1. List metadata
    list_secrets()

    # 2. Retrieve API key
    api_key = get_secret("AI-API-Key")

    print("\nAPI key retrieved.")
    print("Value is intentionally NOT displayed.")

    # 3. Show version
    show_secret_version("AI-API-Key")

    # 4. Demonstrate cache
    print("\nTesting cache...")

    get_secret_cached("AI-API-Key")

    get_secret_cached("AI-API-Key")

    print("\nDemo completed.")
