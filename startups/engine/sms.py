import kavenegar
import requests
import re
import threading

key = '2F417954435A6C766E783236736D414A3231316F33586C45453979344D707047'

def validate_mobile_number(mobile):
    regex = re.compile(r'^(\+\d{1,3}[- ]?)?\d{11}$', re.I)
    valid_mobile = regex.search(mobile)
    if valid_mobile:
        return valid_mobile.group(0)
    else:
        return False


def single_sms(text, mobile, template):
    valid_mobile = validate_mobile_number(mobile)

    if valid_mobile:
        try:
            url = f'https://api.kavenegar.com/v1/{key}/verify/lookup.json'
            params = {
                'receptor': valid_mobile,
                'token': text,
                'template': template,
            }

            sms_response = requests.get(url=url, params=params)
            print(sms_response.url)
        except Exception as e:
            print(e)
            return False
        return True
    return False



def sms(text, mobile, template):
    thread = threading.Thread(target=single_sms, args=(text, mobile, template, )).start()
    return True