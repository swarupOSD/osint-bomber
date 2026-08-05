"""
GeoIP Location Checker
Finds the geographical location of a URL/IP address
"""

import requests
import json

class GeoIPChecker:
    def __init__(self):
        # Free IP Geolocation API
        self.api_url = "http://ip-api.com/json/{}"
    
    def get_location(self, url):
        """Extract IP from URL and get location"""
        try:
            # Extract domain from URL
            import re
            domain = re.sub(r'^https?://', '', url)
            domain = domain.split('/')[0].split(':')[0]
            
            # Get IP address
            try:
                import socket
                ip = socket.gethostbyname(domain)
            except:
                return None
            
            # Get location from API
            response = requests.get(self.api_url.format(ip), timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    return {
                        'ip': ip,
                        'country': data.get('country', 'Unknown'),
                        'city': data.get('city', 'Unknown'),
                        'region': data.get('regionName', 'Unknown'),
                        'lat': data.get('lat', 0),
                        'lon': data.get('lon', 0),
                        'isp': data.get('isp', 'Unknown'),
                        'timezone': data.get('timezone', 'Unknown')
                    }
            return None
        except Exception as e:
            return None
    
    def get_all_locations(self, results):
        """Get locations for all URLs in results"""
        locations = {}
        for site, url in results.items():
            location = self.get_location(url)
            if location:
                locations[site] = location
        return locations