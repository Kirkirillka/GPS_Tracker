## Experiment 3. 07.02.2020 

Took place on 27.02.2020

This time the aim was to check how **2 major updates** of the Android app behave.

The *first* one concerned usage of HTTP requests instead of MQTT. The reason for it is that all previously detected issues related to MQTT in one way or another.

The *second* update was about complete refactoring of the code. It included not only start following MVVM architectural pattern but also removing of redundant 'Connect' button, as well as real-time interaction with the app in the way that coordinates updates the display when 'Push continuously' is enabled.

### Procedure

Due to the bad weather (heavy snowfall), we decided to experiment indoor (Mensa has enough space inside). 1 CnC, 1 AP, and 3 UEs took part.

All UEs can connect successfully:

- 'Push once' button pressed
- deviceId assigned
- UE coordinates displayed

### Tips

As for 'Push continuously', it should be known in advance the coordinates updated on the display **only in the case of moving to some minimal delta** (10 centimeters). This is insured based on GPS values passed by the Android device.

To make sure the connection is still alive, and the values transferred, it makes sense to check logging messages in logs/log.txt

### Outcome

All in all, the system finally started working as expected, and the meaningful set of data collected:

![Movement trajectory of connected phones](images/experiment_3_1.jpg){ width=50% }

![Signal quality map](images/experiment_3_2.jpg){ width=50% }

![Signal quality changes](images/experiment_3_3.jpg){ width=50% }
