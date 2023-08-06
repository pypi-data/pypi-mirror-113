import datetime

def convert(conversion: datetime.datetime):
    x = conversion.replace(tzinfo=datetime.timezone.utc).timestamp()
    return x
