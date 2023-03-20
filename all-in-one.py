#!/usr/bin/env python
# Demo script to add Sysdig service account in a team role
# All in one version without config file
# W Embrey - IGXGlobal

# import the modules we need for this script
import requests
import json
import time
import calendar
import sys
import os


os.system('clear')
print("Sysdig service account creation POC tool - IGXGlobal ePlus\n")


# add the variables below or they will be requested
sysdig_url = 'https://eu1.app.sysdig.com/api/serviceaccounts/team'
sysdig_apikey = 'abcdef12-3456-789a-bcde-f123456789ab'
team_id = '20001000'
team_role = 'ROLE_TEAM_STANDARD'
name = ''

# get the variables if not hard coded above
if not bool(sysdig_url):
    sysdig_url = input('Enter Sysdig URL from the GUI: ')
if not bool(sysdig_apikey):
    sysdig_apikey = input('Enter Sysdig API key: ')
if not bool(team_id):
    team_id = input('Enter the team ID for the service account: ')
if not bool(team_role):
    team_role = input('Enter team role ID for the service account: ')
if not bool(name):
    name = input('Enter account name for the service account: ')


# get the number of days for token validity
days_input = input('\nEnter the number of days for token validity or press enter to accept default 365: ')
if not bool(days_input):
    days = 365
else:
    try:
        days = int(days_input)
    except Exception as e:
        print(f'Invalid number. Error: {e}\nDefaulting to 365 days')
        days = 365
        
#work out key duration in seconds
key_life = days * 86400
key_expiry = key_life + calendar.timegm(time.gmtime())
print(f'\nKey set to expire: {time.ctime(key_expiry)}')
key_date = int(str(key_expiry) + '999')


 
#set the variable for the new account key
new_apikey = ''

#set the JSON payload
json_payload = {
    "name": name,
    "teamRole": team_role,
    "systemRole": "ROLE_SERVICE_ACCOUNT",
    "teamId": team_id,
    "expirationDate": key_date
    }
payload = json.dumps(json_payload)
print(f'Payload: {json.dumps(json_payload)}')
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer ' + sysdig_apikey,
  'Content-Type': 'application/json'
    }
 
#Try to create the account
try:
    response = requests.request("POST", sysdig_url, headers=headers, data=payload)
    
    response_json = json.loads(response.text)
    new_apikey = response_json["apiKey"]
    if bool(new_apikey):
        print(f'Service account key: {new_apikey}')
    else:
        print(f'Account creation failed: {response.text}')
    
except Exception as e:
    print(f'\nFailed with error:\n{e}')
             
        
def main():
    os.system('clear')
    print(spacer)
    print("Sysdig service account creation POC tool - IGXGlobal ePlus\n")
sys.exit()

