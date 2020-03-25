# tesla-api
Tesla remoteops
=======================

Library and a script to control your Tesla from cli. Works best for scheduled operations, such as
scheduling sentry mode to turn on and off.

example systemd service and timers are included in `contrib/` folder.
copy them to `/etc/systemd/system/`
make sure to set necessary credentials and paths in systemd service files for the commands to actually work.
tesla client id and secret are here: https://pastebin.com/pS7Z6yyP
It is suggested to manually run the script in order to get correct vehicle id to include in systemd service file.

to enable systemd service:
```
systemctl enable tesla-sentry-on.service
systemctl enable tesla-sentry-off.service
```

to manually run setting sentry mode on or off:
```
systemctl start tesla-sentry-on.service
systemctl start tesla-sentry-off.service
```

to enable timers:
```
systemctl enable tesla-sentry-on.timer 
systemctl enable tesla-sentry-off.timer
systemctl start tesla-sentry-on.timer
systemctl start tesla-sentry-off.timer
```
