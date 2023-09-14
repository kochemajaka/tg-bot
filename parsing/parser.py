import time
import requests


def parse_type_gibdd(vin, request_type, checktype, headers):
    url = "ht   tps://xn--b1afk4ade.xn--90adear.xn--p1ai/proxy/check/auto/"
    try:
        request = requests.post(url + request_type, data={"vin": vin, "checkType": checktype}, headers=headers)
    except Exception as error:
        print("Invalid Response")
        # print(error)
        print(url + request_type)
        return {}
    for i in range(2):
        if request.status_code != 500:
            break
        time.sleep(1)
    if request.status_code == 500:
        print(request.text)
        return {}
    try:
        type_json = request.json()
    except Exception as error:
        print("invalid json", request.text, error, sep="\n\n")
        return {}
    print(request_type)
    for value in type_json.values():
        if not isinstance(value, list):
            continue
        return value or {}
    return {}


def parse_gibdd(vin="WAUYP64B01N141245"):
    url = "https://xn--b1afk4ade.xn--90adear.xn--p1ai/proxy/check/auto/"
    check_types = {
        "dtp": "dtp",
        "wanted": "wanted",
        "restrict": "restricted",
        "diagnostic": "diagnostic"
    }
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.5.810 Yowser/2.5 Safari/537.36"
    }
    full_information = {}

    try:
        history_request = requests.post(url + "history", data={"vin": vin, "checkType": "history"}, headers=headers)
    except Exception as error:
        print("Invalid Response")
        print(error)
    for i in range(2):
        if history_request.status_code != 500:
            break
        time.sleep(1)

    if history_request.status_code == 500:
        full_information['ownershipPeriods'] = {}
        full_information["vehicle"] = {}
    else:

        try:
            history_json = history_request.json()
        except Exception as error:
            print("invalid json", history_request.text, error, sep="\n\n")

        try:
            if history_json["RequestResult"]["ownershipPeriods"]["ownershipPeriod"]:
                full_information["ownershipPeriods"] = history_json["RequestResult"]["ownershipPeriods"]["ownershipPeriod"]
        except KeyError:
            print(history_request.text)
            full_information["ownershipPeriods"] = {}

        # vehicle information
        try:
            if history_json["RequestResult"]["vehicle"]:
                full_information["vehicle"] = history_json["RequestResult"]["vehicle"]
        except KeyError:
            print(history_request.text)
            full_information["vehicle"] = {}

    # dtp information
    # restrict information
    # wanted information
    # diagnostic information

    for request_type, check_type in check_types.items():
        time.sleep(1)
        full_information[request_type] = parse_type_gibdd(vin, request_type, check_type, headers)

    return full_information

    # print(full_information)


def parse_rsa(vin="WAUYP64B01N141245"):
    url = "https://api-cloud.ru/api/rsa.php"

    headers = {"type": "osago",
               "token": "87fcabe45fae4df6793757c2cb2ab0cf"}
    if len(vin) == 17:
        headers["vin"] = vin
    else:
        headers["regNumber"] = vin

    exceptions = ["brandmodel", "power"]

    request = requests.get(url, headers=headers)

    re_json = request.json()
    if re_json["count"] == 0:
        print(vin, re_json["message"], sep="--\n--\n", end="-"*70)
        raise Exception

    info = re_json["rez"][0]
    for exception in exceptions:
        info.pop(exception)
    print("rsa")
    return info

# print(parse_gibdd("VF7RCRFJC76658482"))
# print("\n\n")
# print(parse_gibdd())
