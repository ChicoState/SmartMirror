from __future__ import print_function

import os
import sys
import time

sys.path.append(".")

#Spotify Imports
import urllib.request
import json
from api import spotifyLogIn

#Weather Imports
from api import weather

#Google API Imports
from api import googleAPI

#Twitter API Imports
from api import twitterAPI

#FireBase
from firebase import info

#PyQt5 Imports
from PyQt5 import Qt, QtCore, QtWidgets, QtGui
#from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

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
FROM_MAIN,_ = loadUiType(os.path.join(os.path.dirname(__file__),"main.ui"))

class Example(QWidget, FROM_MAIN):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.initUI()

    def initUI(self):

        self.grid = QGridLayout()

        self.labelTime = QLabel()
        self.showTime()

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000) # repeat self.showTime() every 1 sec

        #using google mail api
        numMail = googleAPI.getMail()

        self.mailLabel = QLabel("Unread: " + str(numMail))
        self.mail = QLabel(str(numMail))

        self.mailIcon = QLabel()
        self.mailIcon.setPixmap(QPixmap("./icons/GMAIL.png").scaled(35, 35, Qt.IgnoreAspectRatio, Qt.FastTransformation))

        #using google calendar api
        calendar = googleAPI.getCalendar()
        self.calendarLabel = QLabel(calendar)

        self.calendarIcon = QLabel()
        self.calendarIcon.setPixmap(QPixmap("./icons/CALENDAR.png").scaled(40, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation))

        #using twitter api
        twitterEvents = ''
        try:
            twitterEvents = twitterAPI.getTrending()
        except:
            twitterEvents = "Failed to retrieve data."
        self.twitterLabel = QLabel(twitterEvents)

        self.twitterIcon = QLabel()
        self.twitterIcon.setPixmap(QPixmap("./icons/Twitter.png").scaled(40, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation))

        #using spotify api
        try:
            self.lbl = QtWidgets.QLabel(self)
            self.updateSong()

            self.musicTimer = QTimer()
            self.musicTimer.timeout.connect(self.updateSong)
            self.musicTimer.start(1000) # repeat self.updateSong() every 1 sec
        except:
            self.lbl = QLabel("Spotify cannot connect.")

        #Weather API
        icon, temp, tempScale, location ,localizedName \
            = weather.get_weather()

        self.temp = QLabel(location.lower() + ", " + localizedName.lower() + "\n" +  str(temp)  + str(tempScale))

        self.apiTimer = QTimer()
        self.apiTimer.timeout.connect(self.updateAPI)
        self.apiTimer.start(1000 * 3600) # repeat every hour


        self.labelTime.setAlignment(QtCore.Qt.AlignRight)

        self.labelTime.setStyleSheet("font: 15pt; color: white")

        
        #--------

        #self.paddingLeft = Qlabel(" ")
        #self.grid.addWidget(self.paddingLeft, 0, 0)
        self.grid.setVerticalSpacing(0)

        self.paddingLeft = QLabel(" ")
        self.paddingLeft.setStyleSheet("font: 3pt; color: black")
        
        self.grid.addWidget(self.paddingLeft, 0, 0)

        #weather
        self.temp.setMargin(0)
        self.grid.addWidget(self.temp, 1, 0)

        #Time
        self.labelTime.setMargin(0)
        self.grid.addWidget(self.labelTime, 1, 1)

        #Mail
        self.mailIcon.setMargin(0)
        self.grid.addWidget(self.mailIcon, 2, 0)
        self.mailLabel.setMargin(0)
        self.grid.addWidget(self.mailLabel, 3, 0)


        #Calendar
        self.calendarIcon.setMargin(0)
        self.grid.addWidget(self.calendarIcon, 4, 0)
        self.calendarLabel.setMargin(0)
        self.grid.addWidget(self.calendarLabel, 5, 0)

        #Twitter
        self.twitterIcon.setMargin(0)
        self.grid.addWidget(self.twitterIcon, 6, 0)
        self.twitterLabel.setMargin(0)
        self.grid.addWidget(self.twitterLabel, 7, 0)

        #Spotify
        self.grid.addWidget(self.lbl, 8, 0)
        self.grid.addWidget(self.songs, 9, 0)
        self.grid.addWidget(self.progress, 10, 0)
        #Spotify


        '''
        self.grid.addWidget(self.labelTime, 0, 1)

        self.grid.addWidget(self.mailLabel, 2, 0)
        self.grid.addWidget(self.mailIcon, 1, 0)


        self.grid.addWidget(self.calendarLabel, 4, 0)
        self.grid.addWidget(self.calendarIcon, 3, 0)



        self.grid.addWidget(self.twitterLabel, 6, 0)
        self.grid.addWidget(self.twitterIcon, 5, 0)

        #Spotify
        self.grid.addWidget(self.lbl, 7, 0)
        self.grid.addWidget(self.songs, 8, 0)
        self.grid.addWidget(self.progress, 9, 0, 1, 1)
        #Spotify

        #weather
        self.grid.addWidget(self.temp, 0, 0)
        '''

        self.setLayout(self.grid)

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

        self.progress.setFixedWidth(200)
        self.progress.setFixedHeight(15)

        self.progress.setMaximum(100)
        self.progress.setValue(data['progress_ms'] * 100 / data['item']['duration_ms'])

        self.grid.addWidget(self.lbl, 8, 0)
        self.grid.addWidget(self.songs, 9, 0)
        self.grid.addWidget(self.progress, 10, 0, 1, 1)

    def updateAPI(self):
        numMail = googleAPI.getMail()
        self.mailLabel = QLabel("Unread: " + str(numMail))
        self.mail = QLabel(str(numMail))

        calendar = googleAPI.getCalendar()
        self.calendarLabel = QLabel(calendar)

        twitterEvents = twitterAPI.getTrending()
        self.twitterLabel = QLabel(twitterEvents)

        icon, temp, tempScale, location ,localizedName \
            = weather.get_weather()

        icon = 'icons/conditions/' + str(icon) + '.svg'

        self.iconLabel = QLabel(self)
        pixmap = QPixmap(icon)
        self.iconLabel.setPixmap(pixmap)

        self.temp = QLabel("Current Weather condition:" + '\n' + location + ", " + localizedName + "\n" +  str(temp)  + str(tempScale))

        self.grid.addWidget(self.mailLabel, 4, 0)
        self.grid.addWidget(self.calendarLabel, 6, 0)
        self.grid.addWidget(self.twitterLabel, 8, 0)
        self.grid.addWidget(self.temp, 1, 0)
        self.grid.addWidget(self.iconLabel, 2, 0)


class Splash(QMainWindow, FROM_SPLASH, FROM_MAIN):
    def __init__(self, parent = None):
        super(Splash, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.showMaximized()        #Show Splashcreen full Screeen instead
        pixmap = QPixmap("./icons/splash/IMG_2647.JPG")

        self.splah_image.setPixmap(pixmap.scaled(350, 350))
        self.splah_image.setAlignment(Qt.AlignVCenter)

        progress = ThreadProgress(self)

        progress.mysignal.connect(self.progress)

        progress.start()

    @pyqtSlot(int)
    def progress(self, i):
        self.progressBar.setValue(i)

        if i == 100:
            self.hide()
            self.ex = Example()
            self.ex.show()

def main():
    app=QApplication(sys.argv)
    window = Splash()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
