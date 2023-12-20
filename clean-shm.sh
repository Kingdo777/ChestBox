ipcs -m | grep '0x7777' | awk '{print $2}' | xargs -n 1 sudo ipcrm -m
