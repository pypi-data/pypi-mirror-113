import pandas as pd
import datetime
from cryptography.fernet import Fernet
import pymysql
import random
import math

# Universal fn to establish a connection to the database (SQL)
def db_connection(cypher_key,database="main"):

  key = bytes(cypher_key,'utf-8')
  cipher_suite = Fernet(key)

  if database=="main":
    host_enc = b'gAAAAABgU5NFdPLwUewW-ljzzPKpURLo9mMKzOkClVvpWYotYRT6DsmgNlHYUKP8X3m_c12kAUqSrLw4KTlujTPly2F-R-CFrw=='
    user_enc = b'gAAAAABf-DB2YcOMC7JvsL-GihLJcImh6DvJpt1hNZFetiCzxMacK4agYHkyl3W1mnRkHNmEnecp4mMPZRfqO6bsLP1qgrpWbA=='
    pass_enc = b'gAAAAABf-DCFqT2kj-ExcdPn2IW0m0-M_3piK2-w1xNpUvH21XDsz3iqixvrT-NxKnpf1wirp0NcYoQEGt4TKpYHJzXcrXy6TA=='
    database_enc = b'gAAAAABfQPr48Sej-V7GarivuF4bsfBgP9rldzD500gl174HK4LZy70VfEob-kbaOBFa8rhuio_PbCFj4Nt3nJzVjKqC83d1NA=='

  elif database=="vista":
    host_enc = b'gAAAAABfQPr4eF5i5aU4vfC4RieOdLr9GjwQPWWmvTWT728cK-qUoPesPZmLKwE4vTkhh3oxCmREfrHN1omRwmxJJuo_CS4cMmRKG8_mLFIBQG1mg2Kx102PixJAdf1l74dhO6VI8ZCR'
    user_enc = b'gAAAAABfQPr4PssChqSwFRHAGwKGCrKRLvnjRqfBkrazUydFvX3RBNAr5zAvKxdGJtaemdjq3uRwk1kgY4tLpIO9CxXj_JdC0w=='
    pass_enc = b'gAAAAABfQPr4iwH0c5pxjI4XfV-uT-pBt9tKfQgFJEfjTcTIjwipeN4tI_bG-TtHoamosKEuFOldevYPi-3usIj1ZDSrb-zsXg=='
    database_enc = b'gAAAAABgU5oarKoMuMj5EYPHf59SSfalqJ1_vtsGjbk4Gepefkr5dhTnZg1KVSmt6Rln02B5SOJf-N9dzbA6Q47uJbZ-xNrJdQ=='

  elif database=="dev":
    host_enc = b'gAAAAABgU5RRIJqGSTQhaupb_rwblmtCTjl6Id6fa1JMsZQac6i9eaUtoBoglK92yuSCGiTaIadtjrwxmK5VMS2cM6Po-SWMpQ=='
    user_enc = b'gAAAAABgU5QmKmvNsS7TC2tz66e3S40CSiNF8418N6ANGFn6D_RhP8fd4iQRML3uk9WnDlDAtYHpGjstwgpKH8YJ347xZHQawA=='
    pass_enc = b'gAAAAABgU5Rf1piAvyT_p5LRd0YJheFT2Z9W75R4b2MUA1o1-O4Vn2Xw7R-1bWLx4EhYUrRZ6_ajI8DCgLVULZZdVSWxG6OvCw=='
    database_enc = b'gAAAAABgU5SLKYwupyp_nrcSzGYcwDkkKKxGjmvEpULZV2MmKGDgXCefa2WvINUBrCCmBeyt9GcpzBQQSE9QN8azsDSItdTa5Q=='
  
  else:
    raise ValueError("Invalid Database, pick either of the 3 - ('main','dev','vista')")

  myServer = cipher_suite.decrypt(host_enc).decode("utf-8")
  myUser = cipher_suite.decrypt(user_enc).decode("utf-8")
  myPwd = cipher_suite.decrypt(pass_enc).decode("utf-8")
  db = cipher_suite.decrypt(database_enc).decode("utf-8")

  myConnection = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db)

  return myConnection



"""# Helper Functions


```
next_weekday()
mock_user_agent()
mock_proxy()
earth_distance(lat1,lon1,lat2,lon2)
```


"""

# Get the next weekday ( 0=monday , 1 = tuesday ... )
def next_weekday(weekday=0, d=datetime.date.today()):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

# default - next monday

# gives a random user-agent to use in the API call
def mock_user_agent():
  users = ["Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
  "Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00",
  "Opera/9.60 (Windows NT 6.0; U; en) Presto/2.1.1",
  "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
  "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)"]

  return users[random.randint(0,7)]

# Gives a 'proxies' object for a 'requests' call
def mock_proxy():

  proxies_list = ["45.72.30.159:80",
  "45.130.255.156:80",
  "193.8.127.117:80",
  "45.130.255.147:80",
  "193.8.215.243:80",
  "45.130.125.157:80",
  "45.130.255.140:80",
  "45.130.255.198:80",
  "185.164.56.221:80",
  "45.136.231.226:80"]

  proxy = proxies_list[random.randint(0,9)]

  proxies = {
  "http": proxy,
  "https": proxy
  }

  return proxies

# Arial distance between 2 pairs of coordinates 
def earth_distance(lat1,lon1,lat2,lon2):

  # Radius of the earth
  R = 6373.0

  lat1 = math.radians(lat1)
  lon1 = math.radians(lon1)
  lat2 = math.radians(lat2)
  lon2 = math.radians(lon2)

  dlon = lon2 - lon1
  dlat = lat2 - lat1

  #Haversine formula
  a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  
  distance = R * c

  return distance

def to_fancy_date(date):
  tmstmp = pd.to_datetime(date)
  day = tmstmp.day
  
  if 4 <= day <= 20 or 24 <= day <= 30:
      suffix = "th"
  else:
      suffix = ["st", "nd", "rd"][day % 10 - 1]

  return f"{tmstmp.day}{suffix} {tmstmp.month_name()} {tmstmp.year}"
