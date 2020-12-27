# lego-spike-linux

add user to group dialout or become root

```
usermod -a -G dialout ${USER}
```

connect via usb
```
journalctl -xe -f
```

looks like
```
Dec 27 12:49:53 dudu kernel: usb 1-3: new full-speed USB device number 8 using xhci_hcd
Dec 27 12:49:54 dudu kernel: usb 1-3: New USB device found, idVendor=0694, idProduct=0010, bcdDevice= 2.00
Dec 27 12:49:54 dudu kernel: usb 1-3: New USB device strings: Mfr=1, Product=2, SerialNumber=3
Dec 27 12:49:54 dudu kernel: usb 1-3: Product: LEGO Technic Large Hub in FS Mode
Dec 27 12:49:54 dudu kernel: usb 1-3: Manufacturer: LEGO System A/S
Dec 27 12:49:54 dudu kernel: usb 1-3: SerialNumber: 123456789ABCDE
Dec 27 12:49:54 dudu mtp-probe[8062]: checking bus 1, device 8: "/sys/devices/pci0000:00/0000:00:14.0/usb1/1-3"
Dec 27 12:49:54 dudu mtp-probe[8062]: bus: 1, device: 8 was not an MTP device
Dec 27 12:49:54 dudu kernel: cdc_acm 1-3:1.0: ttyACM0: USB ACM device
Dec 27 12:49:54 dudu kernel: usbcore: registered new interface driver cdc_acm
Dec 27 12:49:54 dudu kernel: cdc_acm: USB Abstract Control Model driver for USB modems and ISDN adapters
Dec 27 12:49:54 dudu mtp-probe[8067]: checking bus 1, device 8: "/sys/devices/pci0000:00/0000:00:14.0/usb1/1-3"
Dec 27 12:49:54 dudu mtp-probe[8067]: bus: 1, device: 8 was not an MTP device
Dec 27 12:49:56 dudu ModemManager[1124]: <info>  [base-manager] couldn't check support for device '/sys/devices/pci0000:00/0000:00:14.0/usb1/1-3': not supported by any plugin
```

find device
```
[conni@dudu conni]# ls -la /dev/ttyACM*
crw-rw----. 1 root dialout 166, 0 Dec 27 13:16 /dev/ttyACM0
```

open terminal
```
screen /dev/ttyACM0 115200
```

press control-c when receiving sensor data stream

```
import hub

hub.display.show('hello world') 
```

exploring the api:
```
[k for k in dir(hub)]
```

references
[micropython on instructables](https://www.instructables.com/MicroPython-on-SPIKE-Prime/)
