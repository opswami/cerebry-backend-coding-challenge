# cerebry-backend-coding-challenge
Simple Restful api for cities suggestion based on keyword and geo location, This is for the Cerebry Coding Challenge.

# API Implementation Detail
## Frameworks
- **Django**
- **Django Rest Framework**

## Cities Data
All cities data are stores in a file in TSV(tab sepperated value) format, fetching data from there.

## City suggestion scoring
Calaculating distance using geo location data (latitude, longitude) and using this distance for giving score to any city. Nearest city will have more confidence score.

# To Run/Start App
- Create Virtual environment
- install all requirement described in requirements.txt using pip
  pip install -r requirements.txt
- run server using 
  python manage.py runserver

This API is only giving result by matching starting keywords(string keyword as city name prefix), It can be further improved by matching as substring anywhere in city name or approximate string matching and giving score for any city based on approximate string match.
