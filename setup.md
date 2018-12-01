Mininet Cheat Sheet
===================


Introduction
============




Setup
=====

## Mininet Wifi

TODO

## Working over SSH

Working on a virtualized user interface is usually annoying for some reasons, like different keymaps and lack of
known workspace tools.


### Setup Port Fowarding

If you're using a NAT network setup (VirtualBox default), you may need to add a port forwarding entry.

VirtualBox -> Settings -> Network -> Advanced -> Port Fowarding

Add rule:

```
Host IP: 127.0.0.1
Host Port: 20022
Guest IP: 10.0.2.15 (*)
Guest IP: 22
```


* ifconfig on virtual machine


**Curiosity**: Another option is to use "Host-only Adapter" setup.


### Mac OS

If you're running a Mac OS, you may need to run some additional step.

Make sure you have Xquartz installed, which is an X11 window server for Mac OS. You can check if Xquartz it's working by running `xterm` on any terminal. You can install Xquartz from the official website at https://www.xquartz.org/ or using Homebrew.

```
brew cask install xquartz
```

You will have to logout for changes to take place.

We also need to set enverionmental variable for the Python interpreter locale. Add to `~/.bash_profile`:

```
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```


### Testing connectivity
```
ssh -Y wifi@localhost -p 20022
```

Start Mininet.

```
wifi@wifi-VirtualBox:~$ sudo -E mn

```

Test `ping`.

```
mininet-wifi> pingall
*** Ping: testing ping reachability
h1 -> h2
h2 -> h1
*** Results: 0% dropped (2/2 received)
```

Test `xterm`

```
mininet-wifi> h1 xterm
```

## Setup File Sharing

Add the current user to the Virtualbox user group to avoid using sudo all the time.

```
sudo usermod -G vboxsf -a $USER
```

Select the data from the host machine you want to share.

VirtualBox -> Settings -> Shared Folders

Add Folder

```
Folder Path: {Path you want to mount, eg: `~/mininet`}
Folder Name: {shared}
Auto-mount: True
```

You must restart the virtual machine for changes to take place.

VirtualBox -> Double Click on Virtual Machine Name -> Reset

Finally, you can add a symbolic link to the shared folder to make it easier to access it from your home.

```
ln -s /media/sf_shared/ ~/shared
```

Troubleshouting
===============

### Can't start mininet

Try cleaning up

```
sudo mn -c
```


References
==========

1. VirtualBox Forum. How to ssh into a guest using NAT?. https://forums.virtualbox.org/viewtopic.php?f=8&t=55766
2. CoderWall. Mac OS X: ValueError: unknown locale: UTF-8 in Python. https://coderwall.com/p/-k_93g/mac-os-x-valueerror-unknown-locale-utf-8-in-python
