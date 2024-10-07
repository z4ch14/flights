import pandas as pd
from flask import Flask, jsonify, request
import requests
from api_flight import process_flight_data

"""
this is an example for sort the csv and fill the "success" column
"""
df = pd.read_csv('flights.csv')

# Process the updated DataFrame and save it to the CSV file
new_flights = process_flight_data(df)
new_flights.to_csv('flights.csv', index=False)

"""
this is an example for the api that send the information about a flight

if you go to the url "http://your_api_endpoint/flights/A12" for example you will get the information 
for the flight A12 and you will get 
[
  {
    "Arrival": "09:00:00",
    "Departure": "13:00:00",
    "flight ID": "A12",
    "success": "success"
  }
]

and for "http://your_api_endpoint/flights/G88"

[
  {
    "Arrival": "09:30:00",
    "Departure": "14:00:00",
    "flight ID": "G88",
    "success": "success"
  },
  {
    "Arrival": "11:30:00",
    "Departure": "14:05:00",
    "flight ID": "G88",
    "success": "fail"
  }
]
"""



"""
this is an example for the api that get a new flight
"""
url = "http://your_api_endpoint/flights"  # Replace with the actual endpoint
data = [{
    "flight ID": "L123",
    "Arrival": "09:00",
    "Departure": "13:00",
    "success": ""
}]

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Flight submitted successfully!")
else:
    print("Error submitting flight:", response.text)