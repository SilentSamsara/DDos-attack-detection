#!/bin/bash
filename='view_history_'`date +%F-%H:%M:%S.pcap`
touch $filename
#没有后面的tdid则无法退出tcpdump进程
tcpdump -i s11-eth1 -s 0 -w $filename & tdid='pgrep tcpdump'

sleep 2s
file_size=`du $filename|awk '{print $1}'`
tshark -r $filename -T fields -e frame.number -e frame.time_epoch -e frame.protocols -e ip.src -e ip.dst -e tcp.port -e udp.port -E separator=, > attack.csv
echo 'file_size'$file_size


