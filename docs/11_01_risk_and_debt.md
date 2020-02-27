# Risk and technical debt

|Number|Description|
|---|---|
|1|There is still lack of testing in both GPS_Frontend and GPS_Tracker.|
|2|Currently, MQTT enabled protocol is not stable in GPS_Android, we haven't figured out why some of messages are not received in GPS_Tracker, requires to find out the reason why. So, better to rely on HTTP protocol sending method.|
|3|GPS_Frontend might have a long list of unnecessary dependencies that influences the final size of code supplied to users.|
|4|Android programming requires some pattern to be followed. Since there are limitations of programming approaches to be used as well as lack of proper programming experience, GPS_Android should be reviewed and optimized.|