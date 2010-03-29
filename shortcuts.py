from __init__ import MozesApi

def moz_request(artist_id, phone, keyword):
    try:
        moz = {}
        moz['keyword'] = keyword
        moz['phone'] = "1" + phone.replace("-", "")
        response = moz
    except MobileAlert.DoesNotExist:
        response = False
    return response

def moz_check_status(profile, artist_id):
    moz = moz_request(artist_id, profile.sms_phone)
    if moz:
        return MozesApi().status(moz['phone'], moz['keyword'])
    return False
    
def moz_subscribe(profile, artist_id):
    moz = moz_request(artist_id, profile.sms_phone)
    if moz:
        return MozesApi().subscribe(moz['phone'], moz['keyword'])
    return False
    
def moz_unsubscribe(profile, artist_id):
    moz = moz_request(artist_id, profile.sms_phone)
    if moz:
        return MozesApi().unsubscribe(moz['phone'], moz['keyword'])
    return False
