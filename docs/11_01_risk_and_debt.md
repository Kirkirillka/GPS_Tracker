# Risk and technical debt

|Number|Description|
|---|----------|
|1|There is still a lack of testing in both GPS_Frontend and GPS_Tracker.|
|2|Currently, MQTT enabled protocol is not stable in GPS_Android, we haven't figured out why GPS_Tracker sometimes doesn't correctly receive messages, requires to find out the reason why. So, better to rely on HTTP protocol sending method.|
|3|GPS_Frontend might have a long list of unnecessary dependencies that influences the final size of code supplied to users.|
|4|Android programming requires some pattern to be followed. Since there are limitations of programming approaches to be used as well as lack of proper programming experience, GPS_Android should be reviewed and optimized.|
|5|After "push continuously", switching off that button actually doesn't stop background task, therefore there is still task to test speed and send messages|
|6|"Simplex" estimation method cannot converge for 2 clusters and produce the unreliable result|
Table: Risk and technical debt description.
