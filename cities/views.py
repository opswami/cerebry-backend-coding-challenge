from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import re
from math import sin, cos, sqrt, atan2, radians


cities_file_path = './data/cities_canada-usa.tsv'
@api_view(['GET',])
def get_cities(request):
	'''
		API to get Cities suggestion list based on the query parameters
		Mandatory Fields : q - search string to get cities suggestion
		Optional Fields : latitude - search location Latitude to get more accurate suggestions
						  longitude - search location Longitude to get more accurate suggestions
	'''
	# Collecting Query params from request data
	searchString = request.GET.get('q', None)
	latitude = request.GET.get('latitude', None)
	longitude = request.GET.get('longitude', None)

	if not searchString :
		return Response({"error": "Please provide search parameter"}, status=status.HTTP_404_NOT_FOUND)
	# Getting Cities data from cities database file
	cities_names, cities_data = get_cities_data()

	# Regex to match queryString with cities name list
	r = re.compile("^%s+"%searchString, re.IGNORECASE)
	relavent_cities = list(filter(r.match, cities_names))

	result_cities_data = {}
	cities_suggestions = []
	for city_name in relavent_cities:
		cities_suggestions.append(cities_data[city_name])

	# Calculating City score if latitude and longitude is present in the request
	min_distance = None
	if latitude and longitude :
		# calculating each city geodistance  based on lat long in request
		lat1 = float(latitude)
		long1 = float(longitude)
		for index, city_data in enumerate(cities_suggestions):
			lat2 = float(city_data['lat'])
			long2 = float(city_data['long'])
			geo_distance = get_distance_using_coordinate(lat1, long1, lat2, long2)
			if not min_distance or min_distance > geo_distance:
				min_distance = geo_distance
			cities_suggestions[index]['geo_distance'] = geo_distance
		# calculating each city score based on calculated geodistance
		for index, city_data in enumerate(cities_suggestions):
			geo_distance = city_data['geo_distance']
			score = min_distance/geo_distance
			cities_suggestions[index]['score'] = "%0.1f" %score
	cities_suggestions = sorted(cities_suggestions, key = lambda i: i['score'],reverse=True) 
	result_cities_data['suggestions'] = cities_suggestions
	return Response(result_cities_data)

def get_cities_data():
	'''
		Getting Cities data from cities database file and storing them in a dictionary
		return : List with names of the cities, Dictionary of cities data
	'''
	cities_data_fp = open(cities_file_path, 'r')
	header_line = cities_data_fp.readline().replace("\n", '')
	headers = header_line.split('\t')
	line = cities_data_fp.readline().replace("\n", '')
	cities_data = {}
	cities_names = []
	while line :
		row_city_data = line.split("\t")
		city_data = {}
		city_data[headers[0]] = row_city_data[0]
		city_data[headers[2]] = row_city_data[2]
		city_data[headers[4]] = row_city_data[4]
		city_data[headers[5]] = row_city_data[5]
		city_data[headers[8]] = row_city_data[8]
		cities_data[row_city_data[2]] = city_data
		cities_names.append(row_city_data[2])
		line = cities_data_fp.readline().replace("\n", '')
	return cities_names, cities_data

def get_distance_using_coordinate(lat1, long1, lat2, long2) :
	'''
		Calculate distance two Geo coordinates latitude and longitude
		return : distance in KM
	'''
	# approximate radius of earth in km
	R = 6373.0

	lat1 = radians(lat1)
	long1 = radians(long1)
	lat2 = radians(lat2)
	long2 = radians(long2)

	dlong = long2 - long1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlong / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	return R*c