service hostapd stop
service hostapd start

ip addr flush dev {{WLAN_INTERFACE}}
ip addr add {{WLAN_ADDR}} dev {{WLAN_INTERFACE}}


service dnsmasq restart
