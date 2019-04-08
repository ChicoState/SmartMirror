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

from PyQt5 import Qt

import time

#Spotify Imports
import urllib.request
import json
import spotifyLogIn

import weather

from PyQt5 import QtCore, QtWidgets, QtGui, QtSvg

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import os
import time


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


#Splash Screen Function for Process Bar
class ThreadProgress(QThread):
    mysignal = pyqtSignal(int)
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
    def run(self):
        i = 0
        while i<101:
            time.sleep(0.1)
            self.mysignal.emit(i)
            i += 1
#Splash Screen Function for Process Bar


# Splash Screen StyleSheet
FROM_SPLASH,_ = loadUiType(os.path.join(os.path.dirname(__file__),"splash.ui"))


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
        numMail = getMail()
        self.mailLabel = QLabel("Unread: " + str(numMail))
        self.mail = QLabel(str(numMail))

        self.mailIcon = QLabel()
        self.mailIcon.setPixmap(QPixmap("GMAIL.png").scaled(40, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation))
        # self.mailIcon.scaled(64, 64, Qt.IgnoreAspectRatio, Qt.FastTransformation)

        #using google calendar api
        calendar = getCalendar()
        # self.calendarLabel = QLabel("Calendar Events:" + "\n" + calendar)
        self.calendarLabel = QLabel(calendar)
        # self.calendar = QLabel(calendar)

        self.calendarIcon = QLabel()
        self.calendarIcon.setPixmap(QPixmap("CALENDAR.png").scaled(40, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation))

        #using twitter api
        twitterEvents = getTrending()
        # self.twitterLabel = QLabel("Twitter Trending:" + "\n" + twitterEvents)
        self.twitterLabel = QLabel(twitterEvents)
        self.twitter = QLabel(twitterEvents)

        self.twitterIcon = QLabel()
        self.twitterIcon.setPixmap(QPixmap("Twitter.png").scaled(60, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation))

        #Using Spotify API

        self.lbl = QtWidgets.QLabel(self)
        self.updateSong()

        self.musicTimer = QTimer()
        self.musicTimer.timeout.connect(self.updateSong)
        self.musicTimer.start(1000) # repeat self.updateSong() every 1 sec

        #Using Spotify API

        #Weather API
        self.weatherIcon = QtWidgets.QLabel(self)

        icon, temp, tempScale, location ,localizedName \
            = weather.get_weather()

        icon = 'icons/conditions/' + str(icon) + '.svg'

        self.iconLabel = QLabel(self)
        pixmap = QPixmap(icon)
        self.iconLabel.setPixmap(pixmap)

        self.temp = QLabel("Current Weather condition:" + '\n' + location + ", " + localizedName + "\n" +  str(temp)  + str(tempScale))


        #self.weather = QLabel(str(weather))
        #Weather API\
        self.tempLabel = QLabel(" ")

        # We create a grid layout and set spacing between widgets.
        self.grid = QGridLayout()
        self.grid.setSpacing(10)


        #self.lcdTime.setStyleSheet(DEFAULT_STYLE);
        self.labelTime.setStyleSheet(DEFAULT_STYLE);

        self.grid.addWidget(self.labelTime, 0, 0)
        self.grid.addWidget(self.tempLabel, 0, 1)

        self.mailLabel.setStyleSheet(DEFAULT_STYLE);
        self.mail.setStyleSheet(DEFAULT_STYLE);

        self.grid.addWidget(self.mailLabel, 4, 0)
        self.grid.addWidget(self.mailIcon, 3, 0)
        # self.grid.addWidget(self.mail, 2, 1)

        self.calendarLabel.setStyleSheet(DEFAULT_STYLE);
        # self.calendar.setStyleSheet(DEFAULT_STYLE);

        self.grid.addWidget(self.calendarLabel, 6, 0)
        self.grid.addWidget(self.calendarIcon, 5, 0)
        # self.grid.addWidget(self.calendar, 3, 1)

        self.twitterLabel.setStyleSheet(DEFAULT_STYLE);
        self.twitter.setStyleSheet(DEFAULT_STYLE);

        self.grid.addWidget(self.twitterLabel, 8, 0)
        self.grid.addWidget(self.twitterIcon, 7, 0)
        # self.grid.addWidget(self.twitter, 4, 1)

        #Spotify
        self.songs.setStyleSheet(DEFAULT_STYLE);
        self.grid.addWidget(self.lbl, 8, 5)
        self.grid.addWidget(self.songs, 9, 5)
        self.grid.addWidget(self.progress, 10, 5, 1 ,1)
        #Spotify

        #weather
        self.temp.setStyleSheet(DEFAULT_STYLE);

        self.grid.addWidget(self.temp, 1, 0)
        self.grid.addWidget(self.iconLabel, 2, 0)
        #weather

        self.setLayout(self.grid)


        # self.setGeometry(300, 300, 350, 300)

        self.setWindowTitle('Smart Mirror')
        self.showFullScreen()

    def showTime(self):
        time = QTime.currentTime()
        time_data = time.toString(Qt.DefaultLocaleLongDate)
        time_data = time_data[:-3]
        self.labelTime.setText(time_data)

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

        self.songs = QLabel(status + " " + data['item']['album']['artists'][0]['name'] + " - " + data['item']['name'])

        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setGeometry(30, 40, 0, 25)
        self.progress.setFixedWidth(200)

        self.progress.setStyleSheet(DEFAULT_STYLE)

        self.progress.setMaximum(100)
        self.progress.setValue(data['progress_ms'] * 100 / data['item']['duration_ms'])

        self.songs.setStyleSheet(DEFAULT_STYLE);

        self.grid.addWidget(self.lbl, 8, 5)
        self.grid.addWidget(self.songs, 9, 5)

        self.grid.addWidget(self.progress, 10, 5, 1 ,1)
        
class Splash(QMainWindow, FROM_SPLASH):
    def __init__(self, parent = None):
        super(Splash, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        pixmap = QPixmap("IMG_2647.JPG")

        self.splah_image.setPixmap(pixmap.scaled(350, 350))

        progress = ThreadProgress(self)
        #self.progressBar.setTextVisible(False)

        progress.mysignal.connect(self.progress)
        progress.start()
        
    @pyqtSlot(int)
    def progress(self, i):
        self.progressBar.setValue(i)
        if i == 100:
            self.hide()
            #exit()                  #Take this out once Splash Screen works
            self.ex = Example()
            self.ex.show()


def main():
    app=QApplication(sys.argv)
    window = Splash()
    window.show()
    #app.exec_()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
