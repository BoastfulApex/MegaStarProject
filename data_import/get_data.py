from dotenv import load_dotenv
import json
import os
import requests
import urllib3

load_dotenv()
  
def get_session_id():
    headers = {}
    url = 'https://212.83.152.252:50000/b1s/v2/Login'
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
    url = f'https://212.83.152.252:50000/b1s/v2/{url}'

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
        if '@odata.nextLink'in items:
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
        if '@odata.nextLink'in items:
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
        if '@odata.nextLink'in items:
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
        if '@odata.nextLink'in items:
            url = items['@odata.nextLink']
        else:
            break
    return results


def items():
    session = get_session_id()
    url = 'Items?$select=ItemCode,ItemName,ItemsGroupCode,U_Subgroup,Manufacturer'
    results = []
    while True:
        items = get_objects(url=url, session=session)
        results += [item for item in items['value']]
        if '@odata.nextLink'in items:
            url = items['@odata.nextLink']
        else:
            break   
    return results


def invoices():
    session = get_session_id()
    url = 'Invoices?$select=DocEntry,DocNum,DocDate,DocDueDate,CardCode,CardName,DocTotal,U_sumUZS,DiscountPercent,DocumentLines'
    results = []
    while True:
        items = get_objects(url=url, session=session)
        results += [item for item in items['value']]
        print()
        if '@odata.nextLink'in items:
            url = items['@odata.nextLink']
        else:
            break   
    return results
