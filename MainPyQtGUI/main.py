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
from PyQt5 import Qt, QtCore, QtWidgets, QtGui, QtSvg
#from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

'''
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
'''


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
        #self.setStyleSheet(DEFAULT_STYLE)
        self.initUI()

    def initUI(self):

        self.grid = QGridLayout()
        #self.setGeometry(10,10,1400,1400)

        self.labelTime = QLabel()
        self.showTime()

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000) # repeat self.showTime() every 1 sec

        # PICTURES TO LOOP THROUGH SECTION
        # self.pictureIter = 0
        # self.files = ["./pictures/a.PNG", "./pictures/b.PNG", "./pictures/c.PNG"]
        # self.pictureLabel = QLabel()
        # self.pictureLabel.setPixmap(QPixmap(self.files[self.pictureIter]).scaled(200, 200, QtCore.Qt.KeepAspectRatio))
        # self.pictureTimer = QTimer()
        # self.pictureTimer.timeout.connect(self.changePicture)
        # self.pictureTimer.start(8000)

        #using gmail api
        numMail = googleAPI.getMail()
        self.mailLabel = QLabel("Unread: " + str(numMail))
        self.mail = QLabel(str(numMail))

        self.mailIcon = QLabel()
        self.mailIcon.setPixmap(QPixmap("./icons/GMAIL.png").scaled(40, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation))

        #using google calendar api
        calendar = googleAPI.getCalendar()
        self.calendarLabel = QLabel(calendar)

        self.calendarIcon = QLabel()
        self.calendarIcon.setPixmap(QPixmap("./icons/CALENDAR.png").scaled(40, 40, Qt.IgnoreAspectRatio, Qt.FastTransformation))

        #using twitter api
        twitterEvents = twitterAPI.getTrending()
        self.twitterLabel = QLabel(twitterEvents)

        self.twitterIcon = QLabel()
        self.twitterIcon.setPixmap(QPixmap("./icons/Twitter.png").scaled(60, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation))

        #using the spotify api
        self.lbl = QtWidgets.QLabel(self)
        self.updateSong()

        self.musicTimer = QTimer()
        self.musicTimer.timeout.connect(self.updateSong)
        self.musicTimer.start(1000) # repeat self.updateSong() every 1 sec

        #Weather API
        self.weatherIcon = QtWidgets.QLabel(self)

        icon, temp, tempScale, location ,localizedName \
            = weather.get_weather()

        icon = 'icons/conditions/' + str(icon) + '.svg'

        self.iconLabel = QLabel(self)
        pixmap = QPixmap(icon)
        self.iconLabel.setPixmap(pixmap)

        self.temp = QLabel("Current Weather condition:" + '\n' + location + ", " + localizedName + "\n" +  str(temp)  + str(tempScale))

        self.apiTimer = QTimer()
        self.apiTimer.timeout.connect(self.updateAPI)
        self.apiTimer.start(1000 * 3600) # repeat every hour

        # We create a grid layout and set spacing between widgets.
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        #self.labelTime.setStyleSheet(DEFAULT_STYLE);

        self.grid.addWidget(self.labelTime, 0, 0)

        #self.mailLabel.setStyleSheet(DEFAULT_STYLE);
        #self.mail.setStyleSheet(DEFAULT_STYLE);

        self.grid.addWidget(self.mailLabel, 4, 0)
        self.grid.addWidget(self.mailIcon, 3, 0)

        #self.calendarLabel.setStyleSheet(DEFAULT_STYLE);

        self.grid.addWidget(self.calendarLabel, 6, 0)
        self.grid.addWidget(self.calendarIcon, 5, 0)

        #self.twitterLabel.setStyleSheet(DEFAULT_STYLE);


        self.grid.addWidget(self.twitterLabel, 8, 0)
        self.grid.addWidget(self.twitterIcon, 7, 0)

        #Spotify
        #self.songs.setStyleSheet(DEFAULT_STYLE);
        self.grid.addWidget(self.lbl, 9, 0)
        self.grid.addWidget(self.songs, 10, 0)
        self.grid.addWidget(self.progress, 10, 5, 1 ,1)
        #Spotify

        # self.grid.addWidget(self.pictureLabel, 9, 0)

        #weather
        #self.temp.setStyleSheet(DEFAULT_STYLE);

        self.grid.addWidget(self.temp, 1, 0)
        #self.grid.addWidget(self.iconLabel, 2, 0)
        self.grid.addWidget(self.iconLabel, 0, 3)
        #weather

        #Firebase
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
        self.progress.setGeometry(30, 40, 0, 25)
        self.progress.setFixedWidth(200)

        #self.progress.setStyleSheet(DEFAULT_STYLE)

        self.progress.setMaximum(100)
        self.progress.setValue(data['progress_ms'] * 100 / data['item']['duration_ms'])

        #self.songs.setStyleSheet(DEFAULT_STYLE);

        self.grid.addWidget(self.lbl, 9, 0)
        self.grid.addWidget(self.songs, 10, 0)

        self.grid.addWidget(self.progress, 10, 5, 1, 1)

    # def changePicture(self):
    #     self.pictureIter += 1
    #     if(self.pictureIter == len(self.files)):
    #         self.pictureIter = 0
    #     self.pictureLabel.setPixmap(QPixmap(self.files[self.pictureIter]).scaled(200, 200, QtCore.Qt.KeepAspectRatio))
    #     self.grid.addWidget(self.pictureLabel, 9, 0)

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
        pixmap = QPixmap("./icons/splash/IMG_2647.JPG")

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
