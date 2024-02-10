from datetime import datetime
from pytz import timezone


    
def convert_cst_to_zulu(cst_datetime):
    # Define time zones
    cst_tz = timezone('America/Chicago')  # Central Standard Time
    zulu_tz = timezone('UTC')  # Coordinated Universal Time (Zulu)

    # Localize the input CST datetime
    localized_cst = cst_tz.localize(cst_datetime)

    # Convert the localized CST datetime to Zulu time
    zulu_datetime = localized_cst.astimezone(zulu_tz)
    
    zulu_datetime_formatted = zulu_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return zulu_datetime_formatted

print(convert_cst_to_zulu(datetime.today()))


