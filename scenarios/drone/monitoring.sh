#!/bin/bash

while true; do 
	if kubectl logs $(kubectl get pod -l app=rru -o jsonpath="{.items[0].metadata.name}") --tail 20 | grep 'Lost IF4p5 connection' ; then
    	   kubectl exec $(kubectl get pod -l app=rru -o jsonpath="{.items[0].metadata.name}") -- killall lte-softmodem.Rel14
	   kubectl exec $(kubectl get pod -l app=rcc -o jsonpath="{.items[0].metadata.name}") -- killall lte-softmodem.Rel14
	   kubectl exec $(kubectl get pod -l app=rru -o jsonpath="{.items[0].metadata.name}") -- bash ./ran.sh > /dev/null 2>&1 &
	   sleep 5s
           kubectl exec $(kubectl get pod -l app=rcc -o jsonpath="{.items[0].metadata.name}") -- bash ./ran.sh > /dev/null 2>&1 &
	fi
done
