import pandas as pd
from datetime import datetime
from geopy.distance import geodesic

def splitTime(date):
    splitDate = date.split(":")
    return int(splitDate[0])*60+int(splitDate[1])*60

def calculate_speed(departure_time, arrival_time, start_coordinates, end_coordinates):
    departure_datetime = splitTime(departure_time)
    arrival_datetime = splitTime(arrival_time)

    travel_time = (arrival_datetime - departure_datetime)
    if(travel_time==0):
        travel_time = 60
    distance = geodesic(start_coordinates, end_coordinates).kilometers
    speed = distance / (travel_time/3600)

    return speed

# Wczytaj dane z pliku CSV
df = pd.read_csv('connection_graph.csv')

# Dodaj nową kolumnę z obliczoną prędkością dla każdego wiersza
df['speed'] = df.apply(lambda row: calculate_speed(row['departure_time'], row['arrival_time'],
                                                   (row['start_stop_lat'], row['start_stop_lon']),
                                                   (row['end_stop_lat'], row['end_stop_lon'])), axis=1)

# Oblicz średnią prędkość
average_speed = df['speed'].mean()

print(f"Średnia prędkość: {average_speed:.2f} km/h")



# Średnia prędkość: 19.35 km/h