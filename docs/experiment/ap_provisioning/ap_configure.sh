# Start hostapd
service hostapd start

# Setting up AP interface
ip addr flush dev wlan3
ip link set up dev wlan3
ip addr add 192.168.10.1 dev wlan3

# Start dnsmasq
service dnsmasq start

# Enable masquerade on the output interface
iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE