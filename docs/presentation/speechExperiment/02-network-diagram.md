# Network diagram

Here we see network configuration. The APs subnet has identical settings, they have 
an internal `Dynamic Host Configuration Protocol (DCHP)` server to provide dynamic addresses 
for connected UEs. To prevent address collisions and to simplify routing, the APs perform `masquerading` 
(Source & Destination Network Address Translation (NAT) (SNAT/DNAT)) on the output interface (connection to Command Center).
Consequently, Command Center cannot access the UEs directly, 
but UEs will always reach Command Center because DCHP server sets the default gateway IP address.

Command Center has `another DCHP` server to set APs dynamic addresses. When APs connect
to wireless point "cnc" they receive a dynamic IP address by Command Center. Because network
for Command Center is different from the internal networks of Wi-Fi adapters in the APs, there is
no network collision.
Finally, each connected UE can access static Command Center address 192.168.20.1 and local
gateway 192.168.10.1.