
import math
import re
import pytz
import datetime
import timezonefinder

# from hijri.core import Hijriah



# Set the Gregorian date you want to convert
# year = 2023
# month = 3
# day = 26

# # Convert the Gregorian date to a Hijri date

# # Print the Hijri date
# print(hijri_date)


'''
--------------------- Copyright Block ----------------------
praytimes.py: Prayer Times Calculator (ver 2.3)
Copyright (C) 2007-2011 PrayTimes.org
Python Code: Saleem Shafi, Hamid Zarrabi-Zadeh
Original js Code: Hamid Zarrabi-Zadeh
License: GNU LGPL v3.0
TERMS OF USE:
	Permission is granted to use this code, with or
	without modification, in any website or application
	provided that credit is given to the original work
	with a link back to PrayTimes.org.
This program is distributed in the hope that it will
be useful, but WITHOUT ANY WARRANTY.
PLEASE DO NOT REMOVE THIS COPYRIGHT BLOCK.
--------------------- Help and Manual ----------------------
User's Manual:
http://praytimes.org/manual
Calculation Formulas:
http://praytimes.org/calculation
------------------------ User Interface -------------------------
	getTimes (date, coordinates, timeZone [, dst [, timeFormat]])
	setMethod (method)       // set calculation method
	adjust (parameters)      // adjust calculation parameters
	tune (offsets)           // tune times by given offsets
	getMethod ()             // get calculation method
	getSetting ()            // get current calculation parameters
	getOffsets ()            // get current time offsets
------------------------- Sample Usage --------------------------
	>>> PT = PrayTimes('ISNA')
	>>> times = PT.getTimes((2011, 2, 9), (43, -80), -5)
	>>> times['Sunrise']
	07:26
From Khabib Murtuzaaliev(skeeph):
    I'm not author of this library, but I have found and corrected a few of errors in this code
'''

# ----------------------- PrayTimes Class ------------------------


class PrayTimes():
    # ------------------------ Constants --------------------------

    # Time Names
    timeNames = {
        'Imsak': 'Imsak',
        'Fajr': 'Fajr',
        'Sunrise': 'Sunrise',
        'Dhuhr': 'Dhuhr',
        'Asr': 'Asr',
        'Sunset': 'Sunset',
        'Maghrib': 'Maghrib',
        'Isha': 'Isha',
        'Midnight': 'Midnight'
    }
        # Calculation Methods
    
    methods = {
            'MWL': {
                'name': 'Muslim World League',
                'params': {'Fajr': 18, 'Isha': 17}},
            'ISNA': {
                'name': 'Islamic Society of North America (ISNA)',
                'params': {'Fajr': 15, 'Isha': 15}},
            'Egypt': {
                'name': 'Egyptian General Authority of Survey',
                'params': {'Fajr': 19.5, 'Isha': 17.5}},
            'Makkah': {
                'name': 'Umm Al-Qura University, Makkah',
                'params': {'Fajr': 18.5, 'Isha': '90 min'}},  # Fajr was 19 degrees before 1430 hijri
            'Karachi': {
                'name': 'University of Islamic Sciences, Karachi',
                'params': {'Fajr': 18, 'Isha': 18}},
            'Tehran': {
                'name': 'Institute of Geophysics, University of Tehran',
                'params': {'Fajr': 17.7, 'Isha': 14, 'Maghrib': 4.5, 'Midnight': 'Jafari'}},
            # Isha is not explicitly specified in this method
            'Jafari': {
                'name': 'Shia Ithna-Ashari, Leva Institute, Qum',
                'params': {'Fajr': 16, 'Isha': 14, 'Maghrib': 4, 'Midnight': 'Jafari'}}
        }

    # Default Parameters in Calculation Methods
    defaultParams = {
        'Maghrib': '0 min', 'Midnight': 'Standard'
    }

    # ---------------------- Default Settings --------------------

    calcMethod = 'MWL'

    # do not change anything here; use adjust method instead
    settings = {
        "Imsak": '10 min',
        "Dhuhr": '0 min',
        "Asr": 'Standard',
        "highLats": 'NightMiddle'
    }

    timeFormat = '24h'
    timeSuffixes = ['am', 'pm']
    invalidTime = '-----'

    numIterations = 1
    offset = {}
	
    # ---------------------- Initialization -----------------------

    def __init__(self, method="MWL"):
        # set methods defaults
        for method, config in self.methods.items():
            for name, value in self.defaultParams.items():
                if not name in config['params'] or config['params'][name] is None:
                    config['params'][name] = value
    
        # initialize settings
        self.calcMethod = method if method in self.methods else 'MWL'
        params = self.methods[self.calcMethod]['params']
        for name, value in params.items():
            self.settings[name] = value

        # init time offsets
        for name in self.timeNames:
            self.offset[name] = 0

    # -------------------- Interface Functions --------------------

    def setMethod(self, method):
        if method in self.methods:
            # Authors of library used here method[method].params but dictionary hasn't this attribute here must use methods[method]['params'] instead it
            self.adjust(self.methods[method]['params'])
            self.calcMethod = method

    def adjust(self, params):
        self.settings.update(params)

    def tune(self, timeOffsets):
        # Here was error of attribute. Authors wrote self.offsets but so attribute didn't exist
        self.offset.update(timeOffsets)

    def getMethod(self):
        return self.calcMethod

    def getSettings(self):
        return self.settings

    def getOffsets(self):
        return self.offset

    def getDefaults(self):
        return self.methods

    # return prayer times for a given date
    def getTimes(self, date, coords, hijri=None ,dst=0, format=None):
        self.lat = coords[0]
        self.lng = coords[1]
        self.elv = coords[2] if len(coords) > 2 else 0
        timezone_str, timezone_offset = self.get_offset_by_lat_long(self.lat, self.lng)
        if format != None:
            self.timeFormat = format
        if type(date).__name__ == 'date':
            date = (date.year, date.month, date.day)
		
        self.timeZone = timezone_offset + (1 if dst else 0)
        self.jDate = self.julian(date[0], date[1], date[2]) - self.lng / (15 * 24.0)


        response = {
            "timings": self.computeTimes(),
            "date": {
                "readable": date.strftime("%d %b %Y"),
                "hijri": {
					"date":hijri.isoformat(),
                    "format": "DD-MM-YYYY",
                    "day": hijri.day,
                    "month": {
                        "number": hijri.month,
                        "en": "Jumādá al-ākhirah",
                        "ar": "جُمادى الآخرة"
                    },
                    "year": hijri.year,
                    "designation": {
                            "abbreviated": "AH",
                            "expanded": "Anno Hegirae"
                    },
                    "holidays": []
                },
                "gregorian": {
                    "date": date.strftime("%d-%m-%Y"),
                    "format": "DD-MM-YYYY",
                    "day": date.day,
                    "month": {
                        "number": date.month,
                    },
                    "year": date.year
                }
            }

        }
        return response

    # convert float time to the given format (see timeFormats)
    def getFormattedTime(self, time, format, suffixes=None):
        if math.isnan(time):
            return self.invalidTime
        if format == 'Float':
            return time
        if suffixes == None:
            suffixes = self.timeSuffixes

        time = self.fixhour(time + 0.5 / 60)  # add 0.5 minutes to round
        hours = math.floor(time)

        minutes = math.floor((time - hours) * 60)
        suffix = suffixes[0 if hours < 12 else 1] if format == '12h' else ''
        formattedTime = "%02d:%02d" % (hours, minutes) if format == "24h" else "%d:%02d" % (
            (hours + 11) % 12 + 1, minutes)
        return formattedTime + suffix

    # ---------------------- Calculation Functions -----------------------

    # compute mid-day time

    def midDay(self, time):
        eqt = self.sunPosition(self.jDate + time)[1]
        return self.fixhour(12 - eqt)

    # compute the time at which sun reaches a specific angle below horizon
    def sunAngleTime(self, angle, time, direction=None):
        try:
            decl = self.sunPosition(self.jDate + time)[0]
            noon = self.midDay(time)
            t = 1 / 15.0 * self.arccos((-self.sin(angle) - self.sin(decl) * self.sin(self.lat)) /
                                       (self.cos(decl) * self.cos(self.lat)))
            return noon + (-t if direction == 'ccw' else t)
        except ValueError:
            return float('nan')

    # compute Asr time
    def AsrTime(self, factor, time):
        decl = self.sunPosition(self.jDate + time)[0]
        angle = -self.arccot(factor + self.tan(abs(self.lat - decl)))
        return self.sunAngleTime(angle, time)

    # compute declination angle of sun and equation of time
    # Ref: http://aa.usno.navy.mil/faq/docs/SunApprox.php
    def sunPosition(self, jd):
        D = jd - 2451545.0
        g = self.fixangle(357.529 + 0.98560028 * D)
        q = self.fixangle(280.459 + 0.98564736 * D)
        L = self.fixangle(q + 1.915 * self.sin(g) + 0.020 * self.sin(2 * g))

        R = 1.00014 - 0.01671 * self.cos(g) - 0.00014 * self.cos(2 * g)
        e = 23.439 - 0.00000036 * D

        RA = self.arctan2(self.cos(e) * self.sin(L), self.cos(L)) / 15.0
        eqt = q / 15.0 - self.fixhour(RA)
        decl = self.arcsin(self.sin(e) * self.sin(L))

        return (decl, eqt)

    # convert Gregorian date to Julian day
    # Ref: Astronomical Algorithms by Jean Meeus
    def julian(self, year, month, day):
        if month <= 2:
            year -= 1
            month += 12
        A = math.floor(year / 100)
        B = 2 - A + math.floor(A / 4)
        return math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5

    # ---------------------- Compute Prayer Times -----------------------

    # compute prayer times at given julian date

    def computePrayerTimes(self, times):
        times = self.dayPortion(times)
        params = self.settings

        Imsak = self.sunAngleTime(
            self.eval(params['Imsak']), times['Imsak'], 'ccw')
        Fajr = self.sunAngleTime(
            self.eval(params['Fajr']), times['Fajr'], 'ccw')
        Sunrise = self.sunAngleTime(self.riseSetAngle(
            self.elv), times['Sunrise'], 'ccw')
        Dhuhr = self.midDay(times['Dhuhr'])
        Asr = self.AsrTime(self.AsrFactor(params['Asr']), times['Asr'])
        Sunset = self.sunAngleTime(
            self.riseSetAngle(self.elv), times['Sunset'])
        Maghrib = self.sunAngleTime(
            self.eval(params['Maghrib']), times['Maghrib'])
        Isha = self.sunAngleTime(self.eval(params['Isha']), times['Isha'])
        prayers = {
            'Imsak': {
                "time": Imsak
            },
            'Fajr':{
                "time": Fajr
            },
            'Sunrise': {
                "time": Sunrise
            } ,
            'Dhuhr': {
                "time": Dhuhr
            } ,
            'Asr': {
                "time": Asr
            }, 
            'Sunset': {
                "time": Sunset
            } , 
            'Maghrib': {
                "time":Maghrib
            }, 
            'Isha': {
                "time":Isha
            } 
        }

        return prayers

    # compute prayer times
    def computeTimes(self):
        times = {
            'Imsak': 5, 'Fajr': 5, 'Sunrise': 6, 'Dhuhr': 12,
            'Asr': 13, 'Sunset': 18, 'Maghrib': 18, 'Isha': 18
        }
        # main iterations
        for i in range(self.numIterations):
            times = self.computePrayerTimes(times)
        times = self.adjustTimes(times)
        # add Midnight time
        if self.settings['Midnight'] == 'Jafari':
            times['Midnight'] = {
                "time":times['Sunset']['time'] + \
                self.timeDiff(times['Sunset']['time'], times['Fajr']['time']) / 2
            }
        else:
            times['Midnight'] = {
                    "time":times['Sunset']['time'] + \
                self.timeDiff(times['Sunset']['time'], times['Sunrise']['time']) / 2
            }
        times = self.tuneTimes(times)
        return self.modifyFormats(times)

    # adjust times in a prayer time array
    def adjustTimes(self, times):
        params = self.settings
        tzAdjust = self.timeZone - self.lng / 15.0
        for t, v in times.items():
            times[t]['time'] += tzAdjust

        if params['highLats'] != 'None':
            times = self.adjustHighLats(times)

        if self.isMin(params['Imsak']):
            times['Imsak']["time"] = times['Fajr']['time'] - self.eval(params['Imsak']) / 60.0
            # need to ask about 'min' settings
        if self.isMin(params['Maghrib']):
            times['Maghrib']['time'] = times['Sunset']['time'] - \
                self.eval(params['Maghrib']) / 60.0

        if self.isMin(params['Isha']):
            times['Isha']['time'] = times['Maghrib']['time'] - self.eval(params['Isha']) / 60.0
        times['Dhuhr']['time'] += self.eval(params['Dhuhr']) / 60.0
        return times

    # get Asr shadow factor
    def AsrFactor(self, AsrParam):
        methods = {'Standard': 1, 'Hanafi': 2}
        return methods[AsrParam] if AsrParam in methods else self.eval(AsrParam)

    # return sun angle for Sunset/Sunrise
    def riseSetAngle(self, elevation=0):
        elevation = 0 if elevation == None else elevation
        return 0.833 + 0.0347 * math.sqrt(elevation)  # an approximation

    # apply offsets to the times
    def tuneTimes(self, times):
        for name, value in times.items():
            times[name]['time'] += self.offset[name] / 60.0

        return times

    # convert times to given time format
    def modifyFormats(self, times):
        for name, value in times.items():
            times[name]['time'] = self.getFormattedTime(times[name]['time'], self.timeFormat)
        return times

    # adjust times for locations in higher latitudes
    def adjustHighLats(self, times):
        params = self.settings
        nightTime = self.timeDiff(
            times['Sunset']['time'], times['Sunrise']['time'])  # Sunset to Sunrise
        times['Imsak']['time'] = self.adjustHLTime(times['Imsak']['time'], times['Sunrise']['time'], self.eval(params['Imsak']), nightTime,
                                           'ccw')
        times['Fajr']['time'] = self.adjustHLTime(
            times['Fajr']['time'], times['Sunrise']['time'], self.eval(params['Fajr']), nightTime, 'ccw')
        times['Isha']['time'] = self.adjustHLTime(
            times['Isha']['time'], times['Sunset']['time'], self.eval(params['Isha']), nightTime)
        times['Maghrib']['time'] = self.adjustHLTime(
            times['Maghrib']['time'], times['Sunset']['time'], self.eval(params['Maghrib']), nightTime)
        return times

    # adjust a time for higher latitudes
    def adjustHLTime(self, time, base, angle, night, direction=None):
        portion = self.nightPortion(angle, night)
        diff = self.timeDiff(
            time, base) if direction == 'ccw' else self.timeDiff(base, time)
        if math.isnan(time) or diff > portion:
            time = base + (-portion if direction == 'ccw' else portion)
        return time

    # the night portion used for adjusting times in higher latitudes
    def nightPortion(self, angle, night):
        method = self.settings['highLats']
        portion = 1 / 2.0  # Midnight
        if method == 'AngleBased':
            portion = 1 / 60.0 * angle
        if method == 'OneSeventh':
            portion = 1 / 7.0
        return portion * night

    # convert hours to day portions
    def dayPortion(self, times):
        for i in times:
            times[i] /= 24.0
        return times

    # ---------------------- Misc Functions -----------------------

    # compute the difference between two times

    def timeDiff(self, time1, time2):
        return self.fixhour(time2 - time1)

    # convert given string into a number
    def eval(self, st):
        val = re.split('[^0-9.+-]', str(st), 1)[0]
        return float(val) if val else 0

    # detect if input contains 'min'
    def isMin(self, arg):
        return isinstance(arg, str) and arg.find('min') > -1

    # ----------------- Degree-Based Math Functions -------------------

    def sin(self, d): return math.sin(math.radians(d))

    def cos(self, d): return math.cos(math.radians(d))

    def tan(self, d): return math.tan(math.radians(d))

    def arcsin(self, x): return math.degrees(math.asin(x))

    def arccos(self, x): return math.degrees(math.acos(x))

    def arctan(self, x): return math.degrees(math.atan(x))

    def arccot(self, x): return math.degrees(math.atan(1.0 / x))

    def arctan2(self, y, x): return math.degrees(math.atan2(y, x))

    def fixangle(self, angle): return self.fix(angle, 360.0)

    def fixhour(self, hour): return self.fix(hour, 24.0)

    def fix(self, a, mode):
        if math.isnan(a):
            return a
        a = a - mode * (math.floor(a / mode))
        return a + mode if a < 0 else a

    def get_offset_by_lat_long(self, lat, lng):
        tf = timezonefinder.TimezoneFinder()
        # From the lat/long, get the tz-database-style time zone name (e.g. 'America/Vancouver') or None
        timezone_str = tf.certain_timezone_at(lat=lat, lng=lng)
        tz = pytz.timezone(timezone_str)
        day = datetime.datetime.now()
        offset = tz.utcoffset(day)/3600
        return timezone_str, offset.total_seconds()
# ---------------------- prayTimes Object -----------------------



prayTimes = PrayTimes()