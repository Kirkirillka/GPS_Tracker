# Experiment 1

The first attempt took place on 12.02.2020. 

`Case 1`
We started with `Sub-Optimal` case.
One AP functioned correctly - one group of APs connection to one AP was made successfully.
Here was a problem with the second group of APs - due to weather conditions we encountered Wi-Fi
module issues of AP (the laptop freeze).

After some time of data collection, it was clear `the second AP` was not sending data to Command
Center at all, so we decided to locate devices according to Near-Optimal layout scheme.

`Case 2`
During `Near-Optimal `layout case we observed increase of RSS level -82 and -84 dBm for the left AP
to -76 and -80 dBm for the other. Link measurement messages from UEs connected to the second
AP dropped by an unknown reason.
Moreover, GPS Frontend showed that some UEs are close to each other (having approximately
the same coordinate), whereas the other 2 were detected much further. It indicates that GNSSs
position measurements are biased.
After, the second Access Point stopped working at some time. Restart and re-connection of UEs
did not help to obtain data.

`Case 3`
Because of the problems encountered in the previous case, we decided to stop the experiment and
figure out possible solutions.

`Outcome`
The first trial showed:
- Further development and bug fixes of GPS Tracker and GPS Android required.
- Tests of placement algorithms can be performed, but due to problems with message sending,
we could not prove that the suggested optimal positions would lead to better signal conditions.

As a result, we decided to:
- resolve the second AP failure reasons
- add logs to UEs
