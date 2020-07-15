#!/bin/bash

kubectl delete deployments mongo-lasse webapp hss amf upf smf pcrf 
kubectl delete service webapp
echo "Free5gc finished"
kubectl delete deployments rcc rru flexran-controller
kubectl delete service flexran-controller
echo "RAN finished"
