import db
import tile38
import asyncio
from datetime import datetime, timedelta
import telegram

report_time = datetime.now()
yesterday = report_time - timedelta(days = 1)

def write_out_park_events(park_events):
    result = ""
    for index, park_event in enumerate(park_events, 1):
        system_id = park_event["system_id"]
        number_of_open_park_events = park_event["number_of_park_events"]
        result += "{}. {} - {}\n".format(index, system_id, number_of_open_park_events)
    return result

def write_out_rentals(rentals):
    result = ""
    for index, park_event in enumerate(rentals, 1):
        system_id = park_event["system_id"]
        number_of_open_park_events = park_event["number_of_trips"]
        result += "{}. {} - {}\n".format(index, system_id, number_of_open_park_events)
    return result

def write_out_stats_tile38(counts):
    data = {k: v for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True)}
    result = ""
    index = 1
    for operator_id, number_of_vehicles in data.items():
        result += "{}. {} - {}\n".format(index, operator_id, number_of_vehicles)
        index += 1
    return result

def count_vehicles_per_operator_tile38(vehicle_ids):
    result = {}
    for vehicle_id in vehicle_ids:
        operator_id = vehicle_id.split(":")[0]
        if operator_id not in result:
            result[operator_id] = 0
        result[operator_id] += 1
    return result

def get_missing_feeds_from_import(tile38_result, feeds_that_should_be_active):
    missing_feeds = [] 
    for row in feeds_that_should_be_active:
        system_id = row["system_id"]
        if system_id not in tile38_result:
            missing_feeds.append(system_id) 
    return missing_feeds
        

number_of_open_park_events = db.get_park_events()
tile38_result = asyncio.run(tile38.get_vehicles())
counts = count_vehicles_per_operator_tile38(vehicle_ids=tile38_result)
number_of_finished_trips = db.get_trips(yesterday)
active_feeds = db.get_feeds_that_should_be_active()
missing_data = get_missing_feeds_from_import(tile38_result, active_feeds)

result = ""
result += "* Dagelijkse rapportage {} * \n\n".format(report_time.strftime("%d-%m-%Y %H:%M"))

result += "*Let op\\!* geen data van de volgende feeds: " + ", ".join(missing_data) + "\n"

result += "Openstaande park_events: \n"
result += write_out_park_events(park_events=number_of_open_park_events) + "\n\n"

result += "Aantal voertuigen in openbare ruimte tile38: \n"
result += write_out_stats_tile38(counts) + "\n\n"

result += "Aantal verhuringen {}:".format(yesterday.strftime("%d-%m-%Y")) + "\n"
result += write_out_rentals(number_of_finished_trips)

telegram.send_telegram_msg(result, -716168993)

print(result)
