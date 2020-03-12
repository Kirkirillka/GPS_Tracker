# 2. Experiment requirement

## Hardware Equipment

- 6 cellphones with Android OS (version 5.0 and above).
  A dedicated GPS and Wi-Fi modules.
- 3 external Wi-Fi Adapters with AP mode capable.
  - Model: AWUS036NEH
  - Antenna's height for CnC: 17.2 cm
  - Antenna's height for AP: 11 cm
- 3 Laptops.
- One ruler.
- Optionally, 6-10 carton bags for hardware safety against the weather.

## Software Equipment

### For UEs

- Android-enabled smartphone (version 5.0 and above).
  - `Magic Perf` installed.
- `GPS_Android` installed.

### For Command Center (CnC)

- Host OS
  - Any Debian-based OS (Debian, Ubuntu, etc.).
  - `VirtualBox` + `VirtualBox Extention Pack` latest version.
  - `Python3` + `Ansible` installed.
  - `openssh-server`.
- The virtual CnC machine
  - `dnsmasq`, `hostapd` installed.
  - `openssh-server` installed.
  - `docker` and `docker-compose` installed.
    - MongoDB container.
    - RabbitMQ container.
    - Mosquitto MQTT broker container.
    - Python3 container.
    - nginx container.
    - nodeJS container.

### For APs

- Host OS
  - Any Debian-based OS (Debian, Ubuntu, etc.).
  - `dnsmasq`, `hostapd` installed.
  - `iperf3` installed.
  - `openssh-server` installed.
  - `docker` and `docker-compose` installed.
    - An FTP server container (e.g. VSFTPd).
