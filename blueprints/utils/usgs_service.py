# USGS API service
import requests

class USGSService:
    """Service for interacting with the USGS Earthquake API."""
    
    def __init__(self):
        self.api_config = {
            "base_url": "https://earthquake.usgs.gov/fdsnws/event/1/query"
        }
    
    def get_earthquake_data(self, start_time, end_time):
        """Fetch earthquake data from the USGS API.
        
        Args:
            start_time (str): Start time for the data retrieval in YYYY-MM-DD format.
            end_time (str): End time for the data retrieval in YYYY-MM-DD format.
            
        Returns:
            dict: A dictionary containing earthquake data or None if the request fails.
        """
        url = self.api_config['base_url']

        params = {
            'starttime': start_time,
            'endtime': end_time,
            'minmagnitude': 2,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'maxradiuskm': 48.2,
            'format': 'geojson'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                earthquake_data = response.json()
                # print(earthquake_data)
            else:
                return None
        except requests.RequestException:
            return None

        if not earthquake_data:
            return {"total_earthquake": 0, "earthquake_data": []}
        
        earthquake_result = []
        total_earthquakes = earthquake_data['metadata']['count']
        # print("Toatalquaked: ", total_earthquakes)

        for feature in earthquake_data["features"]:
            properties = feature["properties"]
            data_consolidated = {
                "magnitude": properties["mag"],
                "place": properties["place"],
                "time": properties["time"],
                "url": properties["url"],
                "tsunami": properties["tsunami"],
                "type": properties["type"]
            }
            earthquake_result.append(data_consolidated)

        result = {
            "total_earthquake": total_earthquakes,
            "earthquake_data": earthquake_result
        }

        return result
