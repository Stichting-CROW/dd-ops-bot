from db_helper import db_helper
from datetime import timedelta

def get_park_events():
    stmt = """
        SELECT system_id, COUNT(*) as number_of_park_events
        FROM park_events 
        WHERE end_time IS NULL 
        GROUP BY system_id 
        ORDER BY COUNT(*) DESC;
    """
    with db_helper.get_resource() as (cur, _):
        cur.execute(stmt)
        return cur.fetchall()

def get_trips(date):
    start_of_day = date.replace(hour= 0, minute= 0)
    end_of_day = start_of_day + timedelta(days = 1)
    stmt = """
        SELECT system_id, COUNT(*) as number_of_trips
        FROM trips 
        WHERE end_time >= %s
        AND end_time < %s
        GROUP BY system_id 
        ORDER BY COUNT(*) DESC;
    """
    with db_helper.get_resource() as (cur, _):
        cur.execute(stmt, (start_of_day, end_of_day))
        return cur.fetchall()

def get_feeds_that_should_be_active():
    stmt = """
        SELECT DISTINCT(system_id) 
        FROM feeds 
        WHERE is_active = true;
    """
    with db_helper.get_resource() as (cur, _):
        cur.execute(stmt)
        return cur.fetchall()