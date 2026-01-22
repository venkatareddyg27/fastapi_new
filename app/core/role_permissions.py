from app.core.permissions import (
    USER_CREATE,
    USER_READ,
    USER_UPDATE,
    USER_DELETE,
)
ALLOWED_ROLES = {"user", "admin", "superadmin"}
ROLE_PERMISSIONS = {
    "user": [
        USER_CREATE,
    ],
    "admin": [
        USER_CREATE,
        USER_READ,
        USER_UPDATE,
    ],
    "superadmin": [
        USER_CREATE,
        USER_READ,
        USER_UPDATE,
        USER_DELETE,
    ],
}
