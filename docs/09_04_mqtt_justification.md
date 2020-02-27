### Consideration on the protocol used to send data from GPS_Android

### Description

During the group study solution design it became clear that
our system needs **a mediator** which can 
control incoming messages. In particular:
- avoid loss of messages
- provide the availability to many devices at once 
- provide smooth transmission to the processing subsystem

![mqtt-justification](mqtt-justification.png){ width=50% }

### Decision

As a result, MQTT was selected for the reasons:
- fitting to criterion above
- reliability
- lightweight

### Status

Accepted


### Consequences

MQTT is a reliable and lightweight protocol, however, it requires additional component (DataBroker) to fetch incoming messages from MQTT topics to normalize data and save it in the data store. In the first two experiment attempt, we encountered the problem when messages sent over MQTT have not arrived. We had no glue if it was the consequence of the MQTT protocol used.

Thus, the **alternative design** based on HTTP excluding MQTT was implemented as well to be more flexible during the experimental part of the project.
