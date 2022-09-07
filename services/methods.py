from datetime import datetime
from dateutil import parser


def string_to_date_format(string):
    return parser.parse(string).date()


def date_to_string_format(string):
    return datetime.strftime(string, "%d/%m/%Y")
