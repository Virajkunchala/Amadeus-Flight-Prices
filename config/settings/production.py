from .base import *
DEBUG = False
ALLOWED_HOSTS = ['*']

AMADEUS_API['TOKEN_URL'] = 'https://test.api.amadeus.com/v1/security/oauth2/token'
AMADEUS_API['FLIGHT_OFFERS_URL'] = 'https://test.api.amadeus.com/v2/shopping/flight-offers'