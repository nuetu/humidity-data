# Humidity Data
A python extraction tool which gathers multiple sources of data and combines them into a singular row on a .csv file, to eventually be used by a machine learning script to set the humidifier mist power level which will keep my room at a perfectly steady humidity reading. 

If using pyVesync and you have a veSync enabled smart humidifier, create file python.py, and add these lines:

python.py 
> email = "your_email@email.com"

> password = "vesyncPassword"

This tool extracts local weather data from the Caldwell, NJ airport, parses to save:
- outdoor temperature 
- outdoor humidity

From your humidifier it extracts:
- indoor humidity
- mist power level

From python library datetime: 
- date
- time

Currently I do not own an indoor smart thermometer or have a setup enabled to gather: 
- indoor temperature 
