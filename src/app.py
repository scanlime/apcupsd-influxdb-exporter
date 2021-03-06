#!/usr/bin/python
import os
import platform
import time
from influxdb import InfluxDBClient
from apcaccess import status as apc


# Try to pull the hostname
HOSTNAME = platform.node()
try:
  HOSTNAME = os.getenv('HOSTNAME', 'meatwad')
except:
  pass

# Run APCACCESS
#os.system('apcaccess > .apcupsd_output.txt')

# Debug

# Send to influxdb

dbname = os.getenv('INFLUXDB_DATABASE', 'upsnew')
user = os.getenv('INFLUXDB_USER', '')
password = os.getenv('INFLUXDB_PASSWORD', '')
port = os.getenv('INFLUXDB_PORT', 8086)
host = os.getenv('INFLUXDB_HOST', '10.0.1.11')
apc_host = os.getenv('APC_HOST', 'localhost')
client = InfluxDBClient(host, port, user, password, dbname)

print "Hostname: ", HOSTNAME
print "database name: ", dbname
print "db host:", host
#print ups

while True:
  ups = apc.parse(apc.get(host=apc_host), strip_units=True)
  if os.environ['WATTS']:
    ups['NOMPOWER'] = os.environ['WATTS']
  json_body =  [
                      {
                          'measurement': 'APC-NEW',
                          'fields': {
                              'BCHARGE' : float(ups['BCHARGE']),
                              'TONBATT' : float(ups['TONBATT']),
                              'TIMELEFT' : float(ups['TIMELEFT']),
                              'NOMPOWER' : float(ups['NOMPOWER'])
                          },
                          'tags': {
                              'host': HOSTNAME
                          }
                      }
                  ]
  if 'LOADPCT' in ups:
    watts = float(float(ups['NOMPOWER']) * float(0.01 *float(ups['LOADPCT'])))
    json_body[0]['fields'].update({
      'WATTS': float(watts),
      'LOADPCT' : float(ups['LOADPCT']),
    })

  print json_body
  print client.write_points(json_body)
  time.sleep(5)
