# Optimization

To check the validity, we place the APs in a Sub-Optimal case position. 
We take the most recent positions of UEs as input data used for `optimization` tasks.

Figure shows on the map real and suggested optimal coordinates for AP. These new 
positions can drop out connected clients due to large distance because at this space connection became
unstable, their error rate is higher.

Distance between real and suggested positions for AP1 is 32m and 20m for AP2 accordingly. We
find out two possible reasons for this difference:

1. Fragmentation of used Android phones - in the experiment we used various gadgets running
dierent Operating System (OS) version. They present several generations of Android evolution. 
The older generations can have less accurate GNSS module, therefore provide a wrong
position estimate.

2. Location provider optimization in GPS Android - GPS Android was designed to choose be-
tween network-assisted and GPS-assisted location estimation. The exact option depends on
what provider has better connection status. First, it tries to set up GPS provider, if it fails,
the phone fallback to network-provided location estimation which is less accurate.