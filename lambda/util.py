import iso8601
import pytz

## ISO8601 Datetime Format (used in v2)
ISO8601_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

## converts a ISO 8601 date time string to datetime
# @param iso8601_string a string formated like '%Y-%m-%dT%H:%M:%S%z'
# @return datetime
def ISO8601_to_datetime(iso8601_string):
    return iso8601.parse_date(iso8601_string).replace(tzinfo=None)

## converts datetime to ISO 8601 date time string
# @param d a datetime object
# @return ISO 8601 date time string
def datetime_to_ISO8601(d):
    return d.strftime(ISO8601_DATETIME_FORMAT)