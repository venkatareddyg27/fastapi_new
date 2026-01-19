from app.core.permissions import (
    USER_CREATE,
    USER_READ,
    USER_UPDATE,
    USER_DELETE,
)

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
