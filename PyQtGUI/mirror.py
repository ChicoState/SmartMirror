from __future__ import print_function
import pickle
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import sys
from twitter import *
sys.path.append(".")
import config

from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QLCDNumber)
from PyQt5.QtCore import QTimer, QTime
from PyQt5 import Qt



# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/calendar.readonly']

def getMail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    result = service.users().labels().get(id='INBOX', userId='me').execute()
    messages = result.get('messagesUnread')
    return messages

def getCalendar():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=5, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    eventlist = ''

    if not events:
        return 'No upcoming events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        eventlist += str(start) + ' ' + str(event['summary']) + '\n'
    return eventlist

def getTrending():
    twitter = Twitter(auth = OAuth(config.access_key,
                      config.access_secret,
                      config.consumer_key,
                      config.consumer_secret))
    results = twitter.trends.place(_id = 23424977)
    trendList = ''
    num = 0
    for location in results:
        for trend in location["trends"]:
            if num < 5:
                trendList += str(trend["name"]) + '\n'
            num += 1
    return trendList



class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.lcdTime = Qt.QLCDNumber()  #self
        self.lcdTime.setSegmentStyle(Qt.QLCDNumber.Filled)
        self.lcdTime.setDigitCount(8)
        self.timer1 = Qt.QTimer(self)
        self.timer1.timeout.connect(self.showTime)
        self.timer1.start(1000)


        #using gmail api
        self.mailLabel = QLabel("Unread emails:")
        numMail = getMail()
        self.mail = QLabel(str(numMail))

        #using google calendar api
        self.calendarLabel = QLabel("Calendar Events:")
        calendar = getCalendar()
        self.calendar = QLabel(calendar)

        #using twitter api
        self.twitterLabel = QLabel("Twitter Trending:")
        twitterEvents = getTrending()
        self.twitter = QLabel(twitterEvents)


        # We create a grid layout and set spacing between widgets.
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.lcdTime, 0, 0)

        grid.addWidget(self.mailLabel, 1, 0)
        grid.addWidget(self.mail, 1, 1)

        grid.addWidget(self.calendarLabel, 2, 0)
        grid.addWidget(self.calendar, 2, 1)

        grid.addWidget(self.twitterLabel, 3, 0)
        grid.addWidget(self.twitter, 3, 1)

        self.setLayout(grid)

        # self.setGeometry(300, 300, 350, 300)

        self.setWindowTitle('Smart Mirror')
        self.showFullScreen()

    def showTime(self):
        time = Qt.QTime.currentTime()
        text = time.toString("hh:mm:ss")
        if ((time.second() % 2) == 0):
            text = text[0:2] + ' ' + text[3:5] + ' ' + text[6:]
        self.lcdTime.display(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
