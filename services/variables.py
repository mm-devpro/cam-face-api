API_URL = '/api/v1'

USER_ROLES = [
    "user"
]
ADMIN_ROLES = [
    "admin",
    "super-admin"
]

PROFILE_GROUP = {
    "acc": "all access",
    "coll": "collaborator",
    "ma": "manager",
    "dir": "director",
    "cus": "customer",
    "vip": "vip",
    "own": "owner",
    "par": "partner",
    "fam": "family",
    "fr": "friend",
    "inv": "invite"
}

LOCKER_TYPE = [
    "door",
    "gate",
    "safe",
    "other"
]

LOCKER_ACCESS = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5"
]

# Validation args for "GET" Methods
ACCESS_VALIDATED_GET_ARGS = ['group', 'digit_pwd', 'profile_id']
ACCOUNT_VALIDATED_GET_ARGS = ['name']
CAMERA_VALIDATED_GET_ARGS = ['source', 'active']
LOCKER_VALIDATED_GET_ARGS = ['name', 'access_lvl', 'type', 'locked', 'digit_activation']
PROFILE_VALIDATED_GET_ARGS = ['name', 'surname', 'dob']
USER_VALIDATED_GET_ARGS = ['username', 'email', 'role']
# Validation args for "POST" "PUT" "DELETE" Methods
ACCESS_VALIDATED_ARGS = ['group', 'digit_pwd']
ACCOUNT_VALIDATED_ARGS = ['name']
CAMERA_VALIDATED_ARGS = ['source', 'active']
LOCKER_VALIDATED_ARGS = ['name', 'access_lvl', 'type', 'locked', 'digit_activation']
PROFILE_VALIDATED_ARGS = ['name', 'surname', 'dob']
USER_VALIDATED_ARGS = ['username', 'email', 'role']
