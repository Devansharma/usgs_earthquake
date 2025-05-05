# Extending USGS API

This project extends the [USGS](https://earthquake.usgs.gov/fdsnws/event/1/) API for different functionalities.

## State co-ordinates Assumptions
For the states co-ordinates we have taken rectangular co-ordinates as following:
| State | Min Latitude | Min Longitude | Max Latitude | Max Longitude |
|-------|-------------|--------------|-------------|--------------|
| Alabama | 30.145127 | -88.473227 | 35.008028 | -84.888246 |
| Alaska | 51.175092 | -179.148909 | 71.441059 | -129.974525 |
| Arizona | 31.332177 | -114.818710 | 37.004260 | -109.045223 |
| Arkansas | 33.004106 | -94.617919 | 36.499767 | -89.644395 |
| California | 32.528832 | -124.482003 | 42.009517 | -114.131211 |
| Colorado | 36.992426 | -109.060253 | 41.003444 | -102.041524 |
| Connecticut | 40.980144 | -73.727775 | 42.050587 | -71.786994 |
| Delaware | 38.451013 | -75.788658 | 39.839007 | -75.048939 |
| Florida | 24.396308 | -87.634938 | 31.000888 | -80.031362 |
| Georgia | 30.355757 | -85.605165 | 35.000659 | -80.839729 |
| Hawaii | 18.910361 | -178.334698 | 28.402123 | -154.806773 |
| Idaho | 41.988057 | -117.243027 | 49.001146 | -111.043564 |
| Illinois | 36.970298 | -91.513079 | 42.508481 | -87.494756 |
| Indiana | 37.771742 | -88.097892 | 41.760592 | -84.784579 |
| Iowa | 40.375501 | -96.639704 | 43.501196 | -90.140061 |
| Kansas | 36.993016 | -102.051744 | 40.003162 | -94.588413 |
| Kentucky | 36.497129 | -89.571203 | 39.147458 | -81.964971 |
| Louisiana | 28.855127 | -94.043147 | 33.019457 | -88.817017 |
| Maine | 43.064817 | -71.084497 | 47.459686 | -66.949895 |
| Maryland | 37.911717 | -79.487651 | 39.723043 | -75.048939 |
| Massachusetts | 41.237964 | -73.508142 | 42.886589 | -69.928393 |
| Michigan | 41.696118 | -90.418136 | 48.306063 | -82.122971 |
| Minnesota | 43.499356 | -97.239209 | 49.384358 | -89.491739 |
| Mississippi | 30.173943 | -91.655009 | 34.996052 | -88.097888 |
| Missouri | 35.995683 | -95.774704 | 40.613640 | -89.098843 |
| Montana | 44.358221 | -116.050003 | 49.001390 | -104.039138 |
| Nebraska | 39.999998 | -104.053514 | 43.001708 | -95.308290 |
| Nevada | 35.001857 | -120.005746 | 42.002207 | -114.039648 |
| New Hampshire | 42.696952 | -72.557247 | 45.305476 | -70.610621 |
| New Jersey | 38.928519 | -75.559614 | 41.357423 | -73.893979 |
| New Mexico | 31.332301 | -109.050173 | 37.000232 | -103.001964 |
| New York | 40.496103 | -79.762152 | 45.015861 | -71.856214 |
| North Carolina | 33.842316 | -84.321869 | 36.588117 | -75.460621 |
| North Dakota | 45.935054 | -104.048881 | 49.000574 | -96.554507 |
| Ohio | 38.403202 | -84.820159 | 41.977523 | -80.518693 |
| Oklahoma | 33.615833 | -103.002565 | 37.002206 | -94.430662 |
| Oregon | 41.991794 | -124.566244 | 46.292035 | -116.463504 |
| Pennsylvania | 39.719798 | -80.519891 | 42.269860 | -74.689516 |
| Rhode Island | 41.146339 | -71.862772 | 42.018798 | -71.120132 |
| South Carolina | 32.034550 | -83.353928 | 35.215402 | -78.499301 |
| South Dakota | 42.479635 | -104.057698 | 45.945362 | -96.436589 |
| Tennessee | 34.982972 | -90.310298 | 36.678118 | -81.646946 |
| Texas | 25.837377 | -106.645646 | 36.500704 | -93.508292 |
| Utah | 36.997968 | -114.052962 | 42.001567 | -109.041058 |
| Vermont | 42.726853 | -73.437741 | 45.016659 | -71.464555 |
| Virginia | 36.540738 | -83.675395 | 39.466012 | -75.242266 |
| Washington | 45.543541 | -124.763068 | 49.002494 | -116.915989 |
| West Virginia | 37.201483 | -82.644739 | 40.638801 | -77.719519 |
| Wisconsin | 42.491983 | -92.888114 | 47.080621 | -86.805415 |
| Wyoming | 40.994746 | -111.056888 | 45.005904 | -104.052154 |

## San Francisco Bay Area co-ordinates Assumption
| Parameter | Value |
|-----------|------|
| `minlatitude` | 37.050339 |
| `minlongitude` | -123.012400 |
| `maxlatitude` | 38.553120 |
| `maxlongitude` | -121.213351 |

## Steps for running the project
1. Clone the repo
    ```sh
    git clone https://github.com/Devansharma/usgs_earthquake.git
    ```
2. Install metrics server on the cluster and disable TLS connection
    ```sh
    kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
    kubectl patch deployment metrics-server -n kube-system   --type='json' -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
    ```
3. Start the deployment on the Kubernetes cluster
    ```sh
    cd usgs_earthquake
    kubectl apply -f k8s_manifests/all.yaml
    ```
    This will create the deployment as well as nodeport service on nodeport `30007`
    
4. Check the status of the pods, all pods should be in running state
    ```sh
    kubectl get pods -n usgs
    ```
    
5. Check the status of the HPA
    ```sh
    kubectl get hpa -n usgs
    ```
## API Response Structure
### Response Format
```json
{
  "earthquake_data": [
    {
      "magnitude": 4.7,
      "place": "49 km SW of Karluk, Alaska",
      "time": 1393343789483,
      "tsunami": 1,
      "type": "earthquake",
      "url": "https://earthquake.usgs.gov/earthquakes/eventpage/ak0142kvd03o"
    }
  ],
  "total_earthquake": 1
}
```
#### Field Descriptions
##### Root Level
At root level response contains 2 fields
| Field | Description |
|-------|-------------|
| `earthquake_data` | An array of earthquake event objects |
| `total_earthquake` | Total count of earthquake events in the response |

##### Earthquake Event Object
Each event in the `earthquake_data` array contains the following fields:
| Field | Description |
|-------|-------------|
| `magnitude` | Earthquake magnitude on the Richter scale |
| `place` | Description of earthquake location |
| `time` | Unix timestamp in milliseconds (epoch time) |
| `tsunami` | Tsunami warning indicator (1 = warning issued, 0 = no warning) |
| `type` | Event type (typically "earthquake") |
| `url` | Link to detailed information about the event |
## New extended APIs

1. Retrieve all earthquakes M2.0+ for the San Francisco Bay Area during a specific time range.
    ```/api/earthquake/data```
    Arguments required API
    ```/api/earthquake/data?start_time=YYYY-MM-DD&end_time=YYYY-MM-DD```
    eg: 
    ```sh
    curl "http://<NodeIP/hostname>:30007/api/earthquake/data?start_time=2023-01-25&end_time=2023-01-31"
    ```
    > In above example <NodeIP/hostname> with the Node IP or HostName
    
    Response:
    ```json
    {
        "earthquake_data": [
        {
            "magnitude": 4.7,
            "place": "49 km SW of Karluk, Alaska",
            "time": 1393343789483,
            "tsunami": 1,
            "type": "earthquake",
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/ak0142kvd03o"
        }
        ],
        "total_earthquake": 1
    }
    ```


2. Retrieve all earthquakes M2.0+ that have 10+ felt reports for the San Francisco Bay Area during a specific time range.
    ```/api/earthquake/critical```
    Arguments required API
    ```/api/earthquake/critical?start_time=YYYY-MM-DD&end_time=YYYY-MM-DD```
    eg: 
    ```sh
    curl "http://<NodeIP/hostname>:30007/api/earthquake/critical?start_time=2023-01-23&end_time=2023-01-31"
    ```
    > In above example <NodeIP/hostname> with the Node IP or HostName
    
    Response:
    ```json
    {
        "earthquake_data": [
        {
            "magnitude": 3.62,
            "place": "9km ENE of San Martin, CA",
            "time": 1674482282950,
            "tsunami": 0,
            "type": "earthquake",
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/nc73836266"
        }
        ],
        "total_earthquake": 1
    }
    ```
    
3. Retrieve all earthquakes M2.0+ for the past day that had tsunami alerts for any given [US state](https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States).
    ```/api/earthquake/tsunami```
    Arguments required API
    ```/api/earthquake/tsunami?date=YYYY-MM-DD&state=state_name```
    eg: 
    ```sh
    curl "http://<NodeIP/hostname>:30007/api/earthquake/tsunami?date=2014-02-26&state=alaska"
    ```
    > In above example <NodeIP/hostname> with the Node IP or HostName
    
    Response:
    ```json
    {
        "earthquake_data": [
        {
            "magnitude": 4.7,
            "place": "49 km SW of Karluk, Alaska",
            "time": 1393343789483,
            "tsunami": 1,
            "type": "earthquake",
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/ak0142kvd03o"
        }
        ],
        "total_earthquake": 1
    }
    ```
    > For ```/api/earthquake/tsunami``` if the state name consists of a white space like ```New Mexico```, it should be passed as ```NewMexico```
    
## Addional Functionalities

1. Endpoint for health check.

   ```api/earthquake/health```

    This API returns a json object as:
    
    ```json
    {
        "status": "healthy"
    }
    ```
    
2. Custom metrics using prometheus client: THis contains counter prometheus metric that keeps count of total requests to the endpoints and also the number of success and failed API requests
    ```api/earthquake/metrics```
    This API returns a prometheus text document
    
3. Added Horizontal Pod Scaling which monitors the CPU Utlization, and scales the pods when CPU Utilization increases by 75%. Minimum Replicas have been set to 2 and maximum till 5