import yaml
import time
import subprocess as sp
from subprocess import Popen, PIPE, STDOUT

try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


with open("configuration.yaml", "r") as ymlfile:
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

#Creating deployments
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
