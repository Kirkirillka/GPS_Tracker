1. ClientApp is an mobile phone application that has GNSS and Wifi modules on the board. Wifi network status is sent with GPS coordinates.
2.Messages sent over from ClientApps.
3. ClientApp can directy push a message to DataBackend via HTTP
4. MessageBroker offer convinient protocol  with an abstract queue, to access data in 
the order they arrived.
5. DataBroker is responsible for normalizing data from clients and store it in internal DB. Potentially, DataBroker can send information from Storage to ClientApps via MessageBroker.
6. Backend serves Requests from all Frontends. It is an external API entrypoint to the system. No direct interaction with internal components are allowed.
7. DataVisualizer has the visualization mechanisms to show metrics and analysis results in convenient format. Also contains operation menu interface.
8. Storage provides the interface to fetch/store metrics from ClientsApp, results of Analyzer computations, any system or application information required for the project.
9. Analyzer modules are responsible to define and solve a problem. To solve the problem, Analyzer requires information from ClientApps. Analyzer can store the result in Storage as well. The result (directive to change Tx power, for example) can be propaganted by to Clients App.
