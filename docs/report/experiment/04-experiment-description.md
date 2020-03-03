# 4. Experiment description.

## General perspective

![Main perspective of the experiment](<images/Deployment Diagram-Free-structure_scheme.png>){width=75%}

From the general system engineering perspective, the experiment is a set of wireless-connected nodes (via Wi-Fi protocol) which measures the receiving signal strength and measure the throughput of the link to upload and download.

All connections are wireless on each bearer:

- UE <-> AP.
- AP <-> CnC.

There investigated one problem: the experimental network bandwidth between UE and AP measurements with `iperf3` showed about **30 MBit/s** speed rate. On the contrary, the speed on the bearer UE <- AP -CnC> showed about **12-15 MBit/s** speed rate. There is markedly seen a drop in speed rate, probably, because of transmission on the radio channel two-times. The problem not in the Wi-Fi itself, but the radio link is not as reliable, as a cord one, so the active bandwidth measurement part must be located as close to the APs as possible - in our case, the server-side `iperf3` is located in APs.

Each UE has two programs on board:

- `GPS_Android` - special software designed to perform RSS and link measurements with linked to GPS coordinates.
- `Magic iperf` - a network bandwidth measurement software. Provides a user-friendly interface to client-side app `iperf` on Android phones.

Each APs has two Wi-Fi adapters. Since we use laptops to run APs, they expected to have one already included, thus one external extra required for each AP. The internal Wi-Fi adapter connects to the CnC provided Wi-Fi network, the external Wi-Fi adapter creates the access point named "**ap**" for the UEs.

The CnC uses one external AP to create the access point named "**cnc**".

## Deployment Diagram

| Component                      | Description                                                                                                                                     |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Android smartphone group (UEs) | A set of smartphones running Android OS (version 5.0+) with dedicated Wi-Fi and installed software.                                              |
| Access points (APs)            | The computers running a Wi-Fi AP software for the UEs connection. Pass traffic through to CnC and take part in RSS and link quality measurement. |
| Command Center (CnC)           | A computing node running the optimization software. Should be provided with sufficient hardware resources.                                      |

Table: The main deployed components.

From the deployment view, we are using a complicated combination of software and hardware.

We prefer to run AP and designed software separately in a virtual machine. That helps to automate development, testing, and maintenance routines.

![Deployment Diagram](images/Deployment%20Diagram-Deployment_Diagram.png){width=75%}

### Command center deployment (CnC)

The CnC software runs on Debian OS in VirtualBox virtual machine. `GPS_Tracker` `GPS_Frontend` are designed to run in containers. For the experiment, the virtual machine has **docker** and **docker-compose** installed to run these containers. We don't consider much performance decrease as long as enough hardware resources provided for the CnC virtual machine.

The AP software consists of two packages:

- `hostapd` - software to manage and run Wi-Fi access points.
- `dnsmasq` - DNS/DHCP server, to provide an IP address, routing and DNS information via DHCP protocol.

The AP software starts in the virtual machine. To access the physical external Wi-Fi adapter the hardware pass through from the host machine to the virtual machine via hypervisor is used.

For easy-to-run configuration and deployment of the CnC, there are provided an **Ansible** script and a **Vagrantfile**. See their requirements to use.

### Access Points deployment (APs)

Unlike CnC, physical nodes runs the AP software and server-side `iperf3` app.

## Network Diagram

The APs subnet have identical settings. These `Wi-Fi HotSpot Network` has an internal DHCP server to provide dynamic addresses for connected UEs. To prevent the network IP addresses collisions and simplify routing, the APs perform masquerading (SNAT/DNAT) on the output interface (the internal interface used to connect to CnC). On the one side, it cannot access the UEs directly from CnC, but the UEs will always reach CnC as long as DHCP sets the default gateway IP address. 

In `Wi-Fi CnC Network` installed another DHCP server. It used to reply to connecting APs with dynamic addresses. Because the subnet used in this network is different from the internal Wi-Fi adapter's network in the APs, there is no network collision.

Finally, the UEs can access the static CnC address `192.168.20.1` as well as its local AP's gateway address `192.168.10.1`.

![Network Diagram](images/Deployment%20Diagram-Network_Diagram.png){width=75%}

## Experiment Steps

The following steps will be executed for each described experimental case:

| No  | Step                                                                     | Description                                                                                                       |
| ----- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| 1   | Initialize network connectivity between APs and CnCs                     | Ensure that these nodes are available in the network by the ICMP protocol                                         |
| 2   | Run the software for the experiment                                      | Startup GPS_Tracker, GPS_Frontend                                                                                 |
| 3   | Place the APs and UEs according to an experiment case                    | There are specific predefined positions for each element on the experiment area.                                  |
| 4   | Measure RSS, Link quality for the initial layout                         | Measurements are done via GPS_Android that sends the result to GPS_Tracker                                        |
| 5   | Run the APs location optimization for each algorithm in GPS_Tracker      | Each optimization algorithm can produce different probable positions for the same UEs positions and measurements. |
| 6   | Move the APs to the optimized positions                                  | It is expected that new positions for APs would increase our network efficiency.                                  |
| 7   | Repeat RSS and Link quality measurements for the optimized APs positions | 1-3 interactions for optimization per each case.                                                                   |  |
Table: Steps for one experimental case.
