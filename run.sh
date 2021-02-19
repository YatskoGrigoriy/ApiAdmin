#!/bin/bash
PATH=/home/grin/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
cd /www/goldennet/Admin  && gunicorn -w 4 app:app -b :5000 

#--log-level debug

#--timeout 600  --access-logfile /var/log/blogflask/access.log
