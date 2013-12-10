#!/bin/sh
ps ax | grep "sudo python halfsync.py"| grep -v grep | awk '{print $1}' | xargs sudo kill
