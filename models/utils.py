def process_result_to_json(db_out):
    res = []
    for i in db_out:
        json = {
        'applicable_date': i['applicable_date'],
        'weather_state_name': i['weather_state_name'],
        'weather_state_abbr': i['weather_state_abbr'],
        'wind_direction_compass': i['wind_direction_compass'],
        'created': i['created'],
        'min_temp': i['min_temp'],
        'max_temp': i['max_temp'],
        'the_temp': i['the_temp'],
        'wind_speed': i['wind_speed'],
        'wind_direction': i['wind_direction'],
        'air_pressure': i['air_pressure'],
        'humidity': i['humidity'],
        'visibility': i['visibility'],
        'predictability': i['predictability'],
        }
        res.append(json)
    return res
