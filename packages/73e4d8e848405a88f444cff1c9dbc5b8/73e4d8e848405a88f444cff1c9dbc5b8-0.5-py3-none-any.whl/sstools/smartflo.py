import requests
import json


class tata:
  
  def call_records(tata_auth_token,from_date="",to_date="",page="",limit=100,agents="",department="",call_type="",callerid="",destination="",direction="",duration="",operator="",services=""):

    url = "https://api-cloudphone.tatateleservices.com/v1/call/records"

    params = {
      "from_date":from_date,
      "to_date":to_date,
      "page":page,
      "limit":limit,
      "agents":agents,
      "department":department,
      "call_type":call_type,
      "callerid":callerid,
      "destination":destination,
      "direction":direction,
      "duration":duration,
      "operator":operator,
      "services":services
    }

    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': tata_auth_token
    }

    response = requests.request("GET", url, headers=headers, data=payload, params=params)

    res = json.loads(response.text)

    return res

