from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

#=======================================================================
#time formating functions. Changes the wacky HD time format to 24-hour 
# then mixed with date for iso
#========================================================================
def apTo24Hour(time):
    #if a time does not have 4 digits add a zero to front
    if len(time)<6:
        time = "0"+time
    #if hour is midnight (which it won't be) hour is 00
    if(time[-1:] == 'a' and time[:2]=="12"):
        return "00"+time[2:-1]
    #remove am and leave as is
    elif(time[-1] == 'a'):
        return time[:-1]
    #check if noon
    elif(time[-1]=='p' and time[:2] =="12"):
        return time[:-1]
    #otherwise add 12 hours and remove pm
    else:
        return str(int(time[:(time.find(':'))])+12) + time[time.find(':'):-1]
    
def makeISO8601(date,time,year="2020"):
    time = apTo24Hour(time)
    iso = year+'-'+date[:2]+'-'+date[3:]+'T'+time[:2]+':'+time[3:]+':'+"00"
    return iso

#==============================================================================
#MAIN
#==============================================================================

def main():
    #THIS IS BASIC STUFF TO LINK THE CALENDER
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #END BASIC IMPORTANT STUFF I DON'T UNDERSTAND
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!





    #Open up the workdays.json file that holds all the workday data
    with open('workdays.json') as f:
        data = json.load(f)
    #load that data into the mydata variable
    mydata = json.loads(data)

    for day in mydata:
        #Variables that will be filled by bot
        DATE = day["date"]
        START_TIME = day["start_time"]
        END_TIME = day["end_time"]
        LUNCH = day["lunch"]
        print(makeISO8601(DATE,START_TIME))
        print(makeISO8601(DATE,END_TIME))
        NOTIFICATION_BUFFER = 30        #minutes

        #Create the event object to be added to calender
        event = {
        'summary': 'Work',
        'location': 'Home Depot',
        'description': "Lunch? "+str(LUNCH),
        'start': {
            'dateTime': makeISO8601(DATE, START_TIME),    #StartDateTimeHERE
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': makeISO8601(DATE, END_TIME),    #EndDateTimeHERE
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [
        ],
        'attendees': [
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'popup', 'minutes': NOTIFICATION_BUFFER}, #30 minutes popup reminder before shift starts
            ],
        },
        }

        print('Posting Event')
        event = service.events().insert(calendarId='primary', body=event).execute()
        print ('Event created: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    main()