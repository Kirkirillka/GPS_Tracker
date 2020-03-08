# Crosscutting concepts

## GPS_Android

|Used approach|Reason|
|---|---|
|In case if a message cannot be sent it saved in the local SQLite database. In the next iteration, the app first tries to send saved messages | If there is a poor signal quality that will help to save the measurement to resend them after connection become better.|

## GPS_Tracker

|Used approach|Reason|
|---|---|
|Used Worker pattern| `Celery` workers allow to parallelize task execution. |
|MQTT Broker as Message Broker|MQTT Protocol is a lightweight reliable protocol for IoT intended application|
|MongoDB as storage for message|Use NoSQL MongoDB increase development velocity as well as performance, especially for JSON-formatted data.|

## GPS_Frontend

|Used approach|Reason|
|---|---|
|Backend is built on Flask Python Web Framework|Flask is a light, easy-to-use framework that requires a little effort but highly extensible.|
|Frontend app is built using Vue.js framework|Vue.js is perfectly suited for fast development but still has good design and extensions.|
