from datetime import datetime

async def test_get_forecast(cli):
    resp = await cli.get('/forecast')
    assert resp.status == 200
    json = await resp.json()
    assert 'records' in json
    assert len(json['records']) == 10


async def test_get_forecast_with_limit(cli):
    resp = await cli.get('/forecast', params={'limit': 1})
    assert resp.status == 200
    json = await resp.json()
    assert len(json['records']) == 1


async def test_get_forecast_with_offset(cli):
    resp_1 = await cli.get('/forecast', params={'limit': 1})
    resp_2 = await cli.get('/forecast', params={'limit': 1, 'offset': 1})

    assert resp_1.status == 200
    assert resp_2.status == 200

    json_1 = await resp_1.json()
    json_2 = await resp_2.json()
    assert json_1 != json_2
    date_1 = datetime.strptime(
        json_1['records'][0]['applicable_date'], '%Y-%m-%d')
    date_2 = datetime.strptime(
        json_2['records'][0]['applicable_date'], '%Y-%m-%d')
    assert date_1 > date_2


async def test_post_new_record(cli):
    data = {"applicable_date": "2018-03-05",
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
            "predictability": 80}
    await cli.delete(f"/forecast/{data['applicable_date']}")
    r = await cli.post('/forecast', json=data)
    assert r.status == 201
    assert 'success' in await r.text()




async def test_post_wrong_record(cli):
    data = {"applicable_date": "2018-03-05",
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
            "predictability": 'here should be int'}
    await cli.delete(f"/forecast/{data['applicable_date']}")
    r = await cli.post('/forecast', json=data)
    assert r.status == 500
    assert 'invalid input' in await r.text()



async def test_post_already_existing_record(cli):
    data = {"applicable_date": "2018-03-05",
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
            "predictability": 80}
    await cli.delete(f"/forecast/{data['applicable_date']}")
    r = await cli.post('/forecast', json=data)
    r = await cli.post('/forecast', json=data)
    assert r.status == 422
    assert 'exist' in await r.text()



async def test_get_forecast_to_specific_day(cli):
    today = datetime.today().replace().strftime('%Y-%m-%d')
    r = await cli.get(f'/forecast/{today}')
    assert r.status == 200
    json = await r.json()
    assert 'records' in json
    assert len(json['records']) == 1
    assert 'applicable_date' in json['records'][0]

async def test_get_forecast_to_specific_day_that_not_exist(cli):
    today = datetime.today().replace(year=1234).strftime('%Y-%m-%d')
    r = await cli.get(f'/forecast/{today}')
    assert r.status == 404
    json = await r.json()
    assert 'not found' in json

async def test_put_record(cli):
    data = {"applicable_date": "2018-03-05",
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
            "predictability": 80}
    await cli.delete(f"/forecast/{data['applicable_date']}")
    await cli.post('/forecast', json=data)
    original_date = data['applicable_date']
    test_date = datetime.today().replace(year=1970).strftime('%Y-%m-%d')
    data['applicable_date'] = test_date
    r = await cli.put(f"forecast/{original_date}", json=data)
    assert r.status == 201


async def test_put_record_that_not_exist(cli):
    data = {"applicable_date": "2018-03-05",
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
            "predictability": 80}
    await cli.delete(f"/forecast/{data['applicable_date']}")
    r = await cli.put(f"forecast/{data['applicable_date']}", json=data)
    assert r.status == 404



async def test_get_forecast_with_drop_table(cli_with_drop_table):
    resp = await cli_with_drop_table.get('/forecast')
    assert resp.status == 200
    json = await resp.json()
    assert 'records' in json
    assert len(json['records']) == 10
