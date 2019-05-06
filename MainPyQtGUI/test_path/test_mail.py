#Google API Imports
import sys
from api import googleAPI

mailData = googleAPI.getMail()

def test_getMailHasData():
    assert(mailData != None)

def test_getMailIsString():
    assert(isinstance(mailData, int) == True)