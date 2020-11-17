import yaml
import time
import subprocess as sp
from subprocess import Popen, PIPE, STDOUT

try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


with open("ran.yaml", "r") as ymlfile:
    ran_yaml = yaml.safe_load(ymlfile)

# Declare variables to be passed into your helm-chart.

namespace = ran_yaml["id"]
option = ran_yaml["option"]
mode = ran_yaml["mode"]

allocation_rcc = ran_yaml["allocation"]["rcc"]
allocation_rru = ran_yaml["allocation"]["rru"]
allocation_vnf = ran_yaml["allocation"]["vnf"]
allocation_pnf = ran_yaml["allocation"]["pnf"]
allocation_enb = ran_yaml["allocation"]["enb"]

coreIP = ran_yaml["CORE"]
FLEXRAN_enable = ran_yaml["FLEXRAN"]["FLEXRAN_enable"]
FLEXRAN_IP = ran_yaml["FLEXRAN"]["FLEXRAN_IP"]
band = ran_yaml["other-params"]["band"]
downlink = ran_yaml["other-params"]["downlink"]
uplink = ran_yaml["other-params"]["uplink"]

#Create NameSpace

#Check if already exists
CheckNamespace = sp.getoutput(["kubectl get ns |  grep -c "+namespace])
print(CheckNamespace)

if CheckNamespace != "0":
  print('ID scenario already exists! Please, change the ID and try again')
  quit()
#Creating
sp.call(["kubectl", "create", "namespace", namespace], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

#Creating deployments using Helm Charts
if option == "rcc-rru":
    sp.call(["helm", "install", "./helm-charts/simplechart/", "--generate-name","--set","name=rcc","--set","namespace="+namespace,"--set","mode="+mode,"--set", "node="+allocation_rcc], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    time.sleep(30)
    sp.call(["helm", "install", "./helm-charts/simplechart/", "--generate-name","--set","name=rru","--set","namespace="+namespace,"--set","mode="+mode,"--set", "node="+allocation_rru], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    time.sleep(30)
    
    print("RAN mounted in Kubernetes namespace:"+namespace)
    RCC_POD = sp.getoutput('kubectl get pod -l app=rcc -o jsonpath="{.items[0].metadata.name}" -n'+namespace)
    RRU_POD = sp.getoutput('kubectl get pod -l app=rru -o jsonpath="{.items[0].metadata.name}" -n'+namespace)
    RCC_IP = sp.getoutput('kubectl get pod -l app=rcc -o jsonpath="{.items[0].status.podIP}" -n'+namespace)
    RRU_IP = sp.getoutput('kubectl get pod -l app=rru -o jsonpath="{.items[0].status.podIP}" -n'+namespace)

    sp.call(["kubectl","-n",namespace,"exec",RRU_POD,"--", "sed", "-i", "s|local_if_name.*;|local_if_name = \"eth0\";|g", "./ci-scripts/conf_files/rru.fdd.band7.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",RRU_POD,"--", "sed", "-i", "s|\"127.0.0.1\"|"+RCC_IP+";|g", "./ci-scripts/conf_files/rru.fdd.band7.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",RRU_POD,"--", "sed", "-i", "s|remote_address.*;|remote_address=\""+RCC_IP+"\";|g", "./ci-scripts/conf_files/rru.fdd.band7.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",RRU_POD,"--", "sed", "-i", "s|local_address.*;|local_address=\""+RRU_IP+"\";|g", "./ci-scripts/conf_files/rru.fdd.band7.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",RRU_POD,"--", "sed", "-i", "s|bands.*;|bands                            = ["+band+"];|g", "./ci-scripts/conf_files/rru.fdd.band7.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

    sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|mcc = 208;|mcc = 208;|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|mnc = 92;|mnc = 93;|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|ipv4 .*;|ipv4       = \""+coreIP+"\";|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|ENB_IPV4_ADDRESS_FOR_S1_MME.*;|ENB_IPV4_ADDRESS_FOR_S1_MME              =\""+RCC_IP+"\/24\";|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|ENB_IPV4_ADDRESS_FOR_S1U.*;|ENB_IPV4_ADDRESS_FOR_S1U              = \""+RCC_IP+"\/24\";|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|ENB_IPV4_ADDRESS_FOR_X2C.*;|ENB_IPV4_ADDRESS_FOR_X2C              = \""+RCC_IP+"\/24\";|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|local_if_name.*;|local_if_name  = \"eth0\";|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|remote_address.*;|remote_address  = \""+RRU_IP+"\";|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|local_address.*;|local_address  = \""+RCC_IP+"\";|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|eutra_band.*;|eutra_band              			      = "+band+";|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|downlink_frequency.*;|downlink_frequency      			      ="+downlink+";|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|uplink_frequency_offset.*;|uplink_frequency_offset 			      = "+uplink+";|g" , "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    
    if FLEXRAN_enable:
        sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i","s|FLEXRAN_ENABLED.*;|FLEXRAN_ENABLED        = \"yes\";|g" , "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i","s|FLEXRAN_INTERFACE_NAME.*;|FLEXRAN_INTERFACE_NAME = \"eth0\";|g" , "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i","s|FLEXRAN_IPV4_ADDRESS.*;|FLEXRAN_IPV4_ADDRESS   = \""+FLEXRAN_IP+"\";|g" , "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

    sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "./ran.sh"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",RRU_POD,"--", "./ran.sh"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

if option == "vnf-pnf":
    sp.call(["helm", "install", "./helm-charts/simplechart/", "--generate-name","--set","name=vnf","--set","namespace="+namespace,"--set","mode="+mode,"--set", "node="+allocation_vnf], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["helm", "install", "./helm-charts/simplechart/", "--generate-name","--set","name=pnf","--set","namespace="+namespace,"--set","mode="+mode,"--set", "node="+allocation_pnf], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    time.sleep(30)

    VNF_POD = sp.getoutput('kubectl get pod -l app=vnf -o jsonpath="{.items[0].metadata.name}" -n'+namespace)
    PNF_POD = sp.getoutput('kubectl get pod -l app=pnf -o jsonpath="{.items[0].metadata.name}" -n'+namespace)
    VNF_IP = sp.getoutput('kubectl get pod -l app=vnf -o jsonpath="{.items[0].status.podIP}" -n'+namespace)
    PNF_IP = sp.getoutput('kubectl get pod -l app=pnf -o jsonpath="{.items[0].status.podIP}" -n'+namespace)

    sp.call(["kubectl","-n",namespace,"exec",PNF_POD,"--", "sed", "-i", "s|local_n_if_name.*;|local_n_if_name = \"eth0\";|g", "./ci-scripts/conf_files/ue.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",PNF_POD,"--", "sed", "-i", "s|remote_n_address.*;|remote_n_address=\""+VNF_IP+"\";|g", "./ci-scripts/conf_files/ue.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",PNF_POD,"--", "sed", "-i", "s|local_n_address.*;|local_n_address=\""+PNF_IP+"\";|g", "./ci-scripts/conf_files/ue.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",PNF_POD,"--", "sed", "-i", "s|bands.*;|bands                            = ["+band+"];|g", "./ci-scripts/conf_files/ue.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

    sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|mcc = 208;|mcc = 208;|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|mnc = 92;|mnc = 93;|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|ipv4 .*;|ipv4       = \""+coreIP+"\";|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|ens3|eth0|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|ENB_IPV4_ADDRESS_FOR_S1_MME.*;|ENB_IPV4_ADDRESS_FOR_S1_MME              =\""+VNF_IP+"\/24\";|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|ENB_IPV4_ADDRESS_FOR_S1U.*;|ENB_IPV4_ADDRESS_FOR_S1U              = \""+VNF_IP+"\/24\";|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|ENB_IPV4_ADDRESS_FOR_X2C.*;|ENB_IPV4_ADDRESS_FOR_X2C              = \""+VNF_IP+"\/24\";|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|local_s_if_name.*;|local_s_if_name  = \"eth0\";|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|remote_s_address.*;|remote_s_address  = \""+PNF_IP+"\";|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|local_s_address.*;|local_s_address  = \""+VNF_IP+"\";|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|eutra_band.*;|eutra_band              			      = "+band+";|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|downlink_frequency.*;|downlink_frequency      			      ="+downlink+";|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|uplink_frequency_offset.*;|uplink_frequency_offset 			      = "+uplink+";|g" , "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

    if FLEXRAN_enable:
        sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i","s|FLEXRAN_ENABLED.*;|FLEXRAN_ENABLED        = \"yes\";|g" , "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i","s|FLEXRAN_INTERFACE_NAME.*;|FLEXRAN_INTERFACE_NAME = \"eth0\";|g" , "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i","s|FLEXRAN_IPV4_ADDRESS.*;|FLEXRAN_IPV4_ADDRESS   = \""+FLEXRAN_IP+"\";|g" , "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

    sp.call(["kubectl","-n",namespace,"exec",PNF_POD,"--", "apt-get","install","-y","iputils-ping","net-tools"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--","sudo","-E","./targets/bin/lte-softmodem.Rel15","-O","./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf",">","/dev/null","2>&1","&"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",PNF_POD,"--","sudo","-E","./targets/bin/lte-softmodem.Rel15","-O","./ci-scripts/conf_files/ue.nfapi.conf","--L2-emul","3","--num-ues","6","--nokrnmod","1", ">","/dev/null","2>&1","&"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    time.sleep(5)

    sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--","killall","lte-uesoftmodem.Rel15"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",PNF_POD,"--","killall","lte-uesoftmodem.Rel15"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

    sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--","./ran.sh",">","/dev/null","2>&1","&"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    sp.call(["kubectl","-n",namespace,"exec",PNF_POD,"--","./ran.sh",">","/dev/null","2>&1","&"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

if option == "enb":
    sp.call(["helm", "install", "./helm-charts/simplechart/", "--generate-name","--set","name=enb","--set","namespace="+namespace,"--set","mode="+mode,"--set", "node="+allocation_enb], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

