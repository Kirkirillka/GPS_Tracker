# Experimentation description

The main purpose of the experiment is to optimize the location of Access Points in such a way that
`network throughput` and `Received Signal Strength (RSS)` of User Equipments (UEs) is maximized.

We have 3 laptops: two APs and one Command Centers.
`Command Center` use external Wi-Fi adapter to set up wireless point for `APs` to access provided
services. Each has two Wi-Fi adapters: one used to set up Wi-Fi access point for UEs, the second
(internal, built in the vast majority of modern laptops) adapter is used for connection to Command
Center.

From the general system engineering perspective, the experiment is a set of `wireless-connected
nodes` (via Wi-Fi 802.11n (300 Mbps)) which measures the receiving signal strength and measure
the throughput of the link to upload and download.
Preliminary tests in default layout showed one `restriction` on experiment activity: network
bandwidth between UE and measurements with iperf3 showed about 30 MBit/s speed rate. On
the contrary, speed on the bearer UE - Command Center showed about 12-15 MBit/s speed
rate. This is significant drop in network rate, probably, because of transmission on the radio channel
two-times. The `problem` here is that radio link has higher error rate due to interference and fading
than wired connection, so we should measure the closest radio link to the UEs (bearer UE - AP),thus
FTP-server placed in AP.
Each UE has GPS Android installed. Access Point create a Wi-Fi access point named "ap".
Command Center runs a wireless point named "cnc".