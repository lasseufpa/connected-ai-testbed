import yaml
import time
import subprocess as sp
from subprocess import Popen, PIPE, STDOUT

try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


with open("core.yaml", "r") as ymlfile:
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
CheckNamespace = sp.getoutput(["kubectl get ns |  grep -c"+namespace])
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


sp.call(["kubectl","-n",namespace,"exec",UPF_POD,"--", "/root/setup.sh"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
print("UPF function configurated")
sp.call(["kubectl","-n",namespace,"exec",MONGO_POD,"--", "/usr/src/data/setup-lasse.sh",MONGO_IP], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
print("Default database created")
time.sleep(15)
sp.call(["kubectl","-n",namespace,"exec",WEBAPP_POD,"--","/root/setup.sh",MONGO_IP], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
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

