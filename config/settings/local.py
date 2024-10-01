from .base import *
from decouple import config

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

AMADEUS_API['TOKEN_URL'] = 'https://test.api.amadeus.com/v1/security/oauth2/token'
AMADEUS_API['FLIGHT_OFFERS_URL'] = 'https://test.api.amadeus.com/v2/shopping/flight-offers'


