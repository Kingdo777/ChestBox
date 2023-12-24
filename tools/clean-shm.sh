#!/bin/bash

#ipcs -m | grep '0x7777' | awk '{print $2}' | xargs -n 1 sudo ipcrm -m
docker exec -it wsk0_kingdo_guest_StateFunction1 sh -c "ipcs -m | grep '0x7777' | awk '{print \$2}' | xargs -n 1 ipcrm -m"