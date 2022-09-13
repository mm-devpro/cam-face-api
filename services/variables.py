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

LOCKER_ACCESS = {
    "0": "basic",
    "1": "low",
    "2": "normal",
    "3": "high",
    "4": "very-high",
    "5": "critical"
}

PROFILE_VALIDATION = {
    1: "created",
    2: "ok",
    3: "verified",
    4: "validated"
}
GENDER = [
    "male",
    "female",
    "other"
]

# Validation args for "GET" Methods
ACCESS_VALIDATED_GET_ARGS = ['group', 'password', 'profile_id', 'access_lvl', 'account_id']
ACCOUNT_VALIDATED_GET_ARGS = ['name']
CAMERA_VALIDATED_GET_ARGS = ['name', 'source', 'active', 'locker_id']
LOCKER_VALIDATED_GET_ARGS = ['name', 'access_lvl', 'type', 'locked', 'digit_activation']
PROFILE_VALIDATED_GET_ARGS = ['name', 'surname', 'dob', 'gender', 'val_num', 'validated']
USER_VALIDATED_GET_ARGS = ['username', 'email', 'role']
# Validation args for "POST" "PUT" "DELETE" Methods
ACCESS_VALIDATED_ARGS = ['group', 'password', 'access_lvl']
ACCOUNT_VALIDATED_ARGS = ['name']
CAMERA_VALIDATED_ARGS = ['name', 'source', 'active', 'locker_id']
LOCKER_VALIDATED_ARGS = ['name', 'access_lvl', 'type', 'locked', 'digit_activation']
PROFILE_VALIDATED_ARGS = ['name', 'surname', 'dob', 'encodings', 'gender', 'val_num', 'validated']
USER_VALIDATED_ARGS = ['username', 'email', 'role', 'password', 'img']
