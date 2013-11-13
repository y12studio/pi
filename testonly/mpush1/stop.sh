#!/bin/sh
ps ax | grep "sudo python main_motion.py"| grep -v grep | awk '{print $1}' | xargs sudo kill
