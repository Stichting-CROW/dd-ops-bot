from tile38_helper import tile38_helper

async def get_vehicles():
    with tile38_helper.get_resource() as tile38_redis_client:
        response = tile38_redis_client.execute_command("SCAN vehicles LIMIT 100000 IDS")
        result = [s.decode("utf-8") for s in response[1]]
        return result
