## Decision on the storage component - MongoDB

### Description

At the beginning of our group study it was clear that
all messages from UEs must have been stored for further
processing/representation in a graphical way in CnC.

We decided to use the NoSQL MongoDB database to store messages.

There were some **aspects** leading us in our way of choice:

- the message structure is changed as the project is growing
- The JSON message type is dictated by Python usage
- availability is more important than consistency (ACID)
- queries must be fast to collect and represent data in real-time
- easy to integrate and use

### Decision

As a result, MongoDB was selected for the reasons:

- Rustam has experience of using it
- fits aspects listed above more than other databases

### Status

Accepted

### Consequences

- The query language used in MongoDB is not SQL-compatible, required efforts to learn
- There is not strict data schema, you can change the structure of message fields easily, but also it requires more checks for validity.
