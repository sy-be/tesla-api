# tesla-api
Tesla remoteops
=======================

Library and a script to control your Tesla from cli. Works best for scheduled operations, such as
scheduling sentry mode to turn on and off or starting and stopping charging.

example systemd service and timers are included in `contrib/` folder.
copy them to `/etc/systemd/system/`
copy example `contrib/systemd/credentials` file somewhere safe, e.g. `~/bin/private` and update it.

update systemd service files to point to credentials location and also update it with vehicle id
to get vehicle id (correct paths if necessary):
```
$ set -o allexport
$ source private/credentials 
$ set +o allexport
$ ./tesla-api/run.py -l
```
above will generate a bearer key and also will return vehicle ids to include in systemd files.
tesla client id and secret are here: https://pastebin.com/pS7Z6yyP

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
