#Google API Imports
from api import googleAPI

calendarData = googleAPI.getCalendar()

def test_getCalendarHasData():
    assert(calendarData != None)

def test_getCalendarIsString():
    assert(isinstance(calendarData, str) == True)