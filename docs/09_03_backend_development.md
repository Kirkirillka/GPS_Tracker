## Decision on GPS_Frontend techniques development

### Description

The GPS_Frontend is a UI to access the functions of other components of the framework. Thus, it would have complicated behavior. The best-suited architecture for that kind of task is Single Page Application (SPA).

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

Finally, the team decided to use the Vue.js framework as the core for GPS_Frontend.

Also, there is a set of dependencies specified:

- "font-awesome" - A set of fonts.
- "@fortawesome/fontawesome-free" -  A set of fonts.
- "apexcharts" -  A library does draw figures using Web.
- "axios" -  A library to work with HTTP(S) requests.
- "bootstrap" -   An open-source toolkit/framework for developing with HTML, CSS, and JS.
- "bootstrap-vue" -  A wrapper to use Bootstrap components natively in Vue.js.
- "core-js" - A standard library to extend the number of components and operation.
- "d3v4" - level JavaScript library for manipulating documents based on data using HTML, SVG, CSS.
- "d3-colorbar" -  An extension to d3 library to work with colors.
- "jquery" - rich JavaScript library.
- "moment" -  A convenient library to work with time.
- "pc-bootstrap4-datetimepicker" -  a DatetimePicker component compatible with Bootstrap.
- "plotly.js-dist" -   A library does draw figures using Web.
- "portal-vue" -  A Vue component to render your component's template anywhere in the DOM.
- "underscore" - A JavaScript library that provides a whole mess of useful functional programming helpers without extending any built-in objects.
- "vue" -  The Progressive JavaScript Framework to build the web application.
- "vue-apexcharts" -  A wrapper to use ApexChart components natively in Vue.js.
- "vue-axios" -  A wrapper to use Axios components natively in Vue.js.
- "vue-bootstrap-datetimepicker" - datetimepicker components natively in Vue.js.
- "vue-router" -  An router extension to Vue.js.
- "vuex" -  A storage library extension to Vue.js.

### Status

Accepted

### Consequences

Advantages:

- We received a well-designed, good-looking and user-friendly UI.
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
