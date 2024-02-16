from datetime import datetime
from pytz import timezone


    
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
