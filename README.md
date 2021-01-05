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

## Key Concepts

* [Free5GC](https://www.free5gc.org/): The free5GC is an open-source project for 5th generation (5G) mobile core networks. The source code of free5GC stage 1 can be downloaded from [here](https://bitbucket.org/nctu_5g/free5gc-stage-1/src/master/).

* [OAI Radio Access Network (OAI-RAN)](https://www.openairinterface.org/?page_id=2763): This project implements 4G LTE and 5G Radio Access Network. Both ENodeB and User Equipment (UE) are implemented. 

  * Already today OAI offers several functional splits, for example between the Radio Cloud Center (RCC) and a Remote Radio Unit (RRU), know as [C-RAN mode of the OAI eNB](https://gitlab.eurecom.fr/oai/openairinterface5g/-/wikis/how-to-connect-cots-ue-to-oai-enb-via-ngfi-rru).

  * Also, OAI can be run in both monolithic ENodeB mode and [nFAPI mode](https://gitlab.eurecom.fr/oai/openairinterface5g/-/wikis/nFAPI-howto) (which PNF runs PHY and VNF runs MAC,etc).

* [FlexRAN](http://mosaic5g.io/flexran/): A Flexible and programmable platform for Software-Defined Radio Access Networks.

## Prerequisites

[Free5GC Minimum Requirements](https://www.free5gc.org/installation)

[OAI-RAN Minimum Requirements](https://gitlab.eurecom.fr/oai/openairinterface5g/-/wikis/OpenAirSystemRequirements)

[OAI-RAN Kernel Requirements for RAN](https://gitlab.eurecom.fr/oai/openairinterface5g/-/wikis/OpenAirKernelMainSetup)


Our installation method requires that you first have installed [Docker](https://docs.docker.com/engine/install/), [Docker-Compose](https://docs.docker.com/compose/install/), and [Kubernetes](https://kubernetes.io/docs/setup/) in all computers of the cluster node. 

Our recommended quickstart method to deploy Connected AI testbed is using three cluster nodes (Antenna, Cloud, and Edge). Another option is using only one node (Antenna).

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
git clone --recurse-submodules https://gitlab.lasse.ufpa.br/2020-ai-testbed/ai-testbed/connected-ai-testbed
```

Step 6: Build the OAI-RAN and Free5GC Docker images in all kubernetes cluster nodes, for that, inside /oai-ran-docker and /free5gc-docker-kube/cluster paths run:

```
docker-compose build
```

## Configuration

The default configuration is the Core, Radio Cloud Center (RCC) and Remote Radio Unit (RRU) on individual nodes. To change, modify `core.yaml`, `ran.yaml` and/or `flexran.yaml`  according to the desired configuration.

## Run

### `run.py`

Run `run.py ` to create CORE, RAN, and/or FLEXRAN.  

`-c`: This option results in reading the indicate <.yaml> file and creating a Core that contain these file configuration.

`-r`: This option results in reading the indicate <.yaml> file and creating a RAN that contain these file configuration.

`-f`: This option results in reading the indicate <.yaml> file and creating a FlexRAN that contain these file configuration.

Usage example:

 `python3.6 run.py -c core.yaml -r ran.yaml  -f flexran.yaml` 

## Multiple scenarios 

Multiple scenarios are created by associating IDs of CORE, RAN, and FLEXRAN types.

## User management

To acess the Core User management visit: 

`http://<CORE NODE IP>: <WEBAPP service port>/`