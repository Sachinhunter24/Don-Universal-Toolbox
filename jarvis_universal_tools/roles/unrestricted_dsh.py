"""Role 10: reserved compatibility slot; deliberately inactive.

This module does not provide unrestricted access and must never bypass tool
permissions, authentication, policy, or explicit user constraints.
"""
def status() -> dict[str, str | bool]:
    return {
        "name": "Unrestricted.DSH",
        "active": False,
        "status": "reserved",
        "reason": "No privileged bypass behavior is implemented."
    }
