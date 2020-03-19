# Experiment 4

The first attempt took place on 03.03.2020. 

The `weather` conditions were appropriate for the experiment, although there was raining lightly.

For the fourth trial, we implement sending of measurement messages `only with HTTP` protocol
from UE to Command Center.

We aimed to find optimized positions for the UEs in `three cases` (Sub-Optimal, Uniform, Near-
Optimal).
We decided to reduce the area layout to 25x25 meters.
We use one smartphone with a special program that can precisely locate the position. Then we
placed the phone where UEs and APs were, which helped us to find out the initial positions.

The experiment is divided into four parts:
- Before 11:05 - Sub-Optimal case
- 11:05 - 11:08 - Uniform case
- 11:08 - 11:12 - Near-Optimal case
- 11:12 - 11:15 - Sub-Optimal to compare the suggested positions


`Case 1`
The first case is the most `profitable from the signal quality` point of view. The APs are implicitly
located at the same distance from the connected UEs. Signal changes can be seen in Figure -
despite this case is expected to have the best link parameters, RSS is unstable for UEs, possible
reason for this - differences in phone generations, e.g. modern phones also include more advanced
Wi-Fi model.

Despite the APs were located close to UEs, the RSS level varies noticeably. However, only in
this case the speed and signal quality measurement were the `most stable` among all cases.

`Case 2`
In the Uniform case, the APs are located with equal distance from the Command Center.

Figure depicts RSS changes in Uniform case. Link measurement is more steady and keeps on
the same level for the majority of UE, however, we encountered speed test failed.

`Case 3`
The third Near-optimal case simulates the situation where the APs are placed uniformly 
far from centers of UEs clusters.

Figure demonstrates that measured `RSS lower` than in Uniform case because of larger distance
between APs and UEs approximately on 10-15 dBm.

`Outcome`
The HTTP protocol helped to receive messages reliably, despite there were connection failures, we
observed that the `farther UE` is located from AP, the less is probable reception of the message.

Retransmission of messages implemented in GPS Android partly mitigated losses.
We found out that network speed measurements were not significant, because there was markedly
seen the difference between uplink and downlink speed, uplink tests threw timeout exception in
case of the larger distance between a UE and a Access Point, because the communication took longer
and the session terminated.