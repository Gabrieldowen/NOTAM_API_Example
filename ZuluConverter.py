from datetime import datetime
from pytz import timezone

#   myDateTime is user's input, zone is desired time zone (ex: CST, EST, PST, MST, HST, AKST)
def time_converter(myDateTime, zone):
    #Define time zones
    zulu_tz = timezone('UTC')                   # Coordinated Universal Time (Zulu)
    cst_tz = timezone('America/Chicago')        # Central Standard Time
    est_tz = timezone('America/New_York')       # Eastern Standard Time
    pst_tz = timezone('America/Los_Angeles')    # Pacific Standard Time
    mst_tz = timezone('America/Denver')         # Mountain Standard Time
    hst_tz = timezone('US/Hawaii')              # Hawaii Standard Time
    akst_tz = timezone('US/Alaska')             # Alaska Standard Time

    # Format date
    date_format = "%Y-%m-%d %H:%M:%S"
    dateTimeFormatted = datetime.strptime(myDateTime, date_format)

    # Match zone variable with desired timezone
    zoneMatch = ""

    # Localize input for converted datetime
    if(zone == "CST"):
        zoneMatch = cst_tz.localize(dateTimeFormatted)
    elif(zone == "EST"):
        zoneMatch = est_tz.localize(dateTimeFormatted)
    elif(zone == "PST"):
        zoneMatch = pst_tz.localize(dateTimeFormatted)
    elif(zone == "MST"):
        zoneMatch = mst_tz.localize(dateTimeFormatted)
    elif(zone == "HST"):
        zoneMatch = hst_tz.localize(dateTimeFormatted)
    elif(zone == "AKST"):
        zoneMatch = akst_tz.localize(dateTimeFormatted)
    else:
        print("Error: no desired time zone entered")

    # Convert the localizes datetime to Zulu time
    zulu_datetime = zoneMatch.astimezone(zulu_tz)
    # Format Zulu time
    zulu_datetime_formatted = zulu_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return zulu_datetime_formatted

