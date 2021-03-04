#!/bin/sh
sleep 5 
kill -15 $(ps aux | pgrep "gunicorn" | awk '{print $2,$NF}')