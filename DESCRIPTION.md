# Information for the Group Study

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

## Discussion

### Organization

- How frequently must you report your results to your supervisor (usually every 3-4 weeks)?
- How frequently will you meet your supervisor (usually, there are only 2-3 meetings overall)?
- First references, basic tools, and templates you can start from (some papers, documents, frameworks, programming environments, simulation tools, templates, demo projects, etc.).
- What is the exact form of report you should have before finishing the project?
- What is the amount of written pages required for documentation of your results?

### General

- What is the main idea of the topic?
- What skills are required from you in the topic: literature study, analysis, simulations, implementation, etc.?
- What output is being expected?
- How can you divide the topic among the group members?

### Technical detaiks

#### Technologies

- What technologies you will use in the project?
- What are components of the project?
- How the components are connected?
- What are the interfaces between components?
- What are main principles of working in the project?
    - Programming
    - Testing
    - Documentation
    - Reporting 

#### Documentation

- How will we document the code? Which tools to use? (Markdown, Sphinx Doc)