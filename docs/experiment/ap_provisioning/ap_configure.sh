# Start hostapd
service hostapd start

## Add local A record for CnC server
echo "192.168.20.1 default\n" >> /etc/hosts

# Setting up AP interface
ip addr flush dev wlan3
ip link set up dev wlan3
ip addr add 192.168.10.1 dev wlan3

# Start dnsmasq
service dnsmasq start

# Enable masquerade on the output interface
iptables -t nat -A POSTROUTING -o wlan_conf.j2 -j MASQUERADE