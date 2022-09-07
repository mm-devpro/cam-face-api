API_URL = '/api/v1'

USER_ROLES = [
    "user"
]
ADMIN_ROLES = [
    "admin",
    "super-admin"
]

PROFILE_GROUP = [
    "All Access",
    "Collaborator",
    "Manager",
    "Director",
    "Customer",
    "VIP",
    "Owner",
    "Partner",
    "Family Member",
    "Friend",
    "Invite"
]

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


ACCESS_VALIDATED_GET_ARGS = ['group', 'digit_pwd', 'profile_id', 'account_id']
ACCOUNT_VALIDATED_GET_ARGS = ['name', 'users', 'lockers', 'cameras']
CAMERA_VALIDATED_GET_ARGS = ['source', 'active', 'account_id', 'locker_id']
LOCKER_VALIDATED_GET_ARGS = ['name', 'access_lvl', 'type', 'locked', 'digit_activation', 'account_id', 'camera']
PROFILE_VALIDATED_GET_ARGS = ['name', 'surname', 'dob', 'access']
USER_VALIDATED_GET_ARGS = ['username', 'email', 'account_id', 'role']
