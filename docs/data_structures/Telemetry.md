# Telemetry data between GPS devices and server


Current data schema: **JSON**

Example of schema of data transferred from GPS devices to server:


```json
{
  "time": "2019-10-26 17:18:46.847521",
  "device": {
    "id": "0c7f856e-d084-4633-8a08-990447db67b6",
    "type": "smartphone"
  },
  "data": [
    {
    "type": "gps",
    "longitude": 567982.52,
    "latitude": 5936090.19,
    "payload": [
      {
        "cell_network_name": "Deutsche Telecom",
        "cell_basestation_name": "be37a3c5-07fe-445e-972a-0bf9027a921a",
        "cell_signal_level": -93 
      }
    ]
    }
  ]
}
```