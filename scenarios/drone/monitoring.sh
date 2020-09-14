#!/bin/bash

while true; do 

	if kubectl logs $(kubectl get pod -l app=rru -o jsonpath="{.items[0].metadata.name}") | grep -q 'Lost IF4p5 connection'; then
	
	kubectl delete deployments rcc rru
	sleep 60s
	#################################################################
	#  OAI-RAN
	###########################################

	helm install ../../helm-charts/simplechart/ --generate-name --set name=rcc --set nodeAffinity.values=edge &>/dev/null &
	sleep 5s
	helm install ../../helm-charts/simplechart/ --generate-name --set name=rru --set nodeAffinity.values=antenna &>/dev/null &
	sleep 5s

	RRU_POD=$(kubectl get pod -l app=rru -o jsonpath="{.items[0].metadata.name}")
	RCC_POD=$(kubectl get pod -l app=rcc -o jsonpath="{.items[0].metadata.name}")
	FLEXRAN_POD=$(kubectl get pod -l app=flexran-controller -o jsonpath="{.items[0].metadata.name}")
	AMF_IP=$(kubectl get pod -l app=amf -o jsonpath="{.items[0].status.podIP}")
	RCC_IP=$(kubectl get pod -l app=rcc -o jsonpath="{.items[0].status.podIP}")
	RRU_IP=$(kubectl get pod -l app=rru -o jsonpath="{.items[0].status.podIP}")
	FLEXRAN_IP=$(kubectl get pod -l app=flexran-controller -o jsonpath="{.items[0].status.podIP}")

#RRU
	kubectl exec $RRU_POD -- sed -i "s|local_if_name.*;|local_if_name                    = \"eth0\";|g" ./ci-scripts/conf_files/rru.fdd.band7.conf
	kubectl exec $RRU_POD -- sed -i "s|\"127.0.0.1\"|\"$RCC_IP\";|g" ./ci-scripts/conf_files/rru.fdd.band7.conf
	kubectl exec $RRU_POD -- sed -i "s|remote_address.*;|remote_address                   = \"$RCC_IP\";|g" ./ci-scripts/conf_files/rru.fdd.band7.conf
	kubectl exec $RRU_POD -- sed -i "s|local_address.*;|local_address                    = \"$RRU_IP\";|g" ./ci-scripts/conf_files/rru.fdd.band7.conf

#RCC
	kubectl exec $RCC_POD -- sed -i "s|mcc = 208;|mcc = 208;|g" ./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf
	kubectl exec $RCC_POD -- sed -i "s|mnc = 92;|mnc = 93;|g" ./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf
	kubectl exec $RCC_POD -- sed -i "s|ipv4 .*;|ipv4       = \"$AMF_IP\";|g" ./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf
	kubectl exec $RCC_POD -- sed -i "s|ENB_IPV4_ADDRESS_FOR_S1_MME.*;|ENB_IPV4_ADDRESS_FOR_S1_MME              = \"$RCC_IP\/24\";|g" ./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf
	kubectl exec $RCC_POD -- sed -i "s|ENB_IPV4_ADDRESS_FOR_S1U.*;|ENB_IPV4_ADDRESS_FOR_S1U              = \"$RCC_IP\/24\";|g" ./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf
	kubectl exec $RCC_POD -- sed -i "s|ENB_IPV4_ADDRESS_FOR_X2C.*;|ENB_IPV4_ADDRESS_FOR_X2C              = \"$RCC_IP\/24\";|g" ./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf
	kubectl exec $RCC_POD -- sed -i "s|local_if_name.*;|local_if_name  = \"eth0\";|g" ./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf
	kubectl exec $RCC_POD -- sed -i "s|remote_address.*;|remote_address  = \"$RRU_IP\";|g" ./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf
	kubectl exec $RCC_POD -- sed -i "s|local_address.*;|local_address  = \"$RCC_IP\";|g" ./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf

#flexran config
	kubectl exec $RCC_POD -- sed -i "s|FLEXRAN_ENABLED.*;|FLEXRAN_ENABLED        = \"yes\";|g" ./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf
	kubectl exec $RCC_POD -- sed -i "s|FLEXRAN_INTERFACE_NAME.*;|FLEXRAN_INTERFACE_NAME = \"eth0\";|g" ./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf
	kubectl exec $RCC_POD -- sed -i "s|FLEXRAN_IPV4_ADDRESS.*;|FLEXRAN_IPV4_ADDRESS   = \"$FLEXRAN_IP\";|g" ./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf

#run
	#kubectl exec $FLEXRAN_POD -- ./run_flexran_rtc.sh  > /dev/null 2>&1 &
	kubectl exec $RCC_POD -- bash ./ran.sh > /dev/null 2>&1 &
	sleep 5s
	kubectl exec $RRU_POD -- bash ./ran.sh > /dev/null 2>&1 &
     	
#	echo "matched"
	fi

done
