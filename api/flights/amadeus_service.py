import requests
from django.conf import settings
from django.core.cache import cache
from retrying import retry
import logging
import time
import redis

logger = logging.getLogger(__name__)
TOKEN_CACHE_KEY = 'amadeus_access_token'
TOKEN_EXPIRY_MARGIN = 300  #refreshing this token 5 mints before expiry 

class AmadeusAPI:
    def __init__(self):
        """Fetching the token from cache and get the expiry time"""
        self.token = None
        self.redis_client = redis.StrictRedis(host='redis', port=6379, db=0)  # Update Redis config if needed
        self.token_key = TOKEN_CACHE_KEY
        
        # Attempt to fetch the token from cache and its expiry time
        self.token = cache.get(self.token_key)
        self.token_expiry = cache.get("amadeus_token_expiry")
        
        if self.token is None or self.token_expiry <= time.time():
            logger.info("No valid cached token found, fetching a new one.")
            self.fetch_amadeus_access_token()
        else:
            logger.info("Using cached Token")
            

    def fetch_amadeus_access_token(self):
        """Fetches a new access token from the Amadeus API."""
        logger.info("Fetching a new Amadeus access token")
        token_url = settings.AMADEUS_API['TOKEN_URL']
        payload = {
            "grant_type": "client_credentials",
            "client_id": settings.AMADEUS_API_KEY,
            "client_secret": settings.AMADEUS_API_SECRET
        }
        
        try:
            
            response = requests.post(token_url, data=payload)
            response.raise_for_status()
            token_data=response.json()
            self.token = token_data['access_token']
            expires_in = token_data.get('expires_in',1800)
            self.token_expiry =time.time()+expires_in
            logger.info(f"Token will expire in: {expires_in} seconds")
            #Cache the token with its expiration time
            cache.set(TOKEN_CACHE_KEY,self.token,timeout=expires_in)
            cache.set("amadeus_token_expiry",self.token_expiry,timeout=expires_in)
            
            logger.info("Fetched new access token")
        except requests.exceptions.RequestException as e:
            logger.error(f"error fetching the access token:{str(e)}")
            raise Exception("Failed to obtain the access token") from e
        
    def get_access_token(self):
        """get the current access token,it will fetch the new one if its already expired"""
        if self.token is None or (self.token_expiry - TOKEN_EXPIRY_MARGIN) <= time.time():
            logger.info("Access token is either None or expired, fetching a new one.")
            self.fetch_amadeus_access_token()
            
        return self.token
        
    @retry(stop_max_attempt_number=5, wait_exponential_multiplier=1000, wait_exponential_max=10000)  
    def fetch_flight_offers(self,origin, destination, departureDate, adults=1, max_results=1,nocache=False):
        """Fetch the flight prices from amadeucs API"""
        # Construct the cache key based on the request parameters
        cache_key = f"flight_offers_{origin}_{destination}_{departureDate}_{adults}_{max_results}"

        # Check if nocache is not set, attempt to retrieve from cache
        if nocache or nocache=='1':
            logger.info("Nocache is set. Bypassing cached flight offers.")
             # Fetch a new access token if nocache is set
            self.fetch_amadeus_access_token()
        else:
            cached_data = cache.get(cache_key)
            if cached_data:
                logger.info("Using cached fetch flight offers.")
                return cached_data

        
        token = self.get_access_token()
        flight_offers_url = settings.AMADEUS_API['FLIGHT_OFFERS_URL']
        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departureDate,
            "adults": adults,
            "max": max_results,
            "currencyCode": "INR"
        }
        
        try:
            response = requests.get(flight_offers_url, headers=headers, params=params)
            logger.info(f"Making request to {flight_offers_url} with headers and params: {params}")
            response.raise_for_status()
            flight_data = response.json()
            # Cache the result for 10 minutes (600 seconds)
            cache.set(cache_key, flight_data, timeout=600)
            return flight_data
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching flight offers: {str(e)}")
            raise Exception(f"Error fetching flight offers:{str(e)}") from e
    
