import requests
import json
import pandas as pd
import datetime
from .common import *

"""# AirBnb"""

airbnb_home_types = ['Entire home apt','Hotel room','Private room', 'Shared room']

airbnb_imp_amenities = [5,4,16,7,9,12]
#AC, Wifi , Breakfast, Parking, Pool, Pets  (Not in order)

# Airbnb Search API
def airbnb_search_api(place_id = "ChIJRYHfiwkB6DsRWIbipWBKa2k", city = "", state = "", min_price = 4000, max_price=50000, min_bedrooms=1, home_type=airbnb_home_types, items_per_grid = 50, amenities = [], items_offset = 0):

  home_type = [item.replace(" ","%20") for item in home_type]
  home_type = ["Entire%20home%2Fapt" if x=="Entire%20home%20apt" else x for x in home_type]
  home_type_filter = "%22%2C%22".join(home_type)

  amenities = [str(item) for item in amenities]
  amenities_filter = "%2C".join(amenities)  

  url = f"https://www.airbnb.co.in/api/v3/ExploreSearch?locale=en-IN&operationName=ExploreSearch&currency=INR&variables=%7B%22request%22%3A%7B%22metadataOnly%22%3Afalse%2C%22version%22%3A%221.7.8%22%2C%22itemsPerGrid%22%3A{items_per_grid}%2C%22tabId%22%3A%22home_tab%22%2C%22refinementPaths%22%3A%5B%22%2Fhomes%22%5D%2C%22source%22%3A%22structured_search_input_header%22%2C%22searchType%22%3A%22filter_change%22%2C%22mapToggle%22%3Afalse%2C%22roomTypes%22%3A%5B%22{home_type_filter}%22%5D%2C%22priceMin%22%3A{min_price}%2C%22priceMax%22%3A{max_price}%2C%22placeId%22%3A%22{place_id}%22%2C%22itemsOffset%22%3A{items_offset}%2C%22minBedrooms%22%3A{min_bedrooms}%2C%22amenities%22%3A%5B{amenities_filter}%5D%2C%22query%22%3A%22{city}%2C%20{state}%22%2C%22cdnCacheSafe%22%3Afalse%2C%22simpleSearchTreatment%22%3A%22simple_search_only%22%2C%22treatmentFlags%22%3A%5B%22simple_search_1_1%22%2C%22oe_big_search%22%5D%2C%22screenSize%22%3A%22large%22%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22274161d4ce0dbf360c201612651d5d8f080d23820ce74da388aed7f9e3b00c7f%22%7D%7D"
  #url = f"https://www.airbnb.co.in/api/v3/ExploreSearch?locale=en-IN&operationName=ExploreSearch&currency=INR&variables=%7B%22request%22%3A%7B%22metadataOnly%22%3Afalse%2C%22version%22%3A%221.7.8%22%2C%22itemsPerGrid%22%3A20%2C%22roomTypes%22%3A%5B%22Entire%20home%2Fapt%22%5D%2C%22minBedrooms%22%3A0%2C%22source%22%3A%22structured_search_input_header%22%2C%22searchType%22%3A%22pagination%22%2C%22tabId%22%3A%22home_tab%22%2C%22mapToggle%22%3Afalse%2C%22refinementPaths%22%3A%5B%22%2Fhomes%22%5D%2C%22ib%22%3Atrue%2C%22amenities%22%3A%5B4%2C5%2C7%2C9%2C12%2C16%5D%2C%22federatedSearchSessionId%22%3A%22e597713a-7e46-4d10-88e7-3a2a9f15dc8d%22%2C%22placeId%22%3A%22ChIJM6uk0Jz75zsRT1nlkg6PwiQ%22%2C%22itemsOffset%22%3A20%2C%22sectionOffset%22%3A2%2C%22query%22%3A%22Karjat%2C%20Maharashtra%22%2C%22cdnCacheSafe%22%3Afalse%2C%22simpleSearchTreatment%22%3A%22simple_search_only%22%2C%22treatmentFlags%22%3A%5B%22simple_search_1_1%22%2C%22oe_big_search%22%5D%2C%22screenSize%22%3A%22large%22%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22274161d4ce0dbf360c201612651d5d8f080d23820ce74da388aed7f9e3b00c7f%22%7D%7D"

  payload = {}
  headers = {
    'authority': 'www.airbnb.co.in',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'device-memory': '4',
    'x-airbnb-graphql-platform-client': 'apollo-niobe',
    #'x-csrf-token': 'V4$.airbnb.co.in$lHdA3kStJv0$yEvcPM_C6eeUUHkQuYEdGFWrZreA5ui1e4A-pMzDFI=',
    'x-airbnb-api-key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20',
    'x-csrf-without-token': '4',
    'user-agent': mock_user_agent(),
    'viewport-width': '1600',
    'content-type': 'application/json',
    'accept': '*/*',
    'dpr': '1',
    'ect': '4g',
    'x-airbnb-graphql-platform': 'web',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    # 'referer': f'https://www.airbnb.co.in/s/{city}--{state}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&adults=2&source=structured_search_input_header&search_type=filter_change&map_toggle=false&room_types%5B%5D=Entire%20home%2Fapt&price_min=4221&place_id={place_id}',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  }

  response = requests.get(url, headers=headers, data = payload)
  
  #response = json.loads(response.text.encode('utf8'))

  return response

# Airbnb Calendar API
def airbnb_calendar_api(listing_id,start_month=9,start_year=2020,bev='1600684519_NDg5ZGY1ZDQ4YjNk',month_count=4):
  url = f"https://www.airbnb.co.in/api/v3/PdpAvailabilityCalendar?operationName=PdpAvailabilityCalendar&locale=en-IN&currency=INR&variables=%7B%22request%22%3A%7B%22count%22%3A{month_count}%2C%22listingId%22%3A%22{listing_id}%22%2C%22month%22%3A{start_month}%2C%22year%22%3A{start_year}%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22b94ab2c7e743e30b3d0bc92981a55fff22a05b20bcc9bcc25ca075cc95b42aac%22%7D%7D"

  payload = {}
  headers = {
    'authority': 'www.airbnb.co.in',
    #'pragma': 'no-cache',
    #'cache-control': 'no-cache',
    #'device-memory': '8',
    'x-airbnb-graphql-platform-client': 'minimalist-niobe',
    #'x-csrf-token': 'V4$.airbnb.co.in$lHdA3kStJv0$yEvcPMB_C6eeUUHkQuYEdGFWrZreA5ui1e4A-pMzDFI=',
    'x-airbnb-api-key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20',
    #'x-csrf-without-token': '1',
    'user-agent': mock_user_agent(),
    'viewport-width': '1600',
    'content-type': 'application/json',
    'accept': '*/*',
    'dpr': '1',
    'ect': '4g',
    'x-airbnb-graphql-platform': 'web',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': f'https://www.airbnb.co.in/rooms/{listing_id}?adults=2&source_impression_id=p3_1598719581_vge1qn5YJ%2FXWgUKg&check_in=2020-10-01&guests=1',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cookie': f'bev={bev};'
  }

  response = requests.request("GET", url, headers=headers, data = payload)
  response = json.loads(response.text.encode('utf8'))

  return response

#Airbnb search DataFrame
def airbnb_search(place_ids = ["ChIJRYHfiwkB6DsRWIbipWBKa2k"], max_iters = 5, min_price=4000,max_price=200000, home_type=[],amenities=[], min_bedrooms=1 ):

  all_items = []

  for place_id in place_ids:

    counter = 1

    offset = 0

    while counter<=max_iters:  

      print(f"Round {counter} for {place_id}")
      counter+=1

      response = airbnb_search_api(place_id = place_id, min_price = min_price ,max_price=max_price, min_bedrooms=min_bedrooms,home_type=home_type,amenities=amenities, items_offset = offset)
      offset += 50

      if not response['data']['dora']['exploreV3']['sections']:
        break

      else:
        for sections in response['data']['dora']['exploreV3']['sections']:
          if 'listing' in sections['items'][0].keys():
            all_items.extend(sections['items'])


  items_df = pd.DataFrame([item['listing'] for item in all_items])
  prices_df = pd.DataFrame([item['pricingQuote'] for item in all_items])
  items_df[['canInstantBook','weeklyPriceFactor','monthlyPriceFactor','priceDropDisclaimer','priceString','rateType']] = prices_df[['canInstantBook','weeklyPriceFactor','monthlyPriceFactor','priceDropDisclaimer','priceString','rateType']]
  return_obj = items_df[['id','name','roomAndPropertyType','reviews','avgRating','starRating','reviewsCount','amenityIds','previewAmenityNames','bathrooms','bedrooms','city','lat','lng','personCapacity','publicAddress','pictureUrl','pictureUrls','isHostHighlyRated','isNewListing','isSuperhost','canInstantBook','weeklyPriceFactor','monthlyPriceFactor','priceDropDisclaimer','priceString','rateType']]
  return_obj = return_obj.drop_duplicates('id')

  return return_obj

# Airbnb Calendar DataFrame
def airbnb_calendar(listing_id,start_month=datetime.datetime.today().month,start_year=datetime.datetime.today().year):

  api_response = airbnb_calendar_api(listing_id,start_month,start_year)

  all_months = [month['days'] for month in api_response['data']['merlin']['pdpAvailabilityCalendar']['calendarMonths']]

  all_days=[]

  for month in all_months:
    all_days.extend(month)

  all_days = pd.DataFrame(all_days)
  all_days['price'] = [item['localPriceFormatted'][1:].replace(",","") for item in all_days['price'].values]

  all_days['calendarDate'] = pd.to_datetime(all_days['calendarDate'])

  all_days['listing_id'] = listing_id

  all_days = all_days.astype({'price':'int32'})

  return all_days

# Get Occupancy data for a listing id
def airbnb_occupancy(listing_id):
  clndr = airbnb_calendar(listing_id=listing_id,start_month=datetime.datetime.today().month,start_year=datetime.datetime.today().year)

  clndr = clndr.set_index('calendarDate')

  clndr_monthly = clndr.groupby(pd.Grouper(freq='M')).mean()

  clndr_monthly['month-year'] = [str(item.month_name())+" "+str(item.year) for item in clndr_monthly.index]

  clndr_monthly = clndr_monthly.set_index('month-year')

  clndr_monthly['occupancy'] = 1-clndr_monthly['available']

  occupancy = clndr_monthly['occupancy'].to_json()
  available = clndr[clndr['available']==True].index
  blocked = clndr[clndr['available']==False].index

  available = [str(item.date()) for item in available]
  blocked = [str(item.date()) for item in blocked]

  return_obj = {
      "listing_id": listing_id,
      "monthly_occupancy" : occupancy,
      "blocked_dates" : blocked,
      "available_dates": available
  }

  return return_obj

