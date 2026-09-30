from fastapi import Header, HTTPException


def get_current_user(
    authorization: str | None = Header(default=None)
):
    if authorization not in [
        "Bearer user-token",
        "Bearer admin-token"
    ]:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    if authorization == "Bearer admin-token":
        return {
            "role": "admin"
        }

    return {
        "role": "user"
    }


def require_admin(user: dict):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin permission required"
        )

    return user
