### Why MongoDB?

In the beginning of our group study it was clear that 
all messages from UEs must have been stored for further 
processing/representation in a graphical way in CnC.

There were some **aspects** leading us in our way of choice:
- message structure is changed as the project is growing
- json message type is dictated by Python usage
- availability is more important than consistency (ACID)
- queries must be fast to collect and represent data in real-time 
- easy to integrate and use

## Outcome
As a result, MongoDB was selected for the reasons:
- Rustam has experience of using it
- fits aspects listed above more than other databases