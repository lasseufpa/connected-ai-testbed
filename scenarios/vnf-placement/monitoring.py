import subprocess as sp
from subprocess import Popen, PIPE, STDOUT
try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

i = 0
j = 0

while True:

    counter_1 = int(sp.getoutput('kubectl logs $(kubectl get pod -l app=amf -o jsonpath=\"{.items[0].metadata.name}\") | grep -c \'AM4G overload_start\''))

    HSS_POD = sp.getoutput('kubectl get pod -l app=hss -o jsonpath="{.items[0].metadata.name}"')
    AMF_POD = sp.getoutput('kubectl get pod -l app=amf -o jsonpath="{.items[0].metadata.name}"')
    UPF_POD = sp.getoutput('kubectl get pod -l app=upf -o jsonpath="{.items[0].metadata.name}"')
    SMF_POD = sp.getoutput('kubectl get pod -l app=smf -o jsonpath="{.items[0].metadata.name}"')
    PCRF_POD = sp.getoutput('kubectl get pod -l app=pcrf -o jsonpath="{.items[0].metadata.name}"')
    
    MONGO_IP = sp.getoutput('kubectl get pod -l app=mongo-lasse -o jsonpath="{.items[0].status.podIP}"')
    HSS_IP = sp.getoutput('kubectl get pod -l app=hss -o jsonpath="{.items[0].status.podIP}"')
    AMF_IP = sp.getoutput('kubectl get pod -l app=amf -o jsonpath="{.items[0].status.podIP}"')
    UPF_IP = sp.getoutput('kubectl get pod -l app=upf -o jsonpath="{.items[0].status.podIP}"')
    SMF_IP = sp.getoutput('kubectl get pod -l app=smf -o jsonpath="{.items[0].status.podIP}"')
    PCRF_IP = sp.getoutput('kubectl get pod -l app=pcrf -o jsonpath="{.items[0].status.podIP}"')

    VNF_POD = sp.getoutput('kubectl get pod -l app=vnf -o jsonpath="{.items[0].metadata.name}"')
    PNF_POD = sp.getoutput('kubectl get pod -l app=pnf -o jsonpath="{.items[0].metadata.name}"')

    if (counter_1 != i):
        i= i + 1
        sp.call(["kubectl", "exec", HSS_POD, "--", "pkill", "-9","nextepc"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl", "exec", AMF_POD, "--", "pkill", "-9", "free5gc"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl", "exec", UPF_POD, "--", "pkill", "-9", "free5gc"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl", "exec", SMF_POD, "--", "pkill", "-9", "free5gc"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl", "exec", PCRF_POD, "--", "pkill", "-9", "nextepc"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

        sp.call(["kubectl", "exec", VNF_POD, "--", "killall", "lte-softmodem.Rel15"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl", "exec", PNF_POD, "--", "killall", "lte-uesoftmodem.Rel15"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

        sp.run(["kubectl", "exec", HSS_POD, "--", "./setup-lasse.sh", MONGO_IP, HSS_IP, AMF_IP, UPF_IP, SMF_IP, PCRF_IP], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.run(["kubectl", "exec", AMF_POD, "--", "./setup-lasse.sh", MONGO_IP, HSS_IP, AMF_IP, UPF_IP, SMF_IP, PCRF_IP], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.run(["kubectl", "exec", UPF_POD, "--", "./setup-lasse.sh", MONGO_IP, HSS_IP, AMF_IP, UPF_IP, SMF_IP, PCRF_IP], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.run(["kubectl", "exec", SMF_POD, "--", "./setup-lasse.sh", MONGO_IP, HSS_IP, AMF_IP, UPF_IP, SMF_IP, PCRF_IP], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.run(["kubectl", "exec", PCRF_POD, "--", "./setup-lasse.sh", MONGO_IP, HSS_IP, AMF_IP, UPF_IP, SMF_IP, PCRF_IP], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.run(["kubectl", "exec", VNF_POD, "--", "bash", "./ran.sh"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.run(["kubectl", "exec", PNF_POD, "--", "bash", "./ran.sh"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        
