# 1. Formal Description of experiment

Main information on the experiment

| Key                | Value                         |
| ------------------ | ----------------------------- |
| Date of experiment | 11.02-12.02                   |
| Experiment team    | 3 RCSE students, 1 supervisor |

Целью эксперимена является

1. Проверка работоспособности комплекса программ: **GPS_Tracker**, **GPS_Frontend**, **GPS_Android**.
   - Соответствие функциональных требованиям, предъявляемой к системе.
   - Производительность работы системы.
   - Стабильность работы системы в случае промышленной эксплуатации.
2. Проверка работы алгоирмов оптимизации производительности мабильных сетей с помощью передвижных базовых станций.
   - Оценка корректности предстазания оптимальных позиций для размещения
   - Оценка скорости алгоритмов оптимизации

## Main information

The main purpose of the experiment is to optimize the location of AP's such way that throughput and RSSI of UE's connected to those AP is maximized.

For that we conduct the experiment in the following way:

1. APs' are located in the space without any obstacles. They are surronded by UEs.
2. UEs connected to APs and evaluate RSSI and throughput via GPS_Android software.
3. Stored measured records by UEs are sent/copied to GPS_Tracker.
4. An operator use interface provided by GPS_Frontend to analyse the measurements and run optimization algorithms to find out the best positions for APs.
5. After the next optimal positions for APs are found, the APs are moved to the optimized points.
6. An experiment is going to step 3 and repeated until no significan improvement for APs positions will be observed.

The experiment is repeated three times with different initial APs and UEs positions.

Test sets:

1. Suboptimal (APs in between clusters)
2. Near-optimal (APs in clusters according to K-Means.)
3. Uniform (in area)

For each of test case we expect that:

1. Minimization of the distance between UEs and APs will lead to RSS gain and throughput increase.
2. The interference effect may be visible – in the suboptimal placements, it should decrease the throughput - ???;

## Glossary

| Termin | Description                                                                                                                             |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| UE     | User Equipment - a mobile terminal which transmit data via radio link. Each UEs runs different Android OS version (4.0+)                |
| AP     | Access Point - an WiFi hotspot running by a laptop with wifi stick. Each laptop has side application to support throughput measurement. |
| RSS    | Received Signal Strength - estimated value of signal power for radio signal. The greater RSSI value, the stronger the signal.           |
