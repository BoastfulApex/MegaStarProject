from dotenv import load_dotenv
import json
import os
import requests
import urllib3
from datetime import date

load_dotenv()


def get_session_id():
    headers = {}
    url = 'https://212.83.191.99:50000/b1s/v2/Login'
    data = {
        'CompanyDB': str(os.getenv("SAP_COMPANY_DB")),
        'Password': str(os.getenv("SAP_PASSWORD")),
        'UserName': str(os.getenv("SAP_USERNAME"))
    }
    json_data = json.dumps(data)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.request("POST", url, headers=headers, data=json_data, verify=False).json()
    return response['SessionId']


def get_objects(url, session):
    url = f'https://212.83.191.99:50000/b1s/v2/{url}'

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    headers = {
        'SessionId': session,
        'Cookie': f'B1SESSION={session}; ROUTEID=.node1',
    }
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    response_data = response.json()
    return response_data


def categories():
    session = get_session_id()
    url = 'ItemGroups?$select=Number,GroupName'
    results = []
    while True:
        items = get_objects(url=url, session=session)
        results += [cat for cat in items['value']]
        if '@odata.nextLink' in items:
            url = items['@odata.nextLink']
        else:
            break
    return results


def sub_categories():
    session = get_session_id()
    url = 'U_U_SUBGROUP1'
    results = []
    while True:
        items = get_objects(url=url, session=session)
        results += [cat for cat in items['value']]
        if '@odata.nextLink' in items:
            url = items['@odata.nextLink']
        else:
            break

    return results


def manufacturers():
    session = get_session_id()
    url = 'Manufacturers'
    results = []
    while True:
        items = get_objects(url=url, session=session)
        results += [mans for mans in items['value']]
        if '@odata.nextLink' in items:
            url = items['@odata.nextLink']
        else:
            break

    return results


def clients():
    session = get_session_id()
    url = 'BusinessPartners?$select=CardCode,CardName,Phone1'
    results = []
    while True:
        items = get_objects(url=url, session=session)
        results += [user for user in items['value']]
        if '@odata.nextLink' in items:
            url = items['@odata.nextLink']
        else:
            break
    return results


def items():
    session = get_session_id()
    url = 'Items?$select=ItemCode,ItemName,ItemsGroupCode,U_Subgroup,Manufacturer,ItemPrices'
    results = []
    while True:
        items = get_objects(url=url, session=session)
        results += [item for item in items['value']]
        print(len(results))
        if '@odata.nextLink' in items:
            url = items['@odata.nextLink']
        else:
            break
    return results


def invoices():
    session = get_session_id()
    url = 'Invoices?$select=DocEntry,DocNum,DocDate,DocDueDate,CardCode,CardName,DocTotal,U_sumUZS,DiscountPercent,' \
          'DocumentLines'
    results = []
    while True:
        items = get_objects(url=url, session=session)
        results += [item for item in items['value']]
        if '@odata.nextLink' in items:
            url = items['@odata.nextLink']
        else:
            break
    return results


def get_top_products():
    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    session = get_session_id()

    url = f"sml.svc/TOP_SOLD_GOODSParameters(P_DateFrom='2021-04-01'," \
          f"P_DateTo='{formatted_date}')/TOP_SOLD_GOODS?$orderby=Quantity desc"

    return get_objects(url=url, session=session)


def get_kurs_valyuta():
    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    url = f"sml.svc/CURRENCIESParameters(P_Date='{formatted_date}')/CURRENCIES?$filter=Code eq 'UZS'"
    session = get_session_id()

    response_data = get_objects(url=url, session=session)
    return response_data['value'][0]['Rate']


def get_warehouses():
    session = get_session_id()
    url = 'Warehouses?'
    results = []
    while True:
        items = get_objects(url=url, session=session)
        results += [item for item in items['value']]
        if '@odata.nextLink' in items:
            url = items['@odata.nextLink']
        else:
            break
    return results
