# USGS API service
import requests
import os
import json
import time

class USGSService:
    """Service for interacting with the USGS Earthquake API."""
    
    def __init__(self):
        self.api_config = {
            "base_url": "https://earthquake.usgs.gov/fdsnws/event/1/query"
        }
        self.recent_requests = []

    def hit_usgs_api(self, params):

        """Hits the USGS earthquake API with the given params

        Args:
            params (json): Parameters required to hit the usgs api

        return:
            dict: JSON reponse from the USGS API
        """

        url = self.api_config['base_url']

        # return the reponse if time difference are less than 30 s
        current_time = time.time()
        for saved_params, timestamp, saved_response in self.recent_requests:
            if saved_params == params and current_time - timestamp < 30:
                print("Using local cache")
                return saved_response

        try:
            response = requests.get(url, params=params, timeout=10)
            # print("##########",response.status_code)
            if response.status_code == 200:
                earthquake_data = response.json()
                self.recent_requests.append((params.copy(), current_time, earthquake_data))

                # Cleanup the local cahe for more than 30 sec
                request_cleanup = []
                for p, t, r in self.recent_requests:
                    if current_time - t < 30:
                        request_cleanup.append((p, t, r))
                self.recent_requests = request_cleanup

                return earthquake_data
            else:
                return None
        except requests.RequestException:
            return None 

    def format_data(self, earthquake_data):

        """Formats the data recieved from the USGS API to the desired format

        Args:
            earthquake_data (json): Response from the USGS API

        Returns:
            dict: Dictionary with required data
        """

        if not earthquake_data:
            return {"total_earthquake": 0, "earthquake_data": []}
        
        earthquake_result = []
        total_earthquakes = earthquake_data['metadata']['count']

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
    
    def get_earthquake_data(self, start_time, end_time):

        """Fetch all earthquakes M2.0+ for the San Francisco Bay Area during a specific time range.
        
        Args:
            start_time (str): Start time for the data retrieval in YYYY-MM-DD format.
            end_time (str): End time for the data retrieval in YYYY-MM-DD format.
            
        Returns:
            dict: A dictionary containing earthquake data or None if the request fails.
        """

        params = {
            'starttime': start_time,
            'endtime': end_time,
            'minmagnitude': 2,
            "minlatitude": 37.050339,
            "minlongitude": -123.012400,
            "maxlatitude": 38.553120,
            "maxlongitude": -121.213351,
            'format': 'geojson'
        }
        
        earthquake_data = self.hit_usgs_api(params)

        return self.format_data(earthquake_data)

    def get_critical_earthquake_reported(self, start_time, end_time):

        """ Fetch all earthquakes M2.0+ that have 10+ felt reports for the San Francisco Bay Area during a specific time range.

        Args:
            start_time (str): Start time for the data retrieval in YYYY-MM-DD format.
            end_time (str): End time for the data retrieval in YYYY-MM-DD format.
            
        Returns:
            dict: A dictionary containing earthquake data or None if the request fails.
        """

        params = {
            'starttime': start_time,
            'endtime': end_time,
            'minmagnitude': 2,
            "minlatitude": 37.050339,
            "minlongitude": -123.012400,
            "maxlatitude": 38.553120,
            "maxlongitude": -121.213351,
            'minfelt': 10,
            'format': 'geojson'
        }

        earthquake_data = self.hit_usgs_api(params)

        return self.format_data(earthquake_data)

    def get_previous_date_tsunami_data(self, date, state):

        """ Fetches the previous days tsunami reported data for the date and specific state

        Args:
            date: Date for which data needs to be fetched
            state: State for which alerts needs to be fetched

        Return:
            dict: A dictionary containing earthquake data or None if the request fails.
        """

        if os.path.exists("us_states_data.json"):
            with open("us_states_data.json", "r") as f:
                coordinate_data = json.load(f)
                
        find_state = False
        for states in coordinate_data["states"]:
            # print(item["state"].lower())
            if states["state"].lower() == state:
                minlatitude = states["minlatitude"]
                minlongitude = states["minlongitude"]
                maxlatitude = states["maxlatitude"]
                maxlongitude = states["maxlongitude"]
                find_state = True
                break
        if not find_state:
            return {"Error": "No state found in DB"}

        
        params = {
            'starttime': date+"T00:00:00",
            'endtime': date+"T23:59:59",
            'minmagnitude': 2,
            "minlatitude": minlatitude,
            "minlongitude": minlongitude,
            "maxlatitude": maxlatitude,
            "maxlongitude": maxlongitude,
            'format': 'geojson'
        }

        # print(params)

        earthquake_data = self.hit_usgs_api(params)

        total_earthquakes = self.format_data(earthquake_data)

        tsunami_earthquake = []

        for eq in total_earthquakes["earthquake_data"]:
            if eq["tsunami"] != 0:
                tsunami_earthquake.append(eq)
            
        result = {
        "earthquake_data": tsunami_earthquake,
        "total_earthquake": len(tsunami_earthquake)
        }
        return result