"""Role 6: bounded repair with preserved failure evidence."""
def recovery_decision(*, attempts: int, max_attempts: int = 2,
                      destructive: bool = False, user_authorized: bool = False) -> dict[str, str | bool]:
    if destructive and not user_authorized:
        return {"may_retry": False, "status": "blocked", "reason": "destructive action lacks explicit authorization"}
    if attempts >= max_attempts:
        return {"may_retry": False, "status": "blocked", "reason": "bounded recovery attempts exhausted"}
    return {"may_retry": True, "status": "retry_allowed", "reason": "preserve error, make one narrow repair, rerun the failed check"}
