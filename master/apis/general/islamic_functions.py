import math


class Qibla:
    def __init__(self) -> None:
        self.makkah_lat = 21.42250833
        self.makkah_lng = 39.82616111

    def get_direction(self, latitude, longitude):
        deg = self._atan2_deg(self._sin_deg(self.makkah_lng - longitude),
		self._cos_deg(latitude) * self._tan_deg(self.makkah_lat)
		- self._sin_deg(latitude) * self._cos_deg(self.makkah_lng - longitude))

        return deg if deg >= 0 else deg + 360

    def _sin_deg(self, deg):
        return math.sin(math.radians(deg))
    
    def _cos_deg(self, deg):
        return math.cos(math.radians(deg))

    def _tan_deg(self, deg):
        return math.tan(math.radians(deg))

    def _atan2_deg(self, y, x):
        return math.degrees(math.atan2(y, x))
    

# class Qibla:
# 	def __init__(self):
# 		self.makkah_lng = 39.82616111
# 		self.makkah_lat = 21.42250833

#         def _sin_deg(deg):
#             return math.sin(math.radians(deg))

#     def _cos_deg(deg):
#             return math.cos(math.radians(deg))

#     def _tan_deg(deg):
#             return math.tan(math.radians(deg))

#     def _atan2_deg(y, x):
#             return math.degrees(math.atan2(y, x))

		
    
# def qibla(lat, lng):
# 	"""Return qibla direction in degrees from the north (clock-wise)
	
# 	Param:
# 	lat as number - latitude in degrees
# 	lng as number - longitude in degrees

# 	Return:
# 	number - 0 means north, 90 means east, 270 means west, etc
# 	"""
# 	makkah_lng = 39.82616111
# 	makkah_lat = 21.42250833
# 	deg = _atan2_deg(_sin_deg(makkah_lng - lng),
# 		_cos_deg(lat) * _tan_deg(makkah_lat)
# 		- _sin_deg(lat) * _cos_deg(makkah_lng - lng))
# 	return deg if deg >= 0 else deg + 360
