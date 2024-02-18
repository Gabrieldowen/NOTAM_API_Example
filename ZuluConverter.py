from datetime import datetime
from pytz import timezone

#   myDateTime is user's input, zone is desired time zone (ex: CST, EST, PST, MST, HST, AKST)
def time_converter(myDateTime, zone):
    #Define time zones
    zulu_tz = timezone('UTC')                   # Coordinated Universal Time (Zulu)
    cst_tz = timezone('America/Chicago')        # Central Standard Time
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

    
def convert_cst_to_zulu(cst_datetime):
    # Define time zones
    cst_tz = timezone('America/Chicago')  # Central Standard Time
    zulu_tz = timezone('UTC')  # Coordinated Universal Time (Zulu)
    date_format = "%Y-%m-%d %H:%M:%S"
    cst = datetime.strptime(cst_datetime, date_format)
    # Localize the input CST datetime
    localized_cst = cst_tz.localize(cst)
    
    # Convert the localized CST datetime to Zulu time
    zulu_datetime = localized_cst.astimezone(zulu_tz)
    
    zulu_datetime_formatted = zulu_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return zulu_datetime_formatted




#EST to Zulu
def convert_est_to_zulu(est_datetime):
    # Define time zones
    est_tz = timezone('America/New_York')    # Eastern Standard Time
    zulu_tz = timezone('UTC')   # Universal Time (Zulu)
    date_format = "%Y-%m-%d %H:%M:%S"
    est = datetime.strptime(est_datetime, date_format)
    # Localize the input EST datetime
    localized_est = est_tz.localize(est)

    # Convert the localized EST datetime to Zulu time
    zulu_datetime = localized_est.astimezone(zulu_tz)

    zulu_datetime_formatted = zulu_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return zulu_datetime_formatted


#PST to Zulu
def convert_pst_to_zulu(pst_datetime):
    pst_tz = timezone('America/Los_Angeles')    # Pacific Standard Time
    zulu_tz = timezone('UTC')   # Universal Time (Zulu)
    date_format = "%Y-%m-%d %H:%M:%S"
    pst = datetime.strptime(pst_datetime, date_format)
    localized_pst = pst_tz.localize(pst)

    zulu_datetime = localized_pst.astimezone(zulu_tz)

    zulu_datetime_formatted = zulu_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return zulu_datetime_formatted



#MST to Zulu
def convert_mst_to_zulu(mst_datetime):
    mst_tz = timezone('America/Denver')     # Mountain Standard Time
    zulu_tz = timezone('UTC')   # Universal Time (Zulu)
    date_format = "%Y-%m-%d %H:%M:%S"
    mst = datetime.strptime(mst_datetime, date_format)
    localized_mst = mst_tz.localize(mst)

    zulu_datetime = localized_mst.astimezone(zulu_tz)

    zulu_datetime_formatted = zulu_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return zulu_datetime_formatted


#HST to Zulu
def convert_hst_to_zulu(hst_datatime):
    hst_tz = timezone('US/Hawaii')     # Hawaii Standard Time
    zulu_tz = timezone('UTC')   # Universal Time (Zulu)
    date_format = "%Y-%m-%d %H:%M:%S"
    hst = datetime.strptime(hst_datatime, date_format)
    localized_hst = hst_tz.localize(hst)

    zulu_datetime = localized_hst.astimezone(zulu_tz)

    zulu_datetime_formatted = zulu_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return zulu_datetime_formatted



#AKST to Zulu
def convert_akst_to_zulu(akst_datatime):
    akst_tz = timezone('US/Alaska')     # Alaska Standard Time
    zulu_tz = timezone('UTC')   # Universal Time (Zulu)
    date_format = "%Y-%m-%d %H:%M:%S"
    akst = datetime.strptime(akst_datatime, date_format)
    localized_akst = akst_tz.localize(akst)

    zulu_datetime = localized_akst.astimezone(zulu_tz)

    zulu_datetime_formatted = zulu_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return zulu_datetime_formatted
