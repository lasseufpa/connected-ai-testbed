import yaml
import time
import subprocess as sp
from subprocess import Popen, PIPE, STDOUT

try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


def core(f):
    with open(f, "r") as ymlfile:
        core_yaml = yaml.safe_load(ymlfile)

    # Declare variables to be passed into your helm-chart.
    namespace = core_yaml["id"]
    mode = core_yaml["mode"]
    allocation_amf = core_yaml["allocation"]["amf"]
    allocation_upf = core_yaml["allocation"]["upf"]
    allocation_hss = core_yaml["allocation"]["hss"]
    allocation_smf = core_yaml["allocation"]["smf"]
    allocation_pcrf = core_yaml["allocation"]["pcrf"]
    allocation_database = core_yaml["allocation"]["database"]
    allocation_webapp = core_yaml["allocation"]["webapp"]

    #Create NameSpace
    #Check if already exists
    CheckNamespace = sp.getoutput(["kubectl get ns |  grep -c "+namespace])
    if CheckNamespace != "0":
        print('ID scenario already exists! Please, change the ID and try again')
        quit()
    #Creating
    sp.call(["kubectl", "create", "namespace", namespace], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    print("namespace created")

    #Creating deployments using Helm Charts
    sp.call(["helm", "install", "./helm-charts/free5gc/", "--generate-name","--set","name=mongo-lasse","--set","namespace="+namespace,"--set","mode="+mode,"--set", "node="+allocation_database], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    time.sleep(5)
    sp.call(["helm", "install", "./helm-charts/free5gc/", "--generate-name","--set","name=amf","--set","namespace="+namespace,"--set","mode="+mode,"--set", "node="+allocation_amf], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    time.sleep(5)
    sp.call(["helm", "install", "./helm-charts/free5gc/", "--generate-name","--set","name=hss","--set","namespace="+namespace,"--set","mode="+mode,"--set", "node="+allocation_hss], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    time.sleep(5)
    sp.call(["helm", "install", "./helm-charts/free5gc/", "--generate-name","--set","name=upf","--set","namespace="+namespace,"--set","mode="+mode,"--set", "node="+allocation_upf], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    time.sleep(5)
    sp.call(["helm", "install", "./helm-charts/free5gc/", "--generate-name","--set","name=smf","--set","namespace="+namespace,"--set","mode="+mode,"--set", "node="+allocation_smf], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    time.sleep(5)
    sp.call(["helm", "install", "./helm-charts/free5gc/", "--generate-name","--set","name=pcrf","--set","namespace="+namespace,"--set","mode="+mode,"--set", "node="+allocation_pcrf], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    time.sleep(5)
    sp.call(["helm", "install", "./helm-charts/free5gc/", "--generate-name","--set","name=webapp","--set","namespace="+namespace,"--set","mode="+mode,"--set", "node="+allocation_webapp], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    print("Pods created")

    #Starting All Functions
    MONGO_POD = sp.getoutput('kubectl get pod -l app=mongo-lasse -o jsonpath="{.items[0].metadata.name}" -n'+namespace)
    HSS_POD = sp.getoutput('kubectl get pod -l app=hss -o jsonpath="{.items[0].metadata.name}" -n'+namespace)
    AMF_POD = sp.getoutput('kubectl get pod -l app=amf -o jsonpath="{.items[0].metadata.name}" -n'+namespace)
    UPF_POD = sp.getoutput('kubectl get pod -l app=upf -o jsonpath="{.items[0].metadata.name}" -n'+namespace)
    SMF_POD = sp.getoutput('kubectl get pod -l app=smf -o jsonpath="{.items[0].metadata.name}" -n'+namespace)
    PCRF_POD = sp.getoutput('kubectl get pod -l app=pcrf -o jsonpath="{.items[0].metadata.name}" -n'+namespace)
    WEBAPP_POD = sp.getoutput('kubectl get pod -l app=webapp -o jsonpath="{.items[0].metadata.name}" -n'+namespace)

    MONGO_IP = sp.getoutput('kubectl get pod -l app=mongo-lasse -o jsonpath="{.items[0].status.podIP}" -n'+namespace)
    HSS_IP = sp.getoutput('kubectl get pod -l app=hss -o jsonpath="{.items[0].status.podIP}" -n'+namespace)
    AMF_IP = sp.getoutput('kubectl get pod -l app=amf -o jsonpath="{.items[0].status.podIP}" -n'+namespace)
    UPF_IP = sp.getoutput('kubectl get pod -l app=upf -o jsonpath="{.items[0].status.podIP}" -n'+namespace)
    SMF_IP = sp.getoutput('kubectl get pod -l app=smf -o jsonpath="{.items[0].status.podIP}" -n'+namespace)
    PCRF_IP = sp.getoutput('kubectl get pod -l app=pcrf -o jsonpath="{.items[0].status.podIP}" -n'+namespace)


    sp.call(["kubectl","-n",namespace,"exec",UPF_POD,"--", "bash","/root/setup.sh"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    print("UPF function configurated")
    sp.call(["kubectl","-n",namespace,"exec",MONGO_POD,"--","bash", "/usr/src/data/setup-lasse.sh",MONGO_IP], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    print("Default database created")
    time.sleep(15)
    sp.Popen(["kubectl","-n",namespace,"exec",WEBAPP_POD,"--","bash","/root/setup.sh",MONGO_IP], stdout=sp.PIPE, stderr=sp.STDOUT)
    print("Webapp configurated")

    sp.call(["kubectl","-n",namespace,"exec",HSS_POD,"--","./setup-lasse.sh",MONGO_IP, HSS_IP, AMF_IP, UPF_IP, SMF_IP, PCRF_IP], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    time.sleep(5)
    sp.call(["kubectl","-n",namespace,"exec",AMF_POD,"--","./setup-lasse.sh", MONGO_IP, HSS_IP, AMF_IP, UPF_IP, SMF_IP, PCRF_IP], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    time.sleep(5)
    sp.call(["kubectl","-n",namespace,"exec",UPF_POD,"--","./setup-lasse.sh", MONGO_IP, HSS_IP, AMF_IP, UPF_IP, SMF_IP, PCRF_IP], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    time.sleep(5)
    sp.call(["kubectl","-n",namespace,"exec",SMF_POD,"--","./setup-lasse.sh", MONGO_IP, HSS_IP, AMF_IP, UPF_IP, SMF_IP, PCRF_IP], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    time.sleep(5)
    sp.call(["kubectl","-n",namespace,"exec",PCRF_POD,"--","./setup-lasse.sh", MONGO_IP, HSS_IP, AMF_IP, UPF_IP, SMF_IP, PCRF_IP], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    time.sleep(5)
    print("All functions started")

def flexran(f):
    with open(f, "r") as ymlfile:
        flexran_yaml = yaml.safe_load(ymlfile)

    # Declare variables to be passed into your helm-chart.
    namespace = flexran_yaml["id"]
    mode = flexran_yaml["mode"]
    allocation = flexran_yaml["allocation"]["flexran"]

    #Create NameSpace
    #Check if already exists
    CheckNamespace = sp.getoutput(["kubectl get ns |  grep -c "+namespace])
    if CheckNamespace != "0":
        print('ID scenario already exists! Please, change the ID and try again')
        quit()
    #Creating
    sp.call(["kubectl", "create", "namespace", namespace], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

    #Creating deployments using Helm Charts
    sp.call(["helm", "install", "./helm-charts/simplechart/", "--generate-name","--set","name=flexran-controller","--set","namespace="+namespace,"--set","mode="+mode,"--set", "node="+allocation], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    time.sleep(10)

    #Starting
    FLEXRAN_POD = sp.getoutput('kubectl get pod -l app=flexran-controller -o jsonpath="{.items[0].metadata.name}" -n'+namespace)
    sp.Popen(["kubectl","-n",namespace,"exec",FLEXRAN_POD,"--","./run_flexran_rtc.sh"], stdout=sp.PIPE, stderr=sp.STDOUT)
    print("Flexran created")

def ran(f):
    with open(f, "r") as ymlfile:
        ran_yaml = yaml.safe_load(ymlfile)

    # Declare variables to be passed into your helm-chart.
    namespace = ran_yaml["id"]
    option = ran_yaml["option"]
    mode = ran_yaml["mode"]

    CORE_ID = ran_yaml["CORE_ID"]
    coreIP = sp.getoutput('kubectl get pod -l app=amf -o jsonpath="{.items[0].status.podIP}" -n'+CORE_ID)
    print("CORE ID:"+CORE_ID)
    print(coreIP)

    FLEXRAN_enable = ran_yaml["FLEXRAN"]["FLEXRAN_enable"]
    
    if FLEXRAN_enable:
        FLEXRAN_ID=ran_yaml["FLEXRAN"]["FLEXRAN_ID"]
        FLEXRAN_IP = sp.getoutput('kubectl get pod -l app=flexran-controller -o jsonpath="{.items[0].status.podIP}" -n'+FLEXRAN_ID)
        print("FLEXRAN IP:"+FLEXRAN_ID)
        print(FLEXRAN_IP)

    band = ran_yaml["other-params"]["band"]
    downlink = ran_yaml["other-params"]["downlink"]
    uplink = ran_yaml["other-params"]["uplink"]
    eNB_ID = ran_yaml["other-params"]["eNB_ID"]
    MCC = ran_yaml["other-params"]["MCC"]
    MNC = ran_yaml["other-params"]["MCC"]
    N_RB_DL = ran_yaml["other-params"]["N_RB_DL"]
    tx_gain = ran_yaml["other-params"]["tx_gain"]
    rx_gain = ran_yaml["other-params"]["rx_gain"]
    
    #Create NameSpace

    #Check if already exists
    CheckNamespace = sp.getoutput(["kubectl get ns |  grep -c "+namespace])
    if CheckNamespace != "0":
        print('ID scenario already exists! Please, change the ID and try again')
        quit()
    
    #Creating
    sp.call(["kubectl", "create", "namespace", namespace], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

    #Creating deployments using Helm Charts
    if option == "rcc-rru":

        allocation_rcc = ran_yaml["allocation"]["rcc"]
        allocation_rru = ran_yaml["allocation"]["rru"]
    
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

        sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|eNB_ID.*;|eNB_ID    =  "+eNB_ID+";|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|mcc = 208;|mcc = "+MCC+";|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|mnc = 92;|mnc = "+MNC+";|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|N_RB_DL.*;|N_RB_DL                 			      = "+N_RB_DL+";|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|tx_gain.*;|tx_gain                                            = "+tx_gain+";|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",RCC_POD,"--", "sed", "-i", "s|rx_gain.*;|rx_gain                                            = "+rx_gain+";|g", "./ci-scripts/conf_files/rcc.band7.tm1.if4p5.lo.25PRB.usrpb210.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

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
        allocation_vnf = ran_yaml["allocation"]["vnf"]
        allocation_pnf = ran_yaml["allocation"]["pnf"]

        sp.call(["helm", "install", "./helm-charts/simplechart/", "--generate-name","--set","name=vnf","--set","namespace="+namespace,"--set","mode="+mode,"--set", "node="+allocation_vnf], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        print("VNF CREATED")
        time.sleep(15)
        sp.call(["helm", "install", "./helm-charts/simplechart/", "--generate-name","--set","name=pnf","--set","namespace="+namespace,"--set","mode="+mode,"--set", "node="+allocation_pnf], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        print("PNF CREATED")
        time.sleep(15)
        print("Setting ...")
        VNF_POD = sp.getoutput('kubectl get pod -l app=vnf -o jsonpath="{.items[0].metadata.name}" -n'+namespace)
        PNF_POD = sp.getoutput('kubectl get pod -l app=pnf -o jsonpath="{.items[0].metadata.name}" -n'+namespace)
        VNF_IP = sp.getoutput('kubectl get pod -l app=vnf -o jsonpath="{.items[0].status.podIP}" -n'+namespace)
        PNF_IP = sp.getoutput('kubectl get pod -l app=pnf -o jsonpath="{.items[0].status.podIP}" -n'+namespace)

        sp.call(["kubectl","-n",namespace,"exec",PNF_POD,"--", "sed", "-i", "s|local_n_if_name.*;|local_n_if_name = \"eth0\";|g", "./ci-scripts/conf_files/ue.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",PNF_POD,"--", "sed", "-i", "s|remote_n_address.*;|remote_n_address=\""+VNF_IP+"\";|g", "./ci-scripts/conf_files/ue.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",PNF_POD,"--", "sed", "-i", "s|local_n_address.*;|local_n_address=\""+PNF_IP+"\";|g", "./ci-scripts/conf_files/ue.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",PNF_POD,"--", "sed", "-i", "s|bands.*;|bands                            = ["+band+"];|g", "./ci-scripts/conf_files/ue.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

        sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|eNB_ID.*;|eNB_ID    =  "+eNB_ID+";|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|mcc = 208;|mcc = "+MCC+";|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|mnc = 92;|mnc = "+MNC+";|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|N_RB_DL.*;|N_RB_DL                 			      = "+N_RB_DL+";|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|tx_gain.*;|tx_gain                                            = "+tx_gain+";|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl","-n",namespace,"exec",VNF_POD,"--", "sed", "-i", "s|rx_gain.*;|rx_gain                                            = "+rx_gain+";|g", "./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        
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

        print("Setting finished.")
        print("Installing required packages ...")
        sp.call(["kubectl","-n",namespace,"exec",PNF_POD,"--", "apt-get","install","-y","iputils-ping","net-tools"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        print("Starting..VNF")
        sp.Popen(["kubectl","-n",namespace,"exec",VNF_POD,"--","sudo","-E","./targets/bin/lte-softmodem.Rel15","-O","./ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf"], stdout=sp.PIPE, stderr=sp.STDOUT)
        print("Starting..PNF")
        sp.Popen(["kubectl","-n",namespace,"exec",PNF_POD,"--","sudo","-E","./targets/bin/lte-uesoftmodem.Rel15","-O","./ci-scripts/conf_files/ue.nfapi.conf","--L2-emul","3","--num-ues","6","--nokrnmod","1"], stdout=sp.PIPE, stderr=sp.STDOUT)
        time.sleep(15)
        print("Checking...")
    
        sp.Popen(["kubectl","-n",namespace,"exec",PNF_POD,"--","sudo","killall","lte-uesoftmodem.Rel15"], stdout=sp.PIPE, stderr=sp.STDOUT)
        sp.Popen(["kubectl","-n",namespace,"exec",PNF_POD,"--","sudo","./ran.sh"], stdout=sp.PIPE, stderr=sp.STDOUT)
    
        sp.Popen(["kubectl","-n",namespace,"exec",VNF_POD,"--","sudo","killall","lte-softmodem.Rel15"], stdout=sp.PIPE, stderr=sp.STDOUT)
        sp.Popen(["kubectl","-n",namespace,"exec",VNF_POD,"--","sudo","./ran.sh"], stdout=sp.PIPE, stderr=sp.STDOUT)

        print("Done")

