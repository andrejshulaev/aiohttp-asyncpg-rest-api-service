#### API usage


Before run:
```
docker-compose -f docker-compose.yml up -d
virtualenv meta
source meta/bin/activate
cd meta && sudo pip install -r requirements.txt
```
To run:
```
python server.py
```

To get records for last 10 days.

POST here to add new one.

```
curl http://0.0.0.0:8080/forecast
```

Specify limit of output:
```
curl http://0.0.0.0:8080/forecast?limit=5
```
Set offset:
```
curel http://0.0.0.0:8080/forecast?limit=5&offset=10
```
to get forecast for specific day:

DELETE or PUT also here to delete or change record

````
http://0.0.0.0:8080/forecast/YYYY-MM-DD 
````