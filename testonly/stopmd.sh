#!/bin/sh
ps ax | grep "sudo python motion_pushover.py"| grep -v grep | awk '{print $1}' | xargs sudo kill
