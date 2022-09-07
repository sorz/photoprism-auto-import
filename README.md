# PhotoPrism Auto Import

This repositry contains a Python scirpt to call
[PhotoPrism](https://photoprism.app/) to import photos on given folder, and
related Systemd configuartion to monitor the folder and run the script whenever
new files are added into the folder.

## How to setup

1. Copy `syncphoto.py` to `/opt/syncphoto/`;
2. Get Session ID from your browser, write it to `/opt/syncphoto/session_id`;
3. Copy `syncphoto.path` and `syncphoto.service` to `/etc/systemd/system/`;
4. Edit the two systemd files to match your PhotoPrism setup;
5. Enable `syncphoto.path`: `sudo systemctl enable --now syncphoto.path`


