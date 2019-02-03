def process_result_to_json(db_out):
    res = []
    for i in db_out:
        json = {
        'applicable_date': i[0],
        'weather_state_name': i[1],
        'weather_state_abbr': i[2],
        'wind_direction_compass': i[2],
        'created': i[4],
        'min_temp': i[5],
        'max_temp': i[6],
        'the_temp': i[7],
        'wind_speed': i[8],
        'wind_direction': i[9],
        'air_pressure': i[10],
        'humidity': i[11],
        'visibility': i[12],
        'predictability': i[13],
        }
        res.append(json)
    return res
