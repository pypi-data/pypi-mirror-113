import requests
import json
import pandas as pd
import datetime
from IPython.display import clear_output
import time
from sqlalchemy.exc import IntegrityError
import math
from .common import *



# Return list of all locations
def vista_locations():
  locations = ["lonavala, maharashtra",
  "goa, goa",
  "alibaug, maharashtra",
  "nainital, uttarakhand",
  "dehradun", "uttarakhand",
  "chail, himanchal-pradesh",
  "manali, himachal-pradesh",
  "shimla, himanchal%20pradesh",
  "ooty, tamil%20nadu",
  "coorg, karnataka",
  "dehradun, uttarakhand",
  "jaipur, rajasthan",
  "udaipur, rajasthan",
  "mahabaleshwar, maharashtra",
  "nashik, maharashtra",
  "gangtok, sikkim",
  "gurgaon, haryana",
  "vadodara, gujarat",
  "kashmir, jammu",
  ]

  return locations

# Wrapper on the search API
def vista_search_api(search_type='city',location="lonavala,%20maharashtra",checkin="",checkout="",guests=2,adults=2,childs=0,page_no=1):

  url = "https://searchapi.vistarooms.com/api/search/getresults"

  param={
    }

  payload = {
      
      "city": location,
      "search_type": "city",
      "checkin": checkin,
      "checkout": checkout,
      "total_guests": guests,
      "adults": adults,
      "childs": childs,
      "page": page_no,
      "min_bedrooms": 1,
      "max_bedrooms": 30,
      "amenity": [],
      "facilities": [],
      "price_start": 1000,
      "price_end": 5000000,
      "sort_by_price": ""
        
    }
  headers = {}

  response = requests.post(url, params=param, headers=headers, data=payload)
  search_data = json.loads(response.text.encode('utf8'))

  return search_data

# Wrapper on the listing API
def vista_listing_api(slug='the-boulevard-villa',guests=2,checkin=datetime.date.today()+datetime.timedelta(1), checkout=datetime.date.today()+datetime.timedelta(2),
                         guest=3,adult=3,child=0):
  
  url = "https://v3api.vistarooms.com/api/single-property"

  param={
          'slug': slug,
          'checkin': checkin,
          'checkout': checkout,
          'guest': guest,
          'adult': adult,
          'child': child    
      }

  payload = {}
  headers = {
  }

  response = requests.get(url, params=param, headers=headers, data = payload)
  property_deets = json.loads(response.text.encode('utf8'))
  return property_deets

# Wrapper on the listing extra details API
def vista_listing_other_details_api(id=107):

  url = "https://v3api.vistarooms.com/api/single-property-detail"

  param={
          'id': id,
      }

  payload = {}
  headers = {
  }
  
  response = requests.get(url, params=param, headers=headers, data = payload)
  property_other_deets = json.loads(response.text.encode('utf8'))
  return property_other_deets

# Wrapper on the price calculator
def vista_price_calculator_api(property_id='710', checkin=datetime.date.today()+datetime.timedelta(1), checkout = datetime.date.today()+datetime.timedelta(2), guest = 2, adult = 2, child = 0):

  if type(checkin)==str:
    checkin = datetime.datetime.strptime(checkin,'%Y-%m-%d')
    checkout = datetime.datetime.strptime(checkout,'%Y-%m-%d')


  url = "https://v3api.vistarooms.com/api/price-breakup"
  
  param={
      'property_id': property_id,
      'checkin': checkin,
      'checkout': checkout,
      'guest': guest,
      'adult': adult,
      'child': child,   
      }

  payload = {}
  headers = {
  }

  response = requests.get(url, params=param, headers=headers, data = payload)
  pricing_deets = json.loads(response.text.encode('utf8'))
  return pricing_deets

# Wrapper on the avalability (Blocked dates)

def vista_availability_api(property_id=119):
  url = "https://v3api.vistarooms.com/api/calendar/property/availability"

  params={
      "property_id":property_id
  }
  payload = {}
  headers = {
  }

  response = requests.get(url, headers=headers, data = payload, params=params)
  calendar = json.loads(response.text.encode('utf8'))
  return calendar



# Gives a json response for basic listing data for the list of locations
def vista_search_locations_json(locations=["lonavala,%20maharashtra"],guests=2,get_all=False,wait_time=10):

  # Empty list to append (extend) all the data
  properties = []

  if get_all:
    locations = vista_locations()

  # Outer loop - for each location
  for location in locations:

    try:

      page_no = 1

      # Inner Loop - for each page in location ( acc to the Vista Search API )
      while True:

        clear_output(wait=True)
        print(f"Page {page_no} for {location.split('%20')[0]} ")

        # Vista API call (search)
        search_data = vista_search_api(location=location,guests=guests,page_no=page_no)

        # Break when you reach the last page for a location
        if not 'data' in search_data.keys():
          break
        if not search_data['data']['properties']:
          break
          
        properties.extend(search_data['data']['properties'])
        page_no += 1

        time.sleep(wait_time)


    except:
      pass


  return properties

# Retruns a DATAFRAME for the above functions & **DROPS DUPLICATES (always use this for analysis)
def vista_search_locations(locations=["lonavala,%20maharashtra"],guests=2,get_all=False,wait_time=10):
  villas = vista_search_locations_json(locations=locations, guests=guests,get_all=get_all,wait_time=wait_time)
  villas = pd.DataFrame(villas)
  villas = villas.drop_duplicates('id')

  return villas

# Returns a JSON with the listing details
def vista_listing(slug='the-boulevard-villa',guests=2,checkin=datetime.date.today()+datetime.timedelta(1), checkout=datetime.date.today()+datetime.timedelta(2)):

  print("Fetching ",slug)
  # Vista API call (listing)
  property_deets = vista_listing_api(slug=slug,guests=guests,checkin=checkin, checkout=checkout)
  
  # Get lat and long (diff API call)
  lat_long = vista_listing_other_details_api(property_deets['data']['property_detail']['id'])['data']['location']

  # Get pricing for various durations
  weekday_pricing = vista_price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(),checkout=next_weekday()+datetime.timedelta(1))
  weekend_pricing = vista_price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(5),checkout=next_weekday(5)+datetime.timedelta(1))
  entire_week_pricing = vista_price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(),checkout=next_weekday()+datetime.timedelta(7))
  entire_month_pricing = vista_price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(),checkout=next_weekday()+datetime.timedelta(30))

  # Add the extra fields in response (JSON)
  property_deets['data']['slug'] = slug
  property_deets['data']['lat'] = lat_long['latitude']
  property_deets['data']['lon'] = lat_long['longitude']
  property_deets['data']['checkin_date'] = checkin
  property_deets['data']['checkout_date'] = checkout
  property_deets['data']['weekday_pricing'] = weekday_pricing
  property_deets['data']['weekend_pricing'] = weekend_pricing
  property_deets['data']['entire_week_pricing'] = entire_week_pricing
  property_deets['data']['entire_month_pricing'] = entire_month_pricing
  property_deets['data']['price_per_room'] = property_deets['data']['price']['amount_to_be_paid']/property_deets['data']['property_detail']['number_of_rooms']

  return property_deets['data']

# Calculates the price for a duration (if unavailable, will automatically look for the next available dates) % Recursive function
def vista_price_calculator(property_id, checkin=datetime.date.today()+datetime.timedelta(1), checkout = datetime.date.today()+datetime.timedelta(2), guest = 2, adult = 2, child = 0, depth=0):

  date_diff = (checkout-checkin).days

  # Set the exit condition for the recursion depth ( to avoid an endless recursion -> slowing down the scripts )
  if date_diff < 7:
    depth_lim = 15
    next_hop = 7
  elif date_diff >= 7 and date_diff < 29:
    depth_lim = 7
    next_hop = 7
  else:
    depth_lim = 5
    next_hop = date_diff
    
  if depth==depth_lim:
    return f"Villa Probably Inactive, checked till {checkin}"
  
  if type(checkin)==str:
    checkin = datetime.datetime.strptime(checkin,'%Y-%m-%d')
    checkout = datetime.datetime.strptime(checkout,'%Y-%m-%d')

  # Vista API call (Calculation)
  pricing = vista_price_calculator_api(property_id=property_id, checkin=checkin, checkout=checkout, guest=guest, adult=adult, child=child)

  if 'error' in pricing.keys():

    # Recursion condition (Call self with next dates in case the dates are not available)
    if pricing['error'] == 'Booking Not Available for these dates':

      next_checkin = checkin + datetime.timedelta(next_hop)
      next_chekout = checkout + datetime.timedelta(next_hop)

      next_pricing = vista_price_calculator(property_id,checkin=next_checkin ,checkout=next_chekout,depth=depth+1)
      return next_pricing

    # For other errors (Like invalid listing ID)
    else:
      return pricing['error']
      
    return next_pricing
  else:
    return pricing['data']['price']

# Uses a list of slugs to generate a master DATAFRAME , this contains literally everything, ideal for any analysis on Vista
def vista_master_dataframe(slugs=(['vista-greenwoods-five-villa','maison-calme-villa','vista-greenwoods-four-villa','mehta-mansion','villa-maira'])):
  
  total_slugs = len(slugs)
  temp_progress_counter = 0
  villas_deets = []   

  for slug in slugs:
    try:
      villa_deets = vista_listing(slug=slug)
      villas_deets.append(villa_deets)
      villas_df = pd.DataFrame(villas_deets)

      temp_progress_counter += 1
      clear_output(wait=True)
      print("Done ",int((temp_progress_counter/total_slugs)*100),"%")
    except:
      pass

  prop_detail_df = pd.DataFrame(list(villas_df['property_detail']))
  agent_details_df =  pd.DataFrame(list(villas_df['agent_details']))
  price_df =  pd.DataFrame(list(villas_df['price']))

  literally_all_deets = pd.concat([prop_detail_df,villas_df,price_df,agent_details_df], axis=1)

  literally_all_deets = literally_all_deets.drop(['property_detail','mini_gallery', 'base_url',
       'agent_details', 'house_rule_pdf', 'mini_gallery_text',
       'seo','number_extra_guest', 'additionalcost',
       'days', 'min_occupancy', 'max_occupancy', 'amount_to_be_paid','total_guest',
       'extra_adult', 'extra_child', 'extra_adult_cost', 'extra_child_cost',
       'per_person','price','checkin_date','checkout_date','total_price','agent_short_words'], axis = 1)
  
  literally_all_deets['amenities'] = [[amenity['name'] for amenity in amenities] for amenities in literally_all_deets['amenities']]
  literally_all_deets['weekday_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['weekday_pricing']]
  literally_all_deets['weekend_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['weekend_pricing']]
  literally_all_deets['entire_week_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['entire_week_pricing']]
  literally_all_deets['entire_month_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['entire_month_pricing']]
  
  return literally_all_deets

# Takes 2 lists of listings (Old and New) and only responds with the Dataframe of the newly added listings
def added_villas_dataframe(old_slugs,new_slugs):
  added_slugs = list(set(new_slugs).difference(set(old_slugs)))
  added_villas = []

  if added_slugs:
    added_villas = vista_master_dataframe(added_slugs) 

  return added_villas

# Non Desctructive SQL QUERY - Try "SELECT * FROM VISTA_MASTER"
def vista_sql_query(query,cypher_key):
  # Returns a daframe object of the query response
  myConnection = db_connection(cypher_key,database="vista")

  response_df = pd.io.sql.read_sql(query, con=myConnection)

  myConnection.close()

  return response_df



# DESTRCUTIVE sql query
def vista_sql_destructive(query,cypher_key):

  con = db_connection(cypher_key,database="vista")

  try:
    with con.cursor() as cur:
        cur.execute(query)
        con.commit()

  finally:
    con.close()

def vista_weekly_update_script(cypher_key,search_api_wait=10):

  # Get the list of all the current villas lited
  vista_search_data = vista_search_locations(get_all=True,wait_time=search_api_wait)

  new_slugs = vista_search_data['slug'].values

  query = "SELECT slug FROM VISTA_MASTER"

  old_slugs = vista_sql_query(query,cypher_key)
  old_slugs = old_slugs['slug'].values

  # Get the list of recently added and removed slugs
  added_slugs = list(set(new_slugs).difference(set(old_slugs)))
  removed_slugs = list(set(old_slugs).difference(set(new_slugs)))

  # Add the new listings to the Database
  vista_newly_added_df = added_villas_dataframe(old_slugs,new_slugs)
  vista_current_columns = vista_sql_query("SELECT * FROM VISTA_MASTER LIMIT 2",cypher_key).columns
  dropcols = set(vista_newly_added_df).difference(set(vista_current_columns))

  try:
    vista_newly_added_df.drop(dropcols,axis=1,inplace=True)
  except:
    pass


  if len(vista_newly_added_df) > 0:
      
      vista_newly_added_df['listing_status'] = "LISTED"
      vista_newly_added_df['status_on'] = datetime.datetime.today()
      vista_newly_added_df['created_on'] = datetime.datetime.today()

      # changind all the "Object" data types to str (to avoid some weird error in SQL)
      all_object_types = pd.DataFrame(vista_newly_added_df.dtypes)
      all_object_types = all_object_types[all_object_types[0]=='object'].index

      for column in all_object_types:
        vista_newly_added_df[column] = vista_newly_added_df[column].astype('str')

      #return vista_newly_added_df
      engine = db_connection(cypher_key,database="vista")

      for i in range(len(vista_newly_added_df)):
        try:
          vista_newly_added_df.iloc[i:i+1].to_sql(name='VISTA_MASTER',if_exists='append',con = engine,index=False)
        except IntegrityError:
          pass  
          
      engine.dispose()

      
  # Update listing Statuses
  vista_update_listing_status(cypher_key)



  # A Summary of the updates
  final_success_response = {
      "No of Added Villas" : len(added_slugs),
      "No of Removed Villas" : len(removed_slugs),
      "Added Villas" : added_slugs,
      "Removed Villas" : removed_slugs
  }

  return final_success_response



# Update listing status 
def vista_update_listing_status(cypher_key):

  get_ids_query ="SELECT id,listing_status FROM VISTA_MASTER"
  vista_data = vista_sql_query(get_ids_query,cypher_key)

  for id in vista_data[vista_data['listing_status']=='DELISTED']['id']:
    stat = vista_check_if_listed(id)
    print(id,stat)
    if stat:
      print("Updating database...")
      query = "UPDATE VISTA_MASTER SET listing_status='LISTED',status_on='"+str(datetime.datetime.today())+"'WHERE id='"+str(id)+"'"
      vista_sql_destructive(query,cypher_key)

  for id in vista_data[vista_data['listing_status']=='LISTED']['id']:
    stat = vista_check_if_listed(id)
    print(id,stat)
    if not stat:
      print("Updating database...")
      query = "UPDATE VISTA_MASTER SET listing_status='DELISTED',status_on='"+str(datetime.datetime.today())+"'WHERE id='"+str(id)+"'"
      vista_sql_destructive(query,cypher_key)

# Breadth first seach algorithm to get the blocked dates

def vista_blocked_dates(property_id,ci,co):

  # check if the listing is active

  lt_status = vista_check_status(property_id)
  if lt_status in ["INACTIVE","DELISTED"]:
    return {
        "id" : property_id,
        "blocked_dates" : lt_status
    }

  # rg = Range => checkout - checkin (in days)
  rg = (datetime.datetime.strptime(co, "%Y-%m-%d") - datetime.datetime.strptime(ci, "%Y-%m-%d")).days    

  api_calls = 0


  # This list contains all the date ranges to be checked - there will be additions and subtractions to this list
  DTE = [(ci,co,rg)]                  


  # we will add the blocekd dates here 
  blocked = {}                         
  explored = []


  while len(DTE) != 0:

    # To see how many API calls happened (fewer the better)
    api_calls += 1                        

    # Pick one item (date range) from the DTE list -> to see if it is available
    dates = DTE.pop()                     

    print(f"Checking : {dates[0]} for {dates[2]} days")

    explored.append(dates)

    checkin = dates[0]
    checkout = dates[1]
    range = dates[2]

    # Call the vista API to see of this is available
    api_response = vista_price_calculator_api(property_id=property_id,checkin=checkin,checkout=checkout)      


    # If no error -> it is available, start the next iteration of the loop
    if "error" not in api_response.keys():                      
      print("Not Blocked")
      continue

    # if the range is unavailable  do this
    else:   

      print("Blocked")

      # if the range is 1, mark the date as blocked
      if range == 1:                                                                 
        blocked[checkin] = api_response['data']['price']['amount_to_be_paid']
        #blocked.append((checkin,api_response['data']['price']['amount_to_be_paid']))
      
      # if the range is not 1, split the range in half and add both these ranges to the DTE list
      else:                                                                           
        checkin_t = datetime.datetime.strptime(checkin, "%Y-%m-%d")
        checkout_t = datetime.datetime.strptime(checkout, "%Y-%m-%d")

        middle_date = checkin_t + datetime.timedelta(math.ceil(range/2))

        first_half = ( str(checkin_t)[:10] , str(middle_date)[:10] , (middle_date - checkin_t).days )
        second_half = ( str(middle_date)[:10] , str(checkout_t)[:10] , (checkout_t - middle_date).days)

        DTE.extend([first_half,second_half])


  response_obj = {
      "id" : property_id,
      "blocked_dates" : blocked,
      "meta_data": {
          "total_blocked_dates" : len(blocked),
          "api_calls":api_calls,
          "checked from": ci,
          "checked till":co
          #"date_ranges_checked":explored
      }
  }

  return response_obj

# To check if the villa is inactive (Listed but blocked for all dates)
def vista_check_status(property_id="",slug=""):

  if vista_check_if_listed(property_id,slug):
    status = "LISTED"
  else:
    status = "DELISTED"
    return status

  if status == "LISTED":

    min_nights = 1

    for i in [8,16,32,64,128]:

      price = vista_price_calculator_api(property_id , checkin=datetime.date.today()+datetime.timedelta(i), checkout = datetime.date.today()+datetime.timedelta(i + min_nights))


      if "error" not in price.keys():
        return "LISTED"

      if i == 128:
        return "INACTIVE"

      elif price['error'] == 'Booking Not Available for these dates':
        pass

      elif isinstance(price['error'].split(" ")[4],int):
        min_nights = price['error'].split(" ")[4]
        pass

def vista_check_if_listed(property_id="",slug=""):

  if len(slug)>0:
    try:
      listing = vista_listing_api(slug)
      property_id = listing['data']['property_detail']['id']
    except: 
      return False

  price = vista_price_calculator_api(property_id , checkin=datetime.date.today()+datetime.timedelta(5), checkout = datetime.date.today()+datetime.timedelta(7))

  if "error" not in price.keys():
    return True

  elif isinstance(price['error'],str):
    return True

  elif 'property_id' in dict(price['error']).keys():
    return False

  return False

# Update listing status 

def vista_update_listing_status_old(cypher_key):

  get_ids_query ="SELECT id,listing_status FROM VISTA_MASTER"
  vista_data = vista_sql_query(get_ids_query,cypher_key)


  for id in vista_data[vista_data['listing_status']=='DELISTED']['id']:
    print(id)
    stat = vista_check_status(id)
    print(id,stat)
    if stat in ["LISTED","INACTIVE"]:
      print("Updating database...")
      query = "UPDATE VISTA_MASTER SET listing_status='"+stat+"',status_on='"+str(datetime.datetime.today())+"'WHERE id='"+str(id)+"'"
      vista_sql_destructive(query,cypher_key)

  for id in vista_data[vista_data['listing_status']=='LISTED']['id']:
    stat = vista_check_status(id)
    print(id,stat)
    if stat in ["DELISTED","INACTIVE"]:
      print("Updating database...")
      query = "UPDATE VISTA_MASTER SET listing_status='"+stat+"',status_on='"+str(datetime.datetime.today())+"'WHERE id='"+str(id)+"'"
      vista_sql_destructive(query,cypher_key)

  for id in vista_data[vista_data['listing_status']=='INACTIVE']['id']:
    stat = vista_check_status(id)
    print(id,stat)
    if stat in ["DELISTED","LISTED"]:
      print("Updating database...")
      query = "UPDATE VISTA_MASTER SET listing_status='"+stat+"',status_on='"+str(datetime.datetime.today())+"'WHERE id='"+str(id)+"'"
      vista_sql_destructive(query,cypher_key)


def vista_update_listing_status(cypher_key):


  get_ids_query ="SELECT id,listing_status FROM VISTA_MASTER"
  vista_data = vista_sql_query(get_ids_query,cypher_key)
    
  for i,r in vista_data.iterrows():

    try:
      old_status = r['listing_status']

      cal = vista_availability_api(r['id'])
    
      if "error" in cal.keys():
        current_status = "DELISTED"

      else:

        cal = pd.DataFrame(cal['data'])
        cal['date'] = cal['date'].astype('datetime64')

        if len(cal[cal['date']< datetime.datetime.today() + datetime.timedelta(90)])/88 > 1:
          current_status = "INACTIVE"


        else:
          current_status = "LISTED"

      if old_status != current_status:
        print(f"Updating database for {r['id']} - {current_status}...")
        query = f"UPDATE VISTA_MASTER SET listing_status='{current_status}',status_on='{str(datetime.datetime.today())}' WHERE id='{r['id']}'"
        #print(query)
        vista_sql_destructive(query,cypher_key)
      else:
        print(r['id'], "Unchanged")
      
    except:
      pass

"""# Lohono


```
# Lohono API wrappers
# Refining the APIs
# Master DataFrame
```


"""

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
