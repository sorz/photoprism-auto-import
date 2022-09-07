# PhotoPrism Auto Import

This repositry contains a Python scirpt to call
[PhotoPrism](https://photoprism.app/) to import photos on given folder, and
related Systemd configuartion to monitor the folder and run the script whenever
new files are added into that folder.

## Dependencies

Ubuntu/Debian:

```bash
sudo apt install python3-requests python3-websocket
```

Arch Linux:

```bash
sudo pacman -S python-requests python-websocket-client
```

## How to setup

1. Copy `syncphoto.py` to `/opt/syncphoto/`;
2. Get Session ID from your browser, write it to `/opt/syncphoto/session_id`;
3. Copy `syncphoto.path` and `syncphoto.service` to `/etc/systemd/system/`;
4. Edit the two systemd files to match your PhotoPrism setup;
5. Enable `syncphoto.path`: `sudo systemctl enable --now syncphoto.path`

## Benfits

- Compatible with any file syncing software (e.g. Syncthing), do not depend on
  their hook.

- Compatible with any PhotoPrism install (docker or not), via HTTP API.

- No extra daemon, no timer/crontab, no polling. Take Systemd's functionality
  for free!

## Known issues

- Multiple import directories are not supported (can be added if someone
  need that).

- Imported files will be moved by PhotoPrism, so that systemd.path
  `PathExists=` do not trigger it again. Keeping files may be possible by using
  `PathModified=` (and change the script), but I have not yet try it.

- Import will start immediately despite more files are still coming. It will
  re-run the script until no file left. The running interval is limited by
  `StartLimitIntervalSec=` on systemd.path.

- Will half-written file get imported thus producing broken files?

- If any error occurs during import and left files, it will retry repeatedly.
  The retry interval is limited by `StartLimitIntervalSec=` on systemd.path.

