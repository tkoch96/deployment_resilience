import os
# This file contains constants -- settings, things in nature that are constant, directory names, etc.


# private IP space -- from https://github.com/zmap/zmap/blob/master/conf/blacklist.conf
private_ips = [("0.0.0.0", 8), ("10.0.0.0", 8), ("100.64.0.0", 10), ("127.0.0.0",8), ("169.254.0.0",16),
	("172.16.0.0", 12), ("192.0.0.0", 24), ("192.0.2.0", 24), ("192.88.99.0", 24), ("192.168.0.0", 16), ("198.18.0.0", 15),
	("198.51.100.0", 24), ("203.0.113.0", 24), ("240.0.0.0",4), ("255.255.255.255", 32), ("224.0.0.0",4),
	("25.0.0.0",8)]


# directories
DATA_DIR = "data"
CACHE_DIR = "cache"
FIGURE_DIR = "figures"
TMP_DIR = "tmp"


VULTR_POP_TO_LOC = {
	'amsterdam': (52.359,4.933),
	'atlanta': (33.749, -84.388),
	'bangalore': (12.940, 77.782),
	'chicago': (41.803,-87.710),
	'dallas': (32.831,-96.641),
	'delhi': (28.674,77.099),
	'frankfurt': (50.074, 8.643),
	'johannesburg': (-26.181, 27.993),
	'london' : (51.452,-.110),
	'losangelas': (34.165,-118.489),
	'madrid': (40.396,-3.678),
	'melbourne': (-37.858, 145.028),
	'mexico': (19.388, -99.138),
	'miami' : (25.786, -80.229),
	'mumbai' : (19.101, 72.869),
	'newyork': (40.802,-73.970),
	'paris': (48.836,2.308),
	'saopaulo' : (-23.561, -46.532),
	'seattle': (47.577, -122.373),
	'seoul': (37.683,126.942),
	'silicon': (37.312,-121.816),
	'singapore': (1.322,103.962),
	'stockholm': (59.365,17.943),
	'sydney': (-33.858,151.068),
	'tokyo': (35.650,139.619),
	'toronto': (43.679, -79.305),
	'warsaw': (52.248,21.027),
}

# Plotting colors
cols = ['orange','red','black','gold','magenta','firebrick','salmon','orangered','lightsalmon','sienna','lawngreen','darkseagreen','palegoldenrod',
	'darkslategray','deeppink','crimson','mediumpurple','khaki','dodgerblue','lime','black','midnightblue',
	'lightsteelblue']

# AS relationships
C_TO_P = 1
P_TO_C = -1
P_TO_P = 0
S_TO_S = 5

