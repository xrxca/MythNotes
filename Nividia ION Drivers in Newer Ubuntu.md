# Using Nvidia ION in Newer Ubuntu Versions
I have some older Zotac boxes that have the NVidia ION video chipset, which is not supported in newer Ubuntu releases.  Since I'm upgrading my boxes from 11.04 (Natty) to 22.04 (Jammy) in order to intall the latest stable MythTV release (33.1 as of this document) I researched and found a PPA that supports this older chipset.

The ppa is kelebek333/nvidia-legacy [Site](https://launchpad.net/~kelebek333/+archive/ubuntu/nvidia-legacy)

I've used this on XUbuntu, LUbuntu, and Vanilla Ubuntu with no issues, and it allows me to use the VDPAU playback settings in MythTV.

### Installation
From a shell prompt:
```console
sudo add-apt-repository ppa:kelebek333/nvidia-legacy
sudo apt install nvidia-340-updates nvidia-340-updates-dev xorg-modulepath-fix
```
Reboot the system.
(That should be it.)
