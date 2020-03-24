# tesla-api
Tesla remoteops
=======================

Library and a script to control your Tesla from cli. Works best for scheduled operations, such as
scheduling sentry mode to turn on and off.

example systemd service and timers are included in `contrib/` folder.
copy them to `~/.config/systemd/user` (create directories if necessary)
make sure to set necessary credentials in systemd service for the commands to actually work.
It is suggested to manually run the script in order to get correct vehicle id to include in systemd service file.

to enable systemd service:
```
systemctl --user enable tesla-sentry-on.service
systemctl --user enable tesla-sentry-off.service
```

to manually run setting sentry mode on or off:
```
systemctl --user start tesla-sentry-on.service
systemctl --user start tesla-sentry-off.service
```

to enable timers:
```
systemctl --user enable tesla-sentry-on.timer 
systemctl --user enable tesla-sentry-off.timer 
```