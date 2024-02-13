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


#EST to Zulu
def convert_est_to_zulu(est_datetime):
    # Define time zones
    est_tz = timezone('America/New_York')    # Eastern Standard Time
    zulu_tz = timezone('UTC')   # Universal Time (Zulu)

    # Localize the input EST datetime
    localized_est = est_tz.localize(est_datetime)

    # Convert the localized EST datetime to Zulu time
    zulu_datetime = localized_est.astimezone(zulu_tz)

    zulu_datetime_formatted = zulu_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return zulu_datetime_formatted

print(convert_est_to_zulu(datetime.today()))

#PST to Zulu
def convert_pst_to_zulu(pst_datetime):
    pst_tz = timezone('America/Los_Angeles')    # Pacific Standard Time
    zulu_tz = timezone('UTC')   # Universal Time (Zulu)

    localized_pst = pst_tz.localize(pst_datetime)

    zulu_datetime = localized_pst.astimezone(zulu_tz)

    zulu_datetime_formatted = zulu_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return zulu_datetime_formatted

print(convert_pst_to_zulu(datetime.today()))

#MST to Zulu
def convert_mst_to_zulu(mst_datetime):
    mst_tz = timezone('America/Denver')     # Mountain Standard Time
    zulu_tz = timezone('UTC')   # Universal Time (Zulu)

    localized_mst = mst_tz.localize(mst_datetime)

    zulu_datetime = localized_mst.astimezone(zulu_tz)

    zulu_datetime_formatted = zulu_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return zulu_datetime_formatted

print(convert_mst_to_zulu(datetime.today()))

#HST to Zulu
def convert_hst_to_zulu(hst_datatime):
    hst_tz = timezone('US/Hawaii')     # Hawaii Standard Time
    zulu_tz = timezone('UTC')   # Universal Time (Zulu)

    localized_hst = hst_tz.localize(hst_datatime)

    zulu_datetime = localized_hst.astimezone(zulu_tz)

    zulu_datetime_formatted = zulu_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return zulu_datetime_formatted

print(convert_hst_to_zulu(datetime.today()))

#AKST to Zulu
def convert_akst_to_zulu(akst_datatime):
    akst_tz = timezone('US/Alaska')     # Alaska Standard Time
    zulu_tz = timezone('UTC')   # Universal Time (Zulu)

    localized_akst = akst_tz.localize(akst_datatime)

    zulu_datetime = localized_akst.astimezone(zulu_tz)

    zulu_datetime_formatted = zulu_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return zulu_datetime_formatted

print(convert_akst_to_zulu(datetime.today()))