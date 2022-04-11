#!/bin/sh

action='-A'
ip1='192.168.0.1'
while getopts 'ad' flag 
do
	case "${flag}" in
		a) 
			action='-A'
			echo 'add all'
			;;
		d) 
			action='-D'
			echo 'delete all'
			;;
	esac
done

#echo $action
iptables $action INPUT -p tcp -s $ip1 --dport 22 -j ACCEPT
iptables $action INPUT -p tcp -s 0.0.0.0/0 --dport 22 -j DROP
#end
