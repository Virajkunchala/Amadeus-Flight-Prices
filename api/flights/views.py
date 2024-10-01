import requests
import logging
from datetime import datetime,timedelta
from django.core.cache import cache
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .amadeus_service import AmadeusAPI
from .serializers import FlightOfferSerializer
from rest_framework import status
import redis

# Create a logger
logger = logging.getLogger('api_logger')


class FlightOffersView(APIView):
    """
    API endpoint to end get the flight offers.
    """ 
    amadeus_api = AmadeusAPI()
    def get(self, request):
        serializer=FlightOfferSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
        ##Extract parameters
        validated_data = serializer.validated_data
        origin = serializer.validated_data['origin']
        destination = serializer.validated_data['destination']
        departureDate = serializer.validated_data['departureDate']
        adults = serializer.validated_data['adults']
        max_results = serializer.validated_data['max']
        nocache = serializer.validated_data.get('nocache', False)

        
        
        try:
            # Fetch flight offers
            flight_data = self.amadeus_api.fetch_flight_offers(origin, destination, departureDate, adults, max_results,nocache)
            
            if not flight_data.get('data'):
                return Response({"message":"No flight offers found"},status=status.HTTP_404_NOT_FOUND)
            
            # Find the cheapest flight
            cheapest_offer=self.find_cheapest_offer(flight_data['data'])
            response_data=self.final_response(origin, destination, departureDate, cheapest_offer)
            logger.debug(f"sucessful response:{response_data}")
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("An error occurred while fetching flight offers.")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def find_cheapest_offer(self,offers):
        """Find the chepest from the response"""
        return min(offers,key=lambda x: float(x['price']['total']))
    
    def final_response(self, origin, destination, departureDate, offer):
        """Forming the final response from the API"""
        return {
            "data": {
                "originLocationCode": origin,
                "destinationLocationCode": destination,
                "departureDate": departureDate,
                "price": f"{offer['price']['total']} {offer['price']['currency']}"
            }
        }
        
        
class Pingview(APIView):  
    """Ping endpoint to check service availability."""
    def get(self,request):
        return Response({"data": "pong"})
    
class HealthCheckView(APIView):
    """Health check endpoint for the application."""
    def get(self, request):
        try:
            # Check Redis connection
            r = redis.StrictRedis(host='redis', port=6379, db=0)
            r.ping() 
            return Response({"status": "healthy"}, status=status.HTTP_200_OK)
        except redis.ConnectionError:
            return Response({"status": "unhealthy", "details": "Cannot connect to Redis"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)