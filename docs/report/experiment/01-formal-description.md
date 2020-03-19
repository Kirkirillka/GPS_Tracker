# 1. Formal Description of the experiment

| Key                | Value                         |
| ------------------ | ----------------------------- |
| Date of experiment | 11.02-12.02                   |
| Experiment team    | 3 RCSE students, 1 supervisor |

The aims of the experiment are:

1. Check the functionality of experimental software system: **GPS_Tracker**, **GPS_Frontend**, **GPS_Android**.

- Check the functional properties of the system.
- System stability, performance and usability measurements in real case scenarios.

2. Evaluation of layout optimization algorithms, which were intended to use on UAVs, but for the experiment we use ground APs.

- Evaluation of correctness of provided optimized positions by the algorithms.
- Measurement of stability, performance, and usability of the algorithms.

## Main information

The main purpose of the experiment is to optimize the location of AP's such a way that throughput and RSS of UE's connected to those AP is maximized.

For that we experiment in the following way:

1. APs are located in free space without any obstacles. They are surrounded by UEs.
2. UEs are connected to APs and evaluate RSS and throughput via our GPS_Android app.
3. Stored measured records by UEs are sent/copied to the central server.
4. An operator uses the provided interface to analyze the measurements and run optimization algorithms to find out the best positions for APs.
5. After the next optimal positions for APs are found, access points moved to the optimized points.
6. An experiment is going to step 3 and repeated until no significant improvement for APs positions will be observed.

The experiment repeated three times with different initial APs and UE positions.

Test sets:

1. Suboptimal (APs are inside of clusters)
![Main perspective of the experiment](<images/05-cases-description-Sub-optimal-clusters.png>){width=75%}
2. Near-optimal (APs in clusters according to K-Means.)
3. Uniform (in the area)

For each test case, we expect that:

1. Minimization of the distance between UEs and APs will lead to RSS and throughput increase.
2. The interference effect may be visible – in the suboptimal placements, it should decrease the throughput;

## Glossary

| Terminology | Description                                                                                                                               |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| UE     | User Equipment - a mobile terminal which transmits data via the radio link. Each UEs runs different Android OS version (4.0+)             |
| AP     | Access Point - a Wi-Fi access point running by a laptop with an external Wi-Fi adapter. Each laptop has a side application to support throughput measurement.  |
|CnC    | A central server where the system core is running. All measurement analysis and UI interactions perform here. |
|UAV    | Unmanned Aerial Vehicle - a vehicle having AP on the board.|
| RSS    | Received Signal Strength - the estimated value of signal power for the radio signal. The greater the RSS value, the stronger the signal. |
