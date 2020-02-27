# Introduction and Motivation

The successful placement of an aerial base station requires knowledge of the locations of the user equipment. This data must be collected continuously to provide up-to-date information for a placement algorithm. 

To prepare the experimental evaluation of the placement of the aerial base stations, the framework for the performance analysis needs to be developed.

## Requirement Overview 

Its main objective is to receive the GPS location data from several Android-based telephones that send this data via UDP sockets.

The site data collector must store the received data in an internal database and then make this data available to the placement algorithm. Another part of this framework is the performance evaluation module, which sends the data over the network and records the amount of data sent.

It is required to have a system that can receive from clients information about their GPS coordinates and Wi-Fi signal quality.
Based on this information, an optimization algorithm must be applied, which predicts how to change the position of the Wi-Fi station to increase capacity concerning all connected clients.
