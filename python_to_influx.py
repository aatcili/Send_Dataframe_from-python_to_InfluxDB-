import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from time import time, sleep

bucket = "mybucket"
org = "my_org"
token = "my_token"
# Store the URL of your InfluxDB instance
url="http://localhost:9000"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

end_time = time() + 300 # time() is calculated in seconds
y_seconds = 5 # time to sleep in seconds
while time() < end_time:
    # time to add data to database
    p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 25.1 + np.random.randn())
    sleep(y_seconds)
    write_api.write(bucket=bucket, org=org, record=p)


# Now we are done. I you want, You can check the data on your influxdb database now.
# Or you can see the results on python too
query_api = client.query_api()
query = """from(bucket:"eliardata")\
|> range(start: -10m)\
|> filter(fn:(r) => r._measurement == "my_measurement")\
|> filter(fn: (r) => r.location == "Prague")\
|> filter(fn:(r) => r._field == "temperature" )"""
result = client.query_api().query(org=org, query=query)
results = []
for table in result:
    for record in table.records:
        results.append((record.get_field(), round(record.get_value()),2))

print(results)

# Now its time to send Dataframe to InfluxDB
# Be aware, i have dataframe which has a index as time 

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point, WriteOptions
import numpy as np

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# Preparing Dataframe: 
# DataFrame must have the timestamp column as an index for the client. 
_write_client = client.write_api(write_options=WriteOptions(batch_size=1000,
flush_interval=10_000,
jitter_interval=2_000,
retry_interval=5_000))
_write_client.write("my_bucket", record=Your_dataFrame, data_frame_measurement_name='cpu',
                    data_frame_tag_columns=['cpu'])