#!/usr/bin/env python
# Demo script to add Sysdig service account in a team role
# W Embrey - IGXGlobal

# import the modules we need for this script
import requests
import json
import time
import calendar
import sys
import os


# import the variables from the config file
try:
    from config import *
except Exception as e:
    print('\nNo config file detected')


# declare vars from config file
def declare_variables():
    if bool(sysdig_url):
        print(f'Using host: {sysdig_url}')
    if bool(sysdig_apikey):
        print(f'Using sysdig_apikey: {sysdig_apikey}')
    if bool(team_id):
        print(f'Using team_id: {team_id}')
    if bool(team_role):
        print(f'Using team_role: {team_role}')
    if bool(name):
        print(f'Using Account name: {name}')

# set global variables
# you can leave these blank because we will check for them
spacer = ('-' * 100) + '\n'


def get_creds():
    # set the variables to global so we adjust the globals
    global sysdig_url
    global sysdig_apikey
    global customer_id
    global team_id
    global team_role
    global name
    
    
    # gather the hostname and credentials if they were not set
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
    return

def get_duration():
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
    return key_date

 
def create_account(url, key, name, team, role, date):
    apikey = ''
    
    #set the JSON payload
    json_payload = {
        "name": name,
        "teamRole": role,
        "systemRole": "ROLE_SERVICE_ACCOUNT",
        "teamId": team,
        "expirationDate": date
        }
    payload = json.dumps(json_payload)
    print(f'Payload: {json.dumps(json_payload)}')
    headers = {
      'Accept': 'application/json',
      'Authorization': 'Bearer ' + key,
      'Content-Type': 'application/json'
        }
      
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        
        response_json = json.loads(response.text)
        apikey = response_json["apiKey"]
        if bool(apikey):
            print(f'Service account key: {apikey}')
        else:
            print(f'Account creation failed: {response.text}')
        
    except Exception as e:
        print(f'\nFailed with error:\n{e}')
             
        
def main():
    os.system('clear')
    print(spacer)
    print("Sysdig service account creation POC tool - IGXGlobal ePlus\n")

    # Set the credentials
    declare_variables()
    get_creds()

    # Get the intended key duration
    key_expiry = get_duration()

    #create the account
    create_account(sysdig_url, sysdig_apikey, name, team_id, team_role, key_expiry)

    print(spacer)
    print('All done, closing script!')
    sys.exit()


if __name__ == "__main__":
    main()