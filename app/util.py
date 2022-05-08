import re
import datetime
import time
from exceptions import InvalidDateException, DateTooFarException, TeeTimeException, CourseException
from selenium import webdriver

def dockerparam():

    ######### Comment out for testing in python #########
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--window-size=1420,1080')
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--disable-gpu')
    web = webdriver.Chrome(options=chrome_options)
    return web


def date(date):

    currentDT = datetime.datetime.now()

    date_string = (date.replace(" ", "").lower())
    valid_months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    year = currentDT.strftime("%Y")
    mon = ''

    month_num_temp = 0
    month_num = 0

    for month in valid_months:
        month_num_temp = month_num_temp + 1
        if month in date_string:
            mon = month
            month_num = month_num_temp
    
    day_list = re.findall('\d+', date_string)
    day = int(day_list[0])

    if day < 1 or day > 31:
        raise InvalidDateException()
    elif mon == 'feb':
        if day > 28:
            raise InvalidDateException()
    elif mon in ['apr', 'jun', 'sep', 'nov']:
        if day > 30:
            raise InvalidDateException()

    date_desired = datetime.datetime(int(year), int(month_num), int(day))
    date_current = datetime.datetime(int(year),  int(currentDT.strftime("%m")), int(currentDT.strftime("%d")))
    timedelta_list = str(date_desired - date_current)
    timedelta = 0

    if timedelta_list == "0:00:00":
        timedelta = 0
    else:
        timed = timedelta_list.split(' day')
        timedelta = abs(int(timed[0]))

    if date_desired < date_current:
        raise InvalidDateException()
    if timedelta >= 8:
        raise DateTooFarException()
    
    if day < 10:
        day = str(0) + str(day)

    answer = [str(month_num), str(day), str(year)]

    return answer


def teetime(teetime):

    tee_string = (teetime.replace(" ", "").lower())

    timeslots = ['anytime', 'early', 'morning', 'afternoon', 'evening', 
    '6am', '7am', '8am', '9am', '10am', '11am', '12pm', '1pm', '2pm',
    '3pm', '4pm', '5pm', '6pm', '7pm']

    final_t = ''

    for subtime in timeslots:
        if tee_string == subtime:
            if tee_string == 'anytime':
                final_t = 'AnyTime'
            elif tee_string == 'early':
                final_t = 'Early(6AM - 8AM)'
            elif tee_string == 'morning':
                final_t = 'Morning(8AM - 12PM)'
            elif tee_string == 'afternoon':
                final_t = 'Afternoon(12PM - 4PM)'
            elif tee_string == 'evening':
                final_t = 'Evening(4PM - 8PM)'
            else:
                final_t = tee_string.upper()
    
    if final_t == '':
        raise TeeTimeException()

    return final_t

def course(course): # REPLACE WITH CURRENT WHEN ALL COURSES ARE ONLINE
    
    course_trimmed = (course.replace(" ", "").lower())
    final_course = 0

    if 'con' in course_trimmed:
        final_course = 1
    if 'lakev' in course_trimmed:
        final_course = 2
    if 'map' in course_trimmed and '18' in course_trimmed:
        final_course = 3
    if 'map' in course_trimmed and '9' in course_trimmed:
        final_course = 4
    if 'mc' in course_trimmed and '18' in course_trimmed:
        final_course = 5
    if 'mc' in course_trimmed and '9' in course_trimmed:
        final_course = 6
    if 'mc' in course_trimmed and '3' in course_trimmed:
        final_course = 7
    if 'sha' and 'ba' in course_trimmed and '9' in course_trimmed:
        final_course = 8
    if 'sha' and 'va' in course_trimmed and '9' in course_trimmed:
        final_course = 9
    if 'sha' in course_trimmed and '18' in course_trimmed:
        final_course = 10
    if final_course == 0:
        raise CourseException()

    return final_course

def timedelta(date):

    currentDT = datetime.datetime.now()

    date_current = datetime.datetime(int(currentDT.strftime("%Y")),  int(currentDT.strftime("%m")), int(currentDT.strftime("%d")), int(currentDT.strftime("%H")), int(currentDT.strftime("%M")), int(currentDT.strftime("%S")))
    des_date = datetime.datetime(int(currentDT.strftime("%Y")), int(date[0]), int(date[1]), int(5), int(59), int(30))
    booking_date = des_date - datetime.timedelta(4)

    timedel = booking_date - date_current
    seconds_diff = timedel.total_seconds()

    return [seconds_diff, booking_date]

def timefinetune(date):

    currentDT = datetime.datetime.now()

    date_current = datetime.datetime(int(currentDT.strftime("%Y")),  int(currentDT.strftime("%m")), int(currentDT.strftime("%d")), int(currentDT.strftime("%H")), int(currentDT.strftime("%M")), int(currentDT.strftime("%S")))
    des_date = datetime.datetime(int(currentDT.strftime("%Y")), int(date[0]), int(date[1]), int(6), int(0), int(1))
    booking_date = des_date - datetime.timedelta(4)

    timedel = booking_date - date_current
    seconds_diff = timedel.total_seconds()

    return seconds_diff

    
    
    