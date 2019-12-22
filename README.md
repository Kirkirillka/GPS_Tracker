# RCSE WS19/20 Group Study: Performance analysis framework for base station placement using IEEE 802.11

## Early access

Now it is possible to run a Proof-of-Concept of the system. The PoC is taking into considering:

- Visualization is done by offline Jupyter Python Notebook ([here](/datavisual/gps_visualize.ipynb))
- Instead of a real ClientApp, there is a mock client class - RealisticWIFIPayloadGenerator, which is running as a part
of PoC.
- Data producing by RealisticWIFIPayloadGenerator is not truly realisitic, especially in GPS location, but produced RSSI
is taken by a formula visualized [here](/datavisual/try_to_find_handy_func.ipynb).

To start up the PoC, you should check if you have Docker and docker-compose installed:

```bash
docker version
docker-compose --version
``` 

If they are installed, first you need get required base images or build them from Dockerfiles:

```bash
docker-compose pull
docker-compose build
```
 
Then type:

```bash
docker-compose up -d
```

Docker will run:

- MongoDB NoSQL database - to store records.
- Eclipse Mosquitto MQTT Message Broker - to be a bus for components.
- DataBroker - to receive messages from MQTT bus and save it in the Storage.
- RealisticWIFIPayloadGenerator - to generate testing data.
- DataVisual - a simple HTTP API backend, if you need integration.

After docker is done, you can havigate to the [notebook](datavisual/gps_visualize.ipynb) and run the cells.

## Available pages

- [Information on the project](DESCRIPTION.md)
- [Project Documentation](docs/README.md)
- [Extra information to keep in mind while working](extras/README.md)
