# Configure AP on Linux using HostAPd and dnsmasq

## Prerequisites

- ansible
- Vagrant
- VirtualBox

## Main information

There is ansible playbook which set up AP on your Linux router.

Tested on:

- Debian 10 (Vagrant)

Steps:

1. Install necessary packages.
2. Add OS'specific settings to allow traffic forwarding.
3. Configure additional wifi interface.
4. Configure `hostapd` and `dnsmasq` and add them to start up.
   5.Set up iptables setting to add NAT on the output interface. So, even Internet will work!

## Usage

It is supposed that WiFi adapter is not occuped by other network programs (e.g. NetworkManager).

If so, them use `airmon-ng check kill` command from package `aircrack-ng`.

### Testing

For local testing you may use ether physical or virtual machine running Debian 10.

For physical machine you need just to plug in the Wifi stick. For the virtual machine you need to add WiFi USB stick in your VM settings.

For proper setup in virtual environment (on VirtualBox) make sure:

1. You are running the latest version of VirtualBox with the latest version of VirtualBox ExtensionPack.
2. You installed `open-vm-box` or `vmbox-guest`.
3. Your user is in **vboxusers** group to allow to see devices on your host machine.

If you have done everything correctly, then you can just set it up by:

1. `cd ansible`
2. `vagrant up --no-provision`
3. Plug in your USB stick
4. `vagrant provision`

### Production

Let our machine has IP address **127.0.0.1** on port **2222** and user **root**, pubkey-based authentification.

The `inventory.yml` file contains:

```conf
127.0.0.1 ansible_port=2222
```

> Warning!
> Currently uses Debian 11 Testing, there is no Vagrant VM for that purpose, so make sure your install the image by yourself!

Check which IP addresses the virtual machine uses. Then perform AP provisioning:

```bash
ansible-playbook ap_run.yml  -i inventory.yml --ask-become-pass
```
