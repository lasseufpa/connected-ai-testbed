import yaml
import time
import subprocess as sp
from subprocess import Popen, PIPE, STDOUT

try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


with open("flexran.yaml", "r") as ymlfile:
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

