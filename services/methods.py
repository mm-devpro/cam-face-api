from datetime import datetime
from dateutil import parser


def string_to_iso_format(string):
    return parser.parse(string).date().isoformat()

