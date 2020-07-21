#!/bin/bash
#Choose scenario
var=$1;

if [ "$var" == "--CRAN-SCENARIO" ]; then

echo "SCENARIO" $var

helm install ../../helm-charts/free5gc/ --generate-name --set name=mongo-lasse &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=hss &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=amf &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=upf &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=smf &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=pcrf &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=webapp &>/dev/null &
sleep 5s
helm install ../../helm-charts/simplechart/ --generate-name --set name=rcc --set nodeAffinity.values=edge &>/dev/null &
sleep 5s
helm install ../../helm-charts/simplechart/ --generate-name --set name=rru --set nodeAffinity.values=antenna &>/dev/null &
sleep 5s
helm install ../../helm-charts/simplechart/ --generate-name --set name=flexran-controller --set nodeAffinity.values=edge &>/dev/null &
sleep 60s

fi

if [ "$var" == "--ALL-IN-ONE-SCENARIO" ]; then

echo "SCENARIO" $var

helm install ../../helm-charts/free5gc/ --generate-name --set name=mongo-lasse --set nodeAffinity.values=antenna &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=hss --set nodeAffinity.values=antenna &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=amf --set nodeAffinity.values=antenna &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=upf --set nodeAffinity.values=antenna &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=smf --set nodeAffinity.values=antenna &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=pcrf --set nodeAffinity.values=antenna &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=webapp --set nodeAffinity.values=antenna &>/dev/null &
sleep 5s
helm install ../../helm-charts/simplechart/ --generate-name --set name=rcc --set nodeAffinity.values=antenna &>/dev/null &
sleep 5s
helm install ../../helm-charts/simplechart/ --generate-name --set name=rru --set nodeAffinity.values=antenna &>/dev/null &
sleep 5s
helm install ../../helm-charts/simplechart/ --generate-name --set name=flexran-controller --set nodeAffinity.values=antenna &>/dev/null &
sleep 60s

fi

if [ "$var" == "--AMF-UPF-EDGE-SCENARIO" ]; then

echo "SCENARIO" $var

helm install ../../helm-charts/free5gc/ --generate-name --set name=mongo-lasse &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=hss &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=amf --set nodeAffinity.values=edge &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=upf --set nodeAffinity.values=edge &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=smf &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=pcrf &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=webapp &>/dev/null &
sleep 5s
helm install ../../helm-charts/simplechart/ --generate-name --set name=rcc --set nodeAffinity.values=edge &>/dev/null &
sleep 5s
helm install ../../helm-charts/simplechart/ --generate-name --set name=rru --set nodeAffinity.values=antenna &>/dev/null &
sleep 5s
helm install ../../helm-charts/simplechart/ --generate-name --set name=flexran-controller --set nodeAffinity.values=edge &>/dev/null &
sleep 60s

fi

if [ "$var" == "--AMF-EDGE-SCENARIO" ]; then

echo "SCENARIO" $var

helm install ../../helm-charts/free5gc/ --generate-name --set name=mongo-lasse &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=hss &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=amf --set nodeAffinity.values=edge &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=upf &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=smf &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=pcrf &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=webapp &>/dev/null &
sleep 5s
helm install ../../helm-charts/simplechart/ --generate-name --set name=rcc --set nodeAffinity.values=edge &>/dev/null &
sleep 5s
helm install ../../helm-charts/simplechart/ --generate-name --set name=rru --set nodeAffinity.values=antenna &>/dev/null &
sleep 5s
helm install ../../helm-charts/simplechart/ --generate-name --set name=flexran-controller --set nodeAffinity.values=edge &>/dev/null &
sleep 60s

fi

if [ "$var" == "--MONOLITH-SCENARIO" ]; then

echo "SCENARIO" $var

helm install ../../helm-charts/free5gc/ --generate-name --set name=mongo-lasse &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=hss &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=amf &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=upf &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=smf &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=pcrf &>/dev/null &
sleep 5s
helm install ../../helm-charts/free5gc --generate-name --set name=webapp &>/dev/null &
sleep 5s
helm install ../../helm-charts/simplechart/ --generate-name --set name=rcc --set nodeAffinity.values=antenna &>/dev/null &
sleep 5s
helm install ../../helm-charts/simplechart/ --generate-name --set name=rru --set nodeAffinity.values=antenna &>/dev/null &
sleep 5s
helm install ../../helm-charts/simplechart/ --generate-name --set name=flexran-controller --set nodeAffinity.values=edge &>/dev/null &
sleep 60s

fi

echo "----------------------------------------------------------"
echo "Scenario mounted in Kubernetes."
echo "----------------------------------------------------------"

#Free5gc init
HSS_POD=$(kubectl get pod -l app=hss -o jsonpath="{.items[0].metadata.name}")
AMF_POD=$(kubectl get pod -l app=amf -o jsonpath="{.items[0].metadata.name}")
UPF_POD=$(kubectl get pod -l app=upf -o jsonpath="{.items[0].metadata.name}")
SMF_POD=$(kubectl get pod -l app=smf -o jsonpath="{.items[0].metadata.name}")
PCRF_POD=$(kubectl get pod -l app=pcrf -o jsonpath="{.items[0].metadata.name}")
MONGO_IP=$(kubectl get pod -l app=mongo-lasse -o jsonpath="{.items[0].status.podIP}")
HSS_IP=$(kubectl get pod -l app=hss -o jsonpath="{.items[0].status.podIP}")
AMF_IP=$(kubectl get pod -l app=amf -o jsonpath="{.items[0].status.podIP}")
UPF_IP=$(kubectl get pod -l app=upf -o jsonpath="{.items[0].status.podIP}")
SMF_IP=$(kubectl get pod -l app=smf -o jsonpath="{.items[0].status.podIP}")
PCRF_IP=$(kubectl get pod -l app=pcrf -o jsonpath="{.items[0].status.podIP}")
WEBAPP_POD=$(kubectl get pod -l app=webapp -o jsonpath="{.items[0].metadata.name}")
MONGO_POD=$(kubectl get pod -l app=mongo-lasse -o jsonpath="{.items[0].metadata.name}")

#Create uptun interface in UPF pod
kubectl exec $UPF_POD -- bash /root/setup.sh &>/dev/null &
#Init mongo and webapp
kubectl exec $MONGO_POD -- bash /usr/src/data/setup-lasse.sh $MONGO_IP &>/dev/null &
sleep 5s
kubectl exec $WEBAPP_POD -- bash /root/setup.sh $MONGO_IP &>/dev/null &

#run
kubectl exec $HSS_POD -- ./setup-lasse.sh $MONGO_IP $HSS_IP $AMF_IP $UPF_IP $SMF_IP $PCRF_IP &>/dev/null &
echo "HSS initialized"
sleep 10s
kubectl exec $AMF_POD -- ./setup-lasse.sh $MONGO_IP $HSS_IP $AMF_IP $UPF_IP $SMF_IP $PCRF_IP &>/dev/null &
echo "AMF initialized"
sleep 10s
kubectl exec $UPF_POD -- ./setup-lasse.sh $MONGO_IP $HSS_IP $AMF_IP $UPF_IP $SMF_IP $PCRF_IP &>/dev/null &
echo "UPF initialized"
sleep 10s
kubectl exec $SMF_POD -- ./setup-lasse.sh $MONGO_IP $HSS_IP $AMF_IP $UPF_IP $SMF_IP $PCRF_IP &>/dev/null &
echo "SMF initialized"
sleep 10s
kubectl exec $PCRF_POD -- ./setup-lasse.sh $MONGO_IP $HSS_IP $AMF_IP $UPF_IP $SMF_IP $PCRF_IP &>/dev/null &
echo "PCRF initialized"
sleep 10s

#Warning
WEBAPP_EXTERNAL_PORT=$(kubectl get service webapp --output jsonpath='{.spec.ports[].nodePort}')

echo "----------------------------------------------------------"
echo "The Core has been initialized, you can configure the users in http://< cloud node >:$WEBAPP_EXTERNAL_PORT"
echo "----------------------------------------------------------"

#################################################################
#  OAI-RAN
###########################################

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
kubectl exec $FLEXRAN_POD -- ./run_flexran_rtc.sh  > /dev/null 2>&1 &
kubectl exec $RCC_POD -- bash ./ran.sh > /dev/null 2>&1 &
sleep 5s
kubectl exec $RRU_POD -- bash ./ran.sh > /dev/null 2>&1 &

echo "----------------------------------------------------------"
echo "RAN initialized"
echo "----------------------------------------------------------"
