import subprocess as sp
from subprocess import Popen, PIPE, STDOUT
try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

i = 0

while True:

    counter_1 = int(sp.getoutput('kubectl logs $(kubectl get pod -l app=amf -o jsonpath=\"{.items[0].metadata.name}\") | grep -c \'Lost IF4p5 connection\''))

    RRU_POD = sp.getoutput('kubectl get pod -l app=rru -o jsonpath="{.items[0].metadata.name}"')
    RCC_POD = sp.getoutput('kubectl get pod -l app=rcc -o jsonpath="{.items[0].metadata.name}"')

    if (counter_1 != i):
        i= i + 1

        sp.call(["kubectl", "exec", RRU_POD, "--", "killall", "lte-softmodem.Rel14"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.call(["kubectl", "exec", RCC_POD, "--", "killall", "lte-softmodem.Rel14"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)

        sp.run(["kubectl", "exec", RCC_POD, "--", "bash", "./ran.sh"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        sp.run(["kubectl", "exec", RRU_POD, "--", "bash", "./ran.sh"], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        
