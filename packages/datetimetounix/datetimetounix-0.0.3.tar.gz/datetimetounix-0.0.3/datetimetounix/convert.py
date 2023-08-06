import datetime

def convert(conversion: datetime.datetime):
    x = conversion.replace(tzinfo=datetime.timezone.utc).timestamp()
    y = "{:.0f}".format(x)
    return int(y)
