# RCSE WS19/20 Group Study: Performance analysis framework for base station placement using IEEE 802.11

## Supervisor
Oleksandr Andryeyev

## Description

The successful placement of an aerial base station requires knowledge of the locations of the user equipment. This data must be collected continuously to provide up-to-date information for a placement algorithm. In order to prepare the experimental evaluation of the placement of the aerial base stations, the framework for the performance analysis needs to be developed.
Its main objective is to receive the GPS location data from several Android-based telephones that send this data via UDP sockets.
The site data collector must store the received data in an internal database and then make this data available to the placement algorithm. Another part of this framework is the performance evaluation module, which sends the data over the network and records the amount of data sent.

## Tasks

- Write a Python program that receives UDP datagrams with GPS data from terminals, decodes them and stores them in an internal database;
- write a Python program that sends the data over the network;
- validate the functionality of the developed program in the real environment using a WiFi (IEEE 802.11) communication link;
- Perform multiple experiments, tune the transmit/receive parameters, and analyze the capacity and robustness of the connection.
- develop a simple GUI interface to visualize the data in real-time.