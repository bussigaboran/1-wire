#!/usr/bin/env python3
"""
This program reads 1-wire sensors from and OWFS mounted file system.
It stores the readings in an sqlite3 database
"""

import datetime
import os
import socket
import sqlite3
import time
from matplotlib import pyplot as plt

sensor_path = '/mnt/1wire/'
base_dir = '~/report/git/1-wire/'
log_path = base_dir + 'log/'
dbfile = os.path.expanduser(log_path + 'temperature.db')


def connect_to_database(fname):
    """ connect to sqlite3 database with tellstick sensor readings """
    if os.path.isfile(fname) is not False:
        db = sqlite3.connect(fname)
        c = db.cursor()
        return db, c


def db_list_sensors(c):
    """ Get list of temperature and humidity sensors from database """
    sql = "SELECT DISTINCT name FROM sensors"
    c.execute(sql)
    sensor_list = c.fetchall()
    return sensor_list


def current_time():
    """ returns a string on the format 2020-06-11 00:00:00 
        containing the current time """
    now = datetime.datetime.now()
    time_string = now.strftime('%Y-%m-%d 00:00:00')
    return time_string


def date_week_ago():
    """ returns a time string with the date from 7 days ago 
        on the format 2020-06-11 00:00:00. The time is set to
        00:00:00 """
    now = datetime.datetime.now()
    week_ago = now - datetime.timedelta(days=7)
    time_string = week_ago.strftime('%Y-%m-%d 00:00:00')
    return time_string


def date_week_ago():
    """ returns a time string with the date from 7 days ago
        on the format 2020-06-11 00:00:00. The time is set to
        00:00:00 """
    now = datetime.datetime.now()
    week_ago = now - datetime.timedelta(month=1)
    time_string = week_ago.strftime('%Y-%m-%d 00:00:00')
    return time_string


def weekly_data(c, name, sensor_type):
    week_ago = date_week_ago()
    now = current_time()
    # select * from sensors where name = 'garage' and timestamp
    # BETWEEN '2020-06-14 0 9:52:00'  and '2020-06-14 10:00:00';
    query = (f'select {sensor_type} from sensors where '
             f'name = {name} and '
             f'timestamp BETWEEN "{week_ago}" and "{now}"')
    c.execute(query)
    rows = c.fetchall()
    return rows


def weekly_data(c, name, sensor_type):
    week_ago = date_week_ago()
    now = current_time()
    # select * from sensors where name = 'garage' and timestamp
    # BETWEEN '2020-06-14 0 9:52:00'  and '2020-06-14 10:00:00';
    query = (f'select {sensor_type} from sensors where '
             f'name = {name} and '
             f'timestamp BETWEEN "{week_ago}" and "{now}"')
    c.execute(query)
    rows = c.fetchall()
    return rows


def generate_graph(sensor_name, reading, time_period):
    """ Plot sensor data given the provided parameters
        sensor_name, reading, time_period """
    fig = plt.figure()
    graph = fig.add_subplot(111)
    fig.suptitle(sensor_name)
    fig.autofmt_xdate()
    y1 = [value for (timestamp, value) in reading]
    x0 = [timestamp for (timestamp, value) in reading]
    x1 = matplotlib.dates.datestr2num(x0)
    graph.plot_date(x=x1, y=y1, fmt="r-", label=sensor_name)
    plt.ylabel("Temperature")
    if 'borken' in socket.gethostname():
        fname = "/usr/share/nginx/www/tmp/%s.png" % sensor_name
    else:
        fname = base_dir + 'graphs/%s.png' % sensor_name
    plt.savefig(fname, facecolor="#C2CEFF")

    device = {}
    sensor_id, sensor_type, name = sensor.split(':')
    fhandle = open(sensor_path + sensor_id + '/' + sensor_type, 'r')
    value = fhandle.read()
    fhandle.close()
    device['sensor_id'] = sensor_id
    device['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
    device['name'] = name
    if sensor_type == 'temperature':
        device['temperature'] = value
    if sensor_type == 'humidity':
        device['humidity'] = value
    return device


def main():
    db, c = connect_to_database(dbfile)
    sensor_list = db_list_sensors(c)
    print(weekly_data(c, 'carport', 'temperature'))
    generate_graph("freezer", "temperature", "month")
    #plot("garage", "temperature", "month")
    #plot("carport", "week")
    print(date_week_ago())
    db.close()


if __name__ == '__main__':
    main()
