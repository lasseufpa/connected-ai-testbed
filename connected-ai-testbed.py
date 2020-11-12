import yaml
import subprocess as sp
from subprocess import Popen, PIPE, STDOUT
try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


with open("config.yaml", "r") as ymlfile:
    core_yaml = yaml.safe_load(ymlfile)

# Declare variables to be passed into your helm-chart.
name = core_yaml["id"]
option = core_yaml["option"]
allocation_amf = core_yaml["allocation"]["amf"]
allocation_upf = core_yaml["allocation"]["upf"]
allocation_hss = core_yaml["allocation"]["hss"]
allocation_smf = core_yaml["allocation"]["smf"]
allocation_pcrf = core_yaml["allocation"]["pcrf"]
allocation_database = core_yaml["allocation"]["database"]
allocation_webapp = core_yaml["allocation"]["webapp"]

#Create NameSpace
#Check if already exists
CheckNamespace = sp.getoutput(["kubectl get ns |  grep -c"+name])
if CheckNamespace != "0":
  print('ID scenario already exists! Please, change the ID and try again')
  quit()
#Creating
sp.call(["kubectl", "create", "namespace", name], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)



