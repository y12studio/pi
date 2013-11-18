#!/bin/sh
ps ax | grep "sudo python mpush.py"| grep -v grep | awk '{print $1}' | xargs sudo kill
