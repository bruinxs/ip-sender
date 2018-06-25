#!/bin/bash

set -e

cp -f ./ipsender.conf /etc
cp -f ./ipsender.py /usr/local/bin
chmod +x /usr/local/bin/ipsender.py
cp -f ./ipsenderd.service /etc/systemd/system

systemctl daemon-reload
systemctl start ipsenderd.service