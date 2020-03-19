# Kirill part

## GPS_Frontend

Now we will describe User Interface part we wrote to work with data - GPS_Frontend.

This is a modern single-page application wrote with web technologies.

Main components we use are:

- VueJS - a Javascript web framework, the skeleton of application
- Vuex - a unite data storage to share between components
- Vuerouter - URL path routing
- Plotly - to plot figures
- Bootstrap - an open-source toolkip, to make UI good looking.

### Why VueJS

VueJS is an extensible Javascript framework.

Main features:

- Low size of library
- Extensibility
- Reactivity - bound view elements and data sources
- Easy-to-use
- Clear documentation

We had three possible candidates to use to build the UI.

- Angular has rich functionality, but too complex for that task.
- React is more fexible, but requires more time to get working in.
- Vue.js is a simple framework with an excellent documentation but has a lack of components in the default conguration. It requires additional libraries and components to design required functions.

### Key points

- Model-View-ViewModel architecture pattern
- Parallel execution, asyncronous calls
- Reactivity (Observer pattern)
- Extensibility

## GPS_Tracker

A set of backend programms intended to serve user requiests, process incoming messages from GPS_Androi and perform optimization tasks.

Key technologies

- Worker design pattern
- Python language
  - Flask Web framework
  - numpy, sklearn, algorithms provided by supervisor
  - Celery task queue
- MongoDB NoSQL
- RabbitMQ

The GPS Tracker is implemented in Python language. This is a dynamic interpreting language. That is known the performance is not so perfect compared to
static compiled languages, but it has higher changeability property.

To summarize, there is a set of problems:

- Possible performance degradation.
- Ambiguous interfaces, more safe checks.
- Parallel execution, scalability is not so high.