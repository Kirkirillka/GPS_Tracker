# Experiment 1

The first attempt took place on 27.02.2020. 

We aimed to check how `2 major updates` of the Android app behave.

The `first` update concerns the usage of HTTP requests instead of MQTT. 
We suspected that MQTT-protocol is the reason of previously detected issues.

The `second` update is to refactor the source code. It includes switching to Model-View-ViewModel
(MVVM) architectural pattern, removing of insignificant interface components.


Due to the bad `weather` conditions (heavy snowfall), we decided to perform experiments indoor
(Mensa). Mensa is a 2-floor building in TU Ilmenau, it has a large area inside.
The layout included 1 Command Center, 1 AP, and 3 UEs took part.


`Consideration during the experiment`
As for 'Push continuously', it should be known in advance the coordinates updated on the display
only in the case of moving to some `minimal delta` (10 centimeters). This is insured based on
GNSS values passed by the Android device.
To make sure the connection is still alive and the values are transferred, we checked the `log
journal` periodically.

`Outcome`
To sum up, the system finally `started working` without failures and the meaningful set of data is
collected

`Figires`
The *first* figure shows movement trajectory of connected clients.

The *second* shows how signal changes in different location inside Mensa. Due to obstacles (concrete
walls, metal objects), the signal rapidly decreases in the farthest corners and on the second 
oor.

*Signal quality* figure describes changes in RSS while UEs were moving inside the building. It is clear to
observe that some phones started transmitting later than others. If a UE fails to send a measurement
message, it stores in a local database and resends once the connection is back.