# Experiment 1

The first attempt took place on 22.02.2020.

This time the aim was to test `changes` in the system components:
- A new way to estimate uplink and downlink `speed` added in GPS Android using File Transport
Protocol (FTP) (ability to specify IP address for Command Center (CnC) in the app)
- `Logging` capabilities in GPS Android
- Improvements in GPS `Frontend` (the uplink/downlink throughput measurements plot, figures
became more informative).

The goal is to perform an reduced experiment with 1 Command Center, 1 AP, and 3 UEs with
the same settings from the previous experiment but with modified components.
The second AP did not participate because of troubles with Wi-Fi Access Point installation
drivers (later the update to Debian 11 Testing fixed this problem).

Only `Near-Optimal` case was performed.
To exclude possible bottleneck because of additional wireless bearer between AP and Command
Center, we tried to measure the direct connection to cnc in short distance 

All UEs can connect to Command Center successfully:
- deviceId assigned
- UE coordinates displayed

During the first half of the experiment, after pressing the 'push once' button we received 
up-link/downlink throughput measurements, however, the values of uplink seemed to be `too high`

Wi-Fi standard (300 000 kBit/s) compared to downlink (1000-2000 kBit/s).
Later, pressing 'push once' button again did not cause speed re-estimation, the messages from
UEs did not reach Command Center. The log journal did not contain any error messages.

`Outcome`
The second attempt was also not successful. We had not managed to solve the problem in measured
data sending. For the next iteration, we proposed to implement some design improvements.

As a `result`, we decided to:
- Add logging capabilities to APs.
- Implement direct Hyper Text Transfer Protocol (HTTP) requests and retire Message Queuing
Telemetry Transport (MQTT) broker architecture.