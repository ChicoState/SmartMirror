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

#Spotify Imports
import time

import urllib.request
import json
import spotifyLogIn
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QProgressBar
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QColor

DEFAULT_STYLE = """
QWidget{
    background-color: black;
}
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}
QProgressBar::chunk {
    background-color: white;
    width: 10px;
}
QLabel{
    color:  #ffffff;
    font: 15pt Comic Sans MS
}
"""

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

        self.setStyleSheet(DEFAULT_STYLE)
        self.initUI()

    def initUI(self):

        self.grid = QGridLayout()
        #self.setGeometry(10,10,1400,1400)

        self.labelTime = QLabel()
        self.showTime()

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000) # repeat self.showTime() every 1 sec


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

        #Using Spotify API

        self.lbl = QtWidgets.QLabel(self)
        self.updateSong()

        self.musicTimer = QTimer()
        self.musicTimer.timeout.connect(self.updateSong)
        self.musicTimer.start(1000) # repeat self.updateSong() every 1 sec

        #Using Spotify API



        # We create a grid layout and set spacing between widgets.
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        #self.lcdTime.setStyleSheet(DEFAULT_STYLE);
        self.labelTime.setStyleSheet(DEFAULT_STYLE);

        #self.grid.addWidget(self.lcdTime, 0, 0)
        self.grid.addWidget(self.labelTime, 0, 0)

        self.mailLabel.setStyleSheet(DEFAULT_STYLE);
        self.mail.setStyleSheet(DEFAULT_STYLE);

        self.grid.addWidget(self.mailLabel, 1, 0)
        self.grid.addWidget(self.mail, 1, 1)

        self.calendarLabel.setStyleSheet(DEFAULT_STYLE);
        self.calendar.setStyleSheet(DEFAULT_STYLE);

        self.grid.addWidget(self.calendarLabel, 2, 0)
        self.grid.addWidget(self.calendar, 2, 1)

        self.twitterLabel.setStyleSheet(DEFAULT_STYLE);
        self.twitter.setStyleSheet(DEFAULT_STYLE);

        self.grid.addWidget(self.twitterLabel, 3, 0)
        self.grid.addWidget(self.twitter, 3, 1)

        #Spotify
        self.songs.setStyleSheet(DEFAULT_STYLE);

        self.grid.addWidget(self.lbl, 4, 0)
        self.grid.addWidget(self.songs, 4, 1)
        self.grid.addWidget(self.progress, 5, 0)

        #Spotify

        self.setLayout(self.grid)


        # self.setGeometry(300, 300, 350, 300)

        self.setWindowTitle('Smart Mirror')
        self.showFullScreen()

    def showTime(self):
        time = QTime.currentTime()
        time_data = time.toString(Qt.DefaultLocaleLongDate)

        if int(time_data[0:2]) >= 10:
            time = time_data[0:11]
        else:
            time = time_data[0:10]

        self.labelTime.setText(time)

    def updateSong(self):
        data = spotifyLogIn.get_data()
        url = data['item']['album']['images'][0]['url']
        self.image = urllib.request.urlopen(url).read()

        image = QtGui.QImage()
        image.loadFromData(self.image)

        self.lbl.adjustSize()

        pixmap4 = image.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        self.lbl.setPixmap(QtGui.QPixmap(pixmap4))

        status = " "

        if data['is_playing'] == True:
            status = "Now Playing:"
        else:
            status = "Stoped:"

        #self.songs = QLabel(status + "\n" + data['item']['name'] + "\n" + data['item']['album']['artists'][0]['name'])
        self.songs = QLabel(status + "\n" + data['item']['album']['artists'][0]['name'] + " - " + data['item']['name'])

        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setGeometry(30, 40, 200, 25)

        self.progress.setStyleSheet(DEFAULT_STYLE)

        self.progress.setMaximum(100)
        self.progress.setValue(data['progress_ms'] * 100 / data['item']['duration_ms'])

        self.songs.setStyleSheet(DEFAULT_STYLE);

        self.grid.addWidget(self.lbl, 4, 0)
        self.grid.addWidget(self.songs, 4, 1)

        self.grid.addWidget(self.progress, 5, 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
