1. ClientApp is an mobile phone application that has GPS and Wifi modules on the board. 
2.Messages sent over from ClientApps.
3. ClientApp can directy push a message to DataBackend via HTTP
4. MessageBroker offer convinient protocol  with an abstract queue, to access data in 
the order they arrived.
5. DataBroker is responsible for normalizing data from clients and store it in internal DB.
6. Backend serves Requests from all Frontends. It is an external API entrypoint to the system.
7. DataVisualizer has the visualization mechanisms to show metrics and analysis results in convenient format.
8. Storage provides the interface to fetch and store metrics, results of Analyzer computations
9. Analyzer modules are responsible to define and solve a problem.
