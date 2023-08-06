import requests
import json
import pandas as pd
from .common import *


# List of all lohono locations 
def lohono_locations():
  locations = ['india-alibaug','india-goa','india-lonavala','india-karjat']
  return locations

# lohono Search API wrapper
def lohono_search_api(location_slug="india-goa",page=1):
  url = "https://www.lohono.com/api/property"

  params = {
      'location_slug': location_slug,
      'page': page
  }

  payload = {}
  headers = {
    'authority': 'www.lohono.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json',
    'user-agent': mock_user_agent(),
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': f'https://www.lohono.com/villas/india/{ location_slug.split("-")[-1] }',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
  }


  response = requests.get(url, headers=headers, data = payload, params=params)

  search_data = json.loads(response.text.encode('utf8'))

  return search_data

# lohono listing API wrapper
def lohono_listing_api(slug='prop-villa-magnolia-p5sp'):
  url = f"https://www.lohono.com/api/property/{slug}"

  payload = {}
  headers = {
    'authority': 'www.lohono.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json',
    'user-agent':  mock_user_agent(),
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.lohono.com/villas/india/goa/prop-fonteira-vaddo-a-C6Cn',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
  }

  response = requests.get(url, headers=headers, data = payload)

  listing_data = json.loads(response.text.encode('utf8'))
  return listing_data['response']

# lohono Pricing API wrapper
def lohono_pricing_api(slug,checkin,checkout,adult=2,child=0):

  url = f"https://www.lohono.com/api/property/{slug}/price"

  payload = "{\"property_slug\":\""+slug+"\",\"checkin_date\":\""+str(checkin)+"\",\"checkout_date\":\""+str(checkout)+"\",\"adult_count\":"+str(adult)+",\"child_count\":"+str(child)+",\"coupon_code\":\"\",\"price_package\":\"\",\"isEH\":false}"

  headers = {
    'authority': 'www.lohono.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json',
    'user-agent': mock_user_agent(),
    'content-type': 'application/json',
    'origin': 'https://www.lohono.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': f'https://www.lohono.com/villas/india/goa/{slug}?checkout_date={checkout}&adult_count={adult}&checkin_date={checkin}',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  }

  response = requests.post(url, headers=headers, data = payload)
  pricing_data = json.loads(response.text.encode('utf8'))

  return pricing_data

# Basic details from the search API
def lohono_search(location_slugs=lohono_locations()):
  page = 1
  all_properties = []

  for location_slug in location_slugs:
    while True:
      print(f"page{ page } for {location_slug}")
      search_response = lohono_search_api(location_slug,page)
      all_properties.extend(search_response['response']['properties'])
      if search_response['paginate']['total_pages'] == page:
        break
      page += 1
      
  return pd.DataFrame(all_properties)

# All details for all the listings
def lohono_master_dataframe():
  search_data = lohono_search()

  slugs = search_data['property_slug'].values

  all_properties = []

  for slug in slugs:
    print(f"getting {slug}")
    listing_raw = lohono_listing_api(slug)
    all_properties.append(listing_raw)

  all_properties = pd.DataFrame(all_properties)

  all_properties['amenities'] = [[amenity['name'] for amenity in amenities] for amenities in all_properties['amenities']]
  all_properties['price'] = search_data['rate']
  all_properties['search_name'] = search_data['name']

  return all_properties
