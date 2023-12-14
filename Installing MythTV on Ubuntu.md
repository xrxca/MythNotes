# Installing MythTV on Ubuntu

I suppose I could have gone with a different OS, but I've been using Ubuntu at work and on home systems for almost 20 years, and used Mythbuntu for my second iteration of MythTV (First was all self compiled, and I actually used a couple original XBoxes as frontends), the last time I updated Mythbuntu was 11.04 which allowed me to use Hauppauge HD-PVRs for recording instead of Tuner Cards.  I'm still using HD-PVRs, but with newer source boxes.

Installing MythTV on a current Ubuntu release is surprisingly easy, the MythTV Wiki has a [page](https://www.mythtv.org/wiki/Installing_MythTV_on_Ubuntu) describing the install.

The quick summary is add the ppa, install the package(s)

For my frontends, the steps were:
```console
sudo add-apt-repository ppa:mythbuntu/33
sudo apt install mythtv-frontend 
```

