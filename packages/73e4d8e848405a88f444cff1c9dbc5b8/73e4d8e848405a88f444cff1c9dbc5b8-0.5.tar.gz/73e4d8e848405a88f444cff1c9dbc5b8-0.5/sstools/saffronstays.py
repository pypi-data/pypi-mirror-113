import requests
import json
import pandas as pd
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from .common import *



# SQL query on the SS database (ONLY SELECT) - returns a dataframe
def sql_query(query,cypher_key):

  myConnection = db_connection(cypher_key,database="main")

  if query.split(' ')[0] != 'SELECT':
    print("Error. Please only use non destructive (SELECT) queries.")
    return "Please only use non destructive (SELECT) queries."

  response_df = pd.io.sql.read_sql(query, con=myConnection)

  myConnection.close()

  return response_df


# to execute destructive queries 
def sql_query_destructive(query,cypher_key):

  con = db_connection(cypher_key,database="main")

  try:
    with con.cursor() as cur:
        cur.execute(query)
        con.commit()

  finally:
    con.close()



class dev:
  def sql_query(query,cypher_key):

    myConnection = db_connection(cypher_key,database="dev")
    response_df = pd.io.sql.read_sql(query, con=myConnection)
    myConnection.close()

    return response_df


  def sql_query_destructive(query,cypher_key):

    con = db_connection(cypher_key,database="dev")

    try:
      with con.cursor() as cur:
          cur.execute(query)
          con.commit()
    finally:
      con.close()

class aws: 
  def sql_query(query,cypher_key):

    myConnection = db_connection(cypher_key,database="main")

    if query.split(' ')[0] != 'SELECT':
      print("Error. Please only use non destructive (SELECT) queries.")
      return "Please only use non destructive (SELECT) queries."

    response_df = pd.io.sql.read_sql(query, con=myConnection)
    myConnection.close()

    return response_df

  # to execute destructive queries 
  def sql_query_destructive(query,cypher_key):

    con = db_connection(cypher_key,database="main")
    try:
      with con.cursor() as cur:
          cur.execute(query)
          con.commit()

    finally:
      con.close()



# Get the status for all the dates for a list of homes
def get_calendar(listing_ids,check_in,check_out):

  parsed_listing_ids = str(listing_ids)[1:-1]
  parsed_listing_ids = parsed_listing_ids.replace("'","").replace(" ","")

  url = "https://www.saffronstays.com/calender_node.php"

  params={
      "listingList": parsed_listing_ids,
      "checkIn":check_in,
      "checkOut":check_out
      
  }
  payload = {}
  headers= {}

  response = requests.get(url, headers=headers, data = payload,params=params)
  response = json.loads(response.text.encode('utf8'))
  return response



# SS Facebook catalogue (a list of currently live listings)
def ss_fb_catalogue():
  url = "https://www.saffronstays.com/items_catalogue.php"

  response = requests.get(url)
  response_data = response.text.encode('utf8')

  csv_endpoint = str(response_data).split('`')[1]
  csv_download_url = "https://www.saffronstays.com/"+csv_endpoint

  ss_data = pd.read_csv(csv_download_url)

  return ss_data



# list of emails and preheader names, update with yours
def sendgrid_email(TEMPLATE_ID,EMAILS,api_key,PAYLOAD={},from_email='book@saffronstays.com',from_name='SaffronStays'):
    """ Send a dynamic email to a list of email addresses

    :returns API response code
    :raises Exception e: raises an exception """
    # create Mail object and populate
    message = Mail(
        from_email=(from_email,from_name),
        to_emails=EMAILS
        )
    # pass custom values for our HTML placeholders
    message.dynamic_template_data = PAYLOAD

    message.template_id = TEMPLATE_ID
    # create our sendgrid client object, pass it our key, then send and return our response objects

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response code: {code}")
        print(f"Response headers: {headers}")
        print(f"Response body: {body}")
        print("Dynamic Messages Sent!")
        return str(response.status_code)

    except Exception as e:
        print("Error: {0}".format(e))
        return "Error: {0}".format(e)
