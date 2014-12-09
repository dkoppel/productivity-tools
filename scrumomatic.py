#!/usr/bin/env python
# scrumomatic

import rtm
import sys


key = ""
secret = ""
token = ""
l_id = ""

rtm_sess = rtm.createRTM(key, secret, token)
t = rtm_sess.tasks.getList(list_id=l_id).tasks.list.taskseries
for x in t:
    if(x.task.completed == ""):
        if (x.url == ""):
            sys.stdout.write(x.name + ", ")
        else:
            sys.stdout.write("[" + x.url + " " + x.name + "], ")
