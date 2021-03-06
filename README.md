### Meta weather API 

Python app that get the weather data from https://www.metaweather.com/ for Saint-Petersburg for last month and present the results with restful api. 


Prerequisites:
  `Docker`


```
-> make
help:            Show available options with this Makefile.    
clean_all:       Clean the docker-container, venv etc.      
clean_venv:      Clean the venv.                            
test:            Run all the tests with pylint.                                  
install_dep:     Setup venv and install the application.                                
run:             Run the application with simple aiohttp server.           
dev_run:         Run application in a dev mode, where gunicorn workers will reload the application on every change.  
```

---
### Usage:

To get records. Default limit is 10

POST here to add new one.

```
curl --request GET  http://0.0.0.0:8080/forecast

curl --request POST \ 
    --data '{"applicable_date": "2019-02-05",
            "weather_state_name": "Thunder",
            "weather_state_abbr": "t",
            "wind_direction_compass": "SW",
            "created": "2019-02-05T10:37:07.697840Z",
            "min_temp": 1.7433333333333334,
            "max_temp": 4.693333333333333,
            "the_temp": 7.775,
            "wind_speed": 8.135003832255627,
            "wind_direction": 230.9926706186993,
            "air_pressure": 1026.5149999999999,
            "humidity": 89,
            "visibility": 4.682963990296667,
            "predictability": 80}'\
    http://0.0.0.0:8080/forecast
```

Specify limit of output:
```
curl --request GET http://0.0.0.0:8080/forecast?limit=5
```
Set offset:
```
curl --request GET http://0.0.0.0:8080/forecast?limit=5&offset=10
```
to get forecast for specific day:

DELETE or PUT also here to delete or change record

````
curl --request GET http://0.0.0.0:8080/forecast/YYYY-MM-DD 

curl --request DELETE http://0.0.0.0:8080/forecast/YYYY-MM-DD 

curl --request PUT \ 
    --data '{"applicable_date": "2019-02-05",
            "weather_state_name": "Thunder",
            "weather_state_abbr": "t",
            "wind_direction_compass": "SW",
            "created": "2019-02-05T10:37:07.697840Z",
            "min_temp": 1.7433333333333334,
            "max_temp": 4.693333333333333,
            "the_temp": 7.775,
            "wind_speed": 8.135003832255627,
            "wind_direction": 230.9926706186993,
            "air_pressure": 1026.5149999999999,
            "humidity": 89,
            "visibility": 4.682963990296667,
            "predictability": 80}'\
    http://0.0.0.0:8080/forecast/2019-02-05
````
