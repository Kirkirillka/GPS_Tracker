### Took place on 12.02.2020

Aim was to involve as many UEs as possible. This is partly a reason of experiment day selection.
Eventually, **6 UEs** took part ranging by Android version from 4 to 9.

Besides installation of apps and binding Wi-Fi to necessary access point, 
a detailed **journal of the Wi-Fi** connection information was enabled.
This allowed monitoring RSSI value on each UEs.

## Weather conditions:
- no precipitation
- cloudy sky
- thin layer of snow on the ground

## Procedure

All items of the experiment were placed on the carton boxes on the ground, so that
they are bit raised from the ground.
![CnC](images/experiment_1_cnc.jpg) 

### Case 1
**Suboptimal scheme** was chosen to begin with:
UEs connection to one AP was made successfully.

But the second AP was connected to the other 3 UEs with more effort.
The reason of it was in the Wi-Fi module issues of AP.
  
After some time of data collection it was clear that the second AP was not sending data to CnC at all, 
so we decided to locate devices according to the near-optimal scheme.

### Case 2
This helped to increase the RSSI signal level a bit from -82 and -84 to -76 and -80, 
data still was collected only from the first AP.
  
In addition, the graphical view in CnC showed 4 UEs close to each other (having approximately the same GPS coordinates), 
whereas the other 2 were detected much further.
  
Then we figured out that the second AP stopped working at some time. But restarting of it and reconnection of UEs did not help to obtain data of that 3 UEs in CnC.

### Case 3
It made no sense to try without data collection on CnC.

## Outcome
As a result, it was decided to:
- fix the second AP failure reasons
- figure out the source of 2 point-outliers in the plot