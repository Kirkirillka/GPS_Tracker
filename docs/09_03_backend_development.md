## Decision on GPS_Tracker techniques development

### Description

The GPS_Tracker is implemented in Python language. This is a dynamic interpreting language. That is known the performance is not so perfect compared to static compiled languages, but it has higher changeability property.

Another problem is its dynamic nature, programmers should add more codes to check that the variables they are working on have the right type, right values and so one.

Also, Python doesn't have a proper parallel threading mechanism due to GIL.

To summarize, there is a set of problems:

- Possible performance degradation.
- Ambiguous interfaces, more safe checks.
- Parallel execution, scalability is not so high.

### Decision

In order to mitigate the consequences of using Python as the main language for GPS_Tracker we decided:

- Use additional code documentation and code annotation to clarify the meaning of Python code, helps IDE to derive expected behavior and check code validity.
- Use Worker architecture pattern (`Celery` library). That will help to add scalability to task execution and simplify parallel code programming.
- Use JetBrain Pycharm IDE as the main IDE for programmers to use

### Status

Accepted

### Consequences

- Worker pattern implemented in `Celery` requires additional component to store information about registered tasks and perform synchronization between workers. RabbitMQ is a message queue used to store that information.
