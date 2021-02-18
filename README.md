# Connected AI testbed

Connected AI testbed allows building flexible and realistic scenarios where different network topologies for 4G/5G and quickly deploy them. 

![UFPA_Live_5G_Network__2_](https://gitlab.lasse.ufpa.br/2020-ai-testbed/ai-testbed/project-agenda/uploads/300adcf0c0e076aa1499e60b5e477df4/UFPA_Live_5G_Network_.png)

 If you find this project useful in your research, please consider citing:

    @ARTICLE{9290141,
      author={C. V. {Nahum} and L. {De Nóvoa Martins Pinto} and V. B. {Tavares} and P. {Batista} and S. {Lins} and N. {Linder} and A. {Klautau}},
      journal={IEEE Access}, 
      title={Testbed for 5G Connected Artificial Intelligence on Virtualized Networks}, 
      year={2020},
      volume={8},
      number={},
      pages={223202-223213},
      doi={10.1109/ACCESS.2020.3043876}
    }

## Quickstart Guide

This document is a quickstart and a getting started guide in one, intended for your first run-through of Connected AI testbed.

## Open-source platforms used

* [Free5GC](https://www.free5gc.org/): The free5GC is an open-source project for 5th generation (5G) mobile core networks. The source code of free5GC stage 1 can be downloaded from [here](https://bitbucket.org/nctu_5g/free5gc-stage-1/src/master/).

* [OAI Radio Access Network (OAI-RAN)](https://www.openairinterface.org/?page_id=2763): This project implements 4G LTE and 5G Radio Access Network. Both ENodeB and User Equipment (UE) are implemented. 

  * Already today OAI offers several functional splits, for example between the Radio Cloud Center (RCC) and a Remote Radio Unit (RRU), know as [C-RAN mode of the OAI eNB](https://gitlab.eurecom.fr/oai/openairinterface5g/-/wikis/how-to-connect-cots-ue-to-oai-enb-via-ngfi-rru).

  * Also, OAI can be run in both monolithic ENodeB mode and [nFAPI mode](https://gitlab.eurecom.fr/oai/openairinterface5g/-/wikis/nFAPI-howto) (which PNF runs PHY and VNF runs MAC,etc).

* [FlexRAN](http://mosaic5g.io/flexran/): A Flexible and programmable platform for Software-Defined Radio Access Networks.

## Requirements

Note: Please do not try if you don't have Free5GC and OAI-RAN Minimum Requirements as Free5GC and OAI needs lot of packages and its very sensitive to version numbers, linux kernel, etc. 

[Free5GC Minimum Requirements](https://www.free5gc.org/installation)

[OAI-RAN Minimum Requirements](https://gitlab.eurecom.fr/oai/openairinterface5g/-/wikis/OpenAirSystemRequirements)

[OAI-RAN Kernel Requirements for RAN](https://gitlab.eurecom.fr/oai/openairinterface5g/-/wikis/OpenAirKernelMainSetup)

Install [Docker](https://docs.docker.com/engine/install/), [Docker-Compose](https://docs.docker.com/compose/install/), and [Kubernetes](https://kubernetes.io/docs/setup/) in all computers of your cluster. 

## CAI hardware and operating-system

We use the specific hardware and operating-system constraints below for our real-time operation:

  - Three computers with a Core i5-8400 CPU@2666~MHz processor with an operational system Ubuntu 16.04 LTS and a low latency kernel. 

  - One USRP B210 http://www.ettus.com/product/details/UB210-KIT

> In our setup,  we associate each
> of the three machines with 
> functions: cloud, edge and antenna

## Installation

Step 1: [create a Kubernetes Cluster](https://kubernetes.io/docs/tutorials/kubernetes-basics/create-cluster/). 

Step 2: [install Helm](https://helm.sh/docs/intro/install/) in your Master Node.

Step 3: Install a Container Network Interface (CNI):

```
kubectl apply -f https://docs.projectcalico.org/v3.11/manifests/calico.yaml
```

Step 4: Label the nodes as antenna, edge or cloud:

```
kubectl label nodes <nodename> environment=<antenna, edge or cloud>
```

Step 5: Clone this Git repository (and submodules):

```
git clone --recurse-submodules https://github.com/lasseufpa/connected-ai-testbed.git
```

Step 6: Build the OAI-RAN and Free5GC Docker images in all kubernetes cluster nodes

> In README of /oai-ran-docker and /free5gc-docker-kube repos 
> you will find a detailed explanation of how to perform the builds

## Configuration

The default configuration is the Core, Radio Cloud Center (RCC) and Remote Radio Unit (RRU) on individual nodes. To change, modify `core.yaml`, `ran.yaml` and/or `flexran.yaml`  according to the desired configuration.

![UFPA_Live_5G_Network__1_](https://www.lasse.ufpa.br/wp-content/uploads/2021/01/core.png)

![UFPA_Live_5G_Network__2_](https://www.lasse.ufpa.br/wp-content/uploads/2021/01/flexran.png)

![UFPA_Live_5G_Network__3_](https://www.lasse.ufpa.br/wp-content/uploads/2021/01/ran.png)

### Real RAN and Emulated RAN 

Our testbed has two possibilities for the RAN: using real equipment and using an emulated version.

> The version using equipment is "rcc-rru" mode
> and the emulated version is "vnf-pnf" mode
> the mode is defined in the RAN configuration file

## Run

### `run.py`

Run `run.py ` to create CORE, RAN, and/or FLEXRAN.  

`-c`: This option results in reading the indicate <.yaml> file and creating a Core that contain these file configuration.

`-r`: This option results in reading the indicate <.yaml> file and creating a RAN that contain these file configuration.

`-f`: This option results in reading the indicate <.yaml> file and creating a FlexRAN that contain these file configuration.

Usage example:

 `python3.6 run.py -c core.yaml -r ran.yaml  -f flexran.yaml` 

 `python3.6 run.py -r ran.yaml` 

## Multiple scenarios 

Multiple scenarios are created by associating IDs of modified CORE, RAN, and FLEXRAN yaml files.

![UFPA_Live_5G_Network__4_](https://www.lasse.ufpa.br/wp-content/uploads/2021/01/exemplo_1.png)

![UFPA_Live_5G_Network__5_](https://www.lasse.ufpa.br/wp-content/uploads/2021/01/exemplo_2.png)

![UFPA_Live_5G_Network__6_](https://www.lasse.ufpa.br/wp-content/uploads/2021/01/exemplo_3.png)

## User management

To acess the Core User management visit: 

`http://<CORE NODE IP>: <WEBAPP service port>/`

The default username and password are “admin” and “1423”.

> For a user to enter the network
> it is necessary that the IMSI, security context (K, OPc, AMF),
> and APN of the user SIMCARD are
> compatible with those inserted in the database