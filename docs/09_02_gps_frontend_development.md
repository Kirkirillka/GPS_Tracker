## Decision on GPS_Tracker techniques development

### Description

The GPS_Tracker is a UI to access the functions of other components of the framework. Thus, it would have complicated behavior. The best-suited architecture for that kind of task is Single Page Application (SPA). 

There are many possible web frameworks exist that may help to build SPA applications but the most famous and functional are:

- Angular
- React
- Vue.js

### Decision

Only one person in the team had experience developing a web application with the Vue.js framework.

The team member discussed and decided that:

- Angular has reach functionality, but too complex for that task.
- React is more flexible, but requires more time to get working in.
- Vue.js is a simple framework with excellent documentation but has a lack of components in the default configuration. It requires additional libraries and components to design required functions.

Finally, the team decided to use the Vue.js framework as the core for GPS_Tracker.

Also there is a set of dependencies specified:

- "font-awesome": "^4.7.0" - A set of fonts.
- "@fortawesome/fontawesome-free": "^5.11.2" - A set of fonts.
- "apexcharts": "^3.10.1" - A library do draw figures using Web.
- "axios": "^0.19.0" - A library to work with HTTP(S) requests.
- "bootstrap": "^4.3.1" -  An open source toolkit/framework for developing with HTML, CSS, and JS.
- "bootstrap-vue": "^2.1.0" - A wrapper to use Bootstrap components natively in Vue.js.
- "core-js": "^3.3.2"- An standard library to extend the number of components and operation.
- "d3v4": "^4.2.2" - A high-level JavaScript library for manipulating documents based on data using HTML, SVG, CSS.
- "d3-colorbar": "0.0.1" - An extension to d3 library to work with colors.
- "jquery": "^3.4.1" -  A fast, small, and feature-rich JavaScript library.
- "moment": "^2.24.0" - A convenient library to work with time.
- "pc-bootstrap4-datetimepicker": "^4.17.50" - a DatetimePicker component compatible with Bootstrap.
- "plotly.js-dist": "^1.51.2" -  A library do draw figures using Web.
- "portal-vue": "^2.1.6" - A Vue component to render your component's template anywhere in the DOM.
- "underscore": "^1.9.1" - A JavaScript library that provides a whole mess of useful functional programming helpers without extending any built-in objects.
- "vue": "^2.6.10" - The Progressive JavaScript Framework to build web application.
- "vue-apexcharts": "^1.5.1" - A wrapper to use ApexChart components natively in Vue.js.
- "vue-axios": "^2.1.5" - A wrapper to use Axios components natively in Vue.js.
- "vue-bootstrap-datetimepicker": "^5.0.1" - A wrapper to use bootstrap4-datetimepicker components natively in Vue.js.
- "vue-router": "^3.1.3" - An router extension to Vue.js. 
- "vuex": "^3.1.2" - A storage library extension to Vue.js.

### Status

Accepted

### Consequences

Advantages:

- We received a well designed, good-looking  and user-friendly UI.
- It can be easily changed and adapted to new requirements.
- Rich set of features and further development.
- High SPA performance.
- UI can be accessed easily from different devices, good portability. 

Disadvantages:

- The difficulty of data analysis in JavaScript, that language probably is not the best suit for that kind of task.
- Some very complex figures (like Heatmap) may busy the whole program drawing a large dataset.
- Due to the big number of components, the JS code compilation takes a relatively long time.
- Dependency on the user's web browser.
- Vue.js is a young project, it may suffer a lack of functions provided by more matured frameworks.
