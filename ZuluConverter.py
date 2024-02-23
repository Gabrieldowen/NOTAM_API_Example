from datetime import datetime
from pytz import timezone

#   myDateTime: user's datetime input, date_format: desired datetime format, zone: desired time zone (ex: CST, EST, PST, MST, HST, AKST)
#   example call: time_converter("2024-02-22 08:30:00", "%Y-%m-%d %H:%M:%S", "EST")
def time_converter(myDateTime, date_format, zone):
    #Define time zones
    zulu_tz = timezone('UTC')                   # Coordinated Universal Time (Zulu)
    cst_tz = timezone('America/Chicago')        # Central Standard Time
    est_tz = timezone('America/New_York')       # Eastern Standard Time
    pst_tz = timezone('America/Los_Angeles')    # Pacific Standard Time
    mst_tz = timezone('America/Denver')         # Mountain Standard Time
    hst_tz = timezone('US/Hawaii')              # Hawaii Standard Time
    akst_tz = timezone('US/Alaska')             # Alaska Standard Time

    # Format date
    dateTimeFormatted = datetime.strptime(myDateTime, date_format)
  
    # Define timezones
    timezones = { "CST": cst_tz, "EST": est_tz, "PST": pst_tz, "MST": mst_tz, "HST": hst_tz, "AKST": akst_tz}

    tz = timezones.get(zone)
    if tz is None:
        print("Error: no desired time zone entered")
        return None
    
    # Localize input for converted datetime
    zoneMatch = tz.localize(dateTimeFormatted)
    

    # Convert the localizes datetime to Zulu time
    zulu_datetime = zoneMatch.astimezone(zulu_tz)
    # Format Zulu time
    zulu_datetime_formatted = zulu_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return zulu_datetime_formatted
