# fixme - add exception handling
def insert_rec_to_db(mydb, mycursor, weather_info, container_version):
    """
    Insert record into database
    :param weather_info:
    :return:
    """
    try:
        sql = "INSERT INTO actual (" \
          "ts_local, " \
          "ts_utc, " \
          "julian, " \
          "hour_utc, " \
          "location, " \
          "main, " \
          "description, " \
          "pressure, " \
          "wind_speed, " \
          "wind_deg, " \
          "wind_quadrant, " \
          "wind_rose, " \
          "wind_strength, " \
          "wind_gust, " \
          "temp, " \
          "feels_like, " \
          "dew_point, " \
          "uvi, " \
          "humidity, " \
          "visibility, " \
          "rain, " \
          "snow, " \
          "coverage, " \
          "met_source, " \
          "lat, " \
          "lon, " \
          "location_code, " \
          "condition_code, " \
          "synopsis, " \
          "synopsis_code, " \
          "light, " \
          "light_condition, " \
          "alert_sender, " \
          "alert_event, " \
          "tz, " \
          "tz_offset, " \
          "ts_epoch, " \
          "sunrise_local, " \
          "sunset_local," \
          "image_name, " \
          "video_name, " \
          "container_version" \
          ") " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        val = (
           weather_info['ts_local'],
           weather_info['ts_utc'],
           weather_info['julian'],
           weather_info['hour_utc'],
           weather_info['location'],
           weather_info['main'],
           weather_info['description'],
           weather_info['pressure'],
           weather_info['wind_speed'],
           weather_info['wind_deg'],
           weather_info['wind_quadrant'],
           weather_info['wind_rose'],
           weather_info['wind_strength'],
           weather_info['wind_gust'],
           weather_info['temp'],
           weather_info['feels_like'],
           weather_info['dew_point'],
           weather_info['uvi'],
           weather_info['humidity'],
           weather_info['visibility'],
           weather_info['rain'],
           weather_info['snow'],
           weather_info['coverage'],
           weather_info['met_source'],
           weather_info['lat'],
           weather_info['lon'],
           weather_info['location_code'],
           weather_info['condition_code'],
           weather_info['synopsis'],
           weather_info['synopsis_code'],
           weather_info['light'],
           weather_info['light_condition'],
           weather_info['alert_sender'],
           weather_info['alert_event'],
           weather_info['tz'],
           weather_info['tz_offset'],
           weather_info['ts_epoch'],
           weather_info['sunrise_local'],
           weather_info['sunset_local'],
           weather_info['image_name'],
           weather_info['video_name'],
           container_version
           )

        mycursor.execute(sql, val)
        mydb.commit()
        print('uuid=' + weather_info['uuid'] + ', ' + mycursor.rowcount.__str__() + ' record inserted into MetMini Actual table OK')

    except Exception as e:
        log_msg = 'insert_rec_to_db() : uuid=' + weather_info['uuid'] + ', error : ' + e.__str__()
        print(log_msg)
