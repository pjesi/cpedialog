__author__ = 'Ping Chen'

import os
import re
import datetime
import calendar
import logging
import string
from google.appengine.api import users
from google.appengine.ext import db

from model import Weblog,WeblogReactions
import config


# Functions to generate permalinks
def get_permalink(date,title):
    return str(date.year) + "/" + str(datetime.datetime.strftime(date,'%m')) + "/" + get_friendly_url(title)

# Module methods to handle incoming data
def get_datetime(time_string):
    if time_string:
        return datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')
    return datetime.datetime.now()

def get_friendly_url(title):
    return re.sub('-+', '-', re.sub('[^\w-]', '', re.sub('\s+', '-', title.strip())))

def u(s, encoding):
      if isinstance(s, unicode):
       return s
      else:
       return unicode(s, encoding)


#get the archive monthe list.
def getDatetimeList():
  weblog = Weblog.all().order('date').get()
  monthlist = []
  if weblog:
      startDate = weblog.date
      startYear = int(datetime.datetime.strftime(startDate,'%Y'))
      startMonth = int(datetime.datetime.strftime(startDate,'%m'))
      #endDate = int(datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d'))
      endDate =  datetime.datetime.now()
      endYear = int(datetime.datetime.strftime(endDate,'%Y'))
      endMonth = int(datetime.datetime.strftime(endDate,'%m'))
      for year in range(startYear,endYear+1):
          if year == startYear:
             if startYear == endYear:
               monthlist.extend(makeMonthList(year,startMonth,endMonth+1))
             else:
               monthlist.extend(makeMonthList(year,startMonth,12+1))
          else:
             if year ==endYear:
                monthlist.extend(makeMonthList(year,1,endMonth+1))
             else:
                monthlist.extend(makeMonthList(year,1,12+1))
  return monthlist

def makeMonthList(year,startMonth,endMonth):
     day = 1
     monthList = []
     for month in range(startMonth,endMonth):
         date = datetime.date(year,month,day)
         monthList.append(date)
     return monthList

def getLogoImagesList():
    logoImagesList = []
    directory = os.path.dirname(__file__)
    path = os.path.normpath(os.path.join(directory, 'img/logo/'))
    files = os.listdir(path)
    for file in files:
        (shortname, extension) = os.path.splitext(file)
        if extension.lower() == ".gif":
            logoImagesList.append(file)
    return logoImagesList

