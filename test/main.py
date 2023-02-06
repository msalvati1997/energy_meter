import influxdb_client
import pandas as pd 
import uuid 

if __name__=="__main__":
    url="http://127.0.0.1:8086"
    client = influxdb_client.InfluxDBClient(url=url,org="")
    query_api = client.query_api()
    power_query="from(bucket:\"powerapi_formula\") |> range(start: -1d) |> filter(fn: (r) => r._measurement == \"power_consumption\" and r._field == \"power\") |> group(columns: [\"target\"])"
    wh_energy="from(bucket:\"powerapi_formula\") |> range(start: -1d) |> filter(fn: (r) => r._measurement == \"power_consumption\" and r._field == \"power\" )|> integral(unit: 1h)"
    id =str(uuid.uuid4())

    df = pd.DataFrame(query_api.query_csv(power_query))
    df.to_csv("sysbench_power"+id+".csv", encoding='utf-8')

    df = pd.DataFrame(query_api.query_csv(wh_energy))
    df.to_csv("sysbench_energy"+id+".csv", encoding='utf-8')
    print("saved to csv")