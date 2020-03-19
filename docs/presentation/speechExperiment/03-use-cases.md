# Use cases

The experiment repeated three times with different `initial positions`. Test sets:
1. Near-Optimal
2. Uniform
3. Sub-Optimal

For each test case, we `expect` that:
1. Minimization of the distance between UEs and APs will lead to Received Signal Strengths
(RSSs) gain and throughput increase.
2. The interference effect may be visible - in the sub-optimal placements, it should decrease the
throughput;

## Sub-optimal

The first Sub-Optimal layout is shown. Each `AP` is in the middle of each group, therefore they have
the same distance to cluster centers.
This case should have the highest signal quality and transmission rate.

## Uniform

In the uniform case layout we want to put APs at the same distance and line from Command Center.
Here, both `APs` are set right on the line between the 1st and 3rd quarters and between the 2nd
and 4th quarters.
Signal quality and transmission rate in this configuration `expected to decrease` compared with
the Near-Optimal case.

## Near-optimal

The last is Near-optimal case. Here `Access Points` are placed in the ground so that both of them
are in the center of the corresponding quarter (2nd and 3rd) 25x25 meters and far from all UEs to
approximately 25m.
UEs located in `two groups` of three elements that fill the other two quarters (1st and 4th)
respectively.
At the same time, they keep a distance from each other to limit interference and hold the same
conditions.
Finally, `Command Center` is set in the middle of whole 50x50 meters an experimental eld, so
that 2 AP and 2 groups of UEs mentioned above are on the same distance.