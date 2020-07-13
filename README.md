
# Quickstart Guide

This document is a quickstart and a getting started guide in one, intended for your first run-through of UFPA Live Network 4G/5G (The Connected AI testbed).

We'll first install [Docker](https://www.docker.com/), [Docker-Compose](https://docs.docker.com/compose/), [Kubernetes](https://kubernetes.io/), [Calico](https://www.projectcalico.org/), and [Helm](https://helm.sh/), then we'll setup some configurations to run the available scenarios.

## Overview

UFPA Live Network 4G/5G (The Connected AI testbed) allows building flexible and realistic scenarios where different network topologies for 4G/5G and quickly deploy them. 

![UFPA_Live_5G_Network__2_](https://gitlab.lasse.ufpa.br/2020-ai-testbed/ai-testbed/project-agenda/uploads/b63d4f758f295f2a81d009275999fff2/UFPA_Live_5G_Network__2_.png)


## Available scenarios

**VNF-PLACEMENT**


|            | antenna | edge        | cloud                |
|:----------:|---------|-------------|----------------------|
| ALL-IN- ONE | VNF, PNF, FLEXRAN-CONTROLLER and Core     |         |                 |
| AMF-EDGE-SCENARIO | PNF   | VNF+AMF+FLEXRAN-CONTROLLER     | Core w/o AMF         |
| AMF-UPF-SCENARIO | PNF     | VNF+AMF+UPF+FLEXRAN-CONTROLLER | Core w/o AMF and UPF |
| CRAN-SCENARIO| PNF     | VNF+FLEXRAN-CONTROLLER | Core |
| MONOLITH-SCENARIO| PNF+VNF    | FLEXRAN-CONTROLLER | Core |

**DRONE**


|            | antenna | edge        | cloud                |
|:----------:|---------|-------------|----------------------|
| ALL-IN- ONE | RCC, RRU, FLEXRAN-CONTROLLER and Core     |         |                 |
| AMF-EDGE-SCENARIO | RRU   | RCC+AMF+FLEXRAN-CONTROLLER     | Core w/o AMF         |
| AMF-UPF-SCENARIO | RRU     | RCC+AMF+UPF+FLEXRAN-CONTROLLER | Core w/o AMF and UPF |
| CRAN-SCENARIO| RRU     | RCC+FLEXRAN-CONTROLLER | Core |
| MONOLITH-SCENARIO| RCC+RRU    | FLEXRAN-CONTROLLER | Core |

## Key Concepts

* [Free5gc](https://www.free5gc.org/): The free5GC is an open-source project for 5th generation (5G) mobile core networks. The source code of free5GC stage 1 can be downloaded from [here](https://bitbucket.org/nctu_5g/free5gc-stage-1/src/master/).

* [OAI Radio Access Network (OAI-RAN)](https://www.openairinterface.org/?page_id=2763): This project implements 4G LTE and 5G Radio Access Network. Both ENodeB and User Equipment (UE) are implemented. 

  * Already today OAI offers several functional splits, for example between the Radio Cloud Center (RCC) and a Remote Radio Unit (RRU), know as [C-RAN mode of the OAI eNB](https://gitlab.eurecom.fr/oai/openairinterface5g/-/wikis/how-to-connect-cots-ue-to-oai-enb-via-ngfi-rru).

  * Also, OAI can be run in both monolithic ENodeB mode and [nFAPI mode](https://gitlab.eurecom.fr/oai/openairinterface5g/-/wikis/nFAPI-howto) (which PNF runs PHY and VNF runs MAC,etc).

* [Flexran](http://mosaic5g.io/flexran/): A Flexible and programmable platform for Software-Defined Radio Access Networks.

## Prerequisites

Node Minimum Requirement:

Software:
* OS: Ubuntu 18.04
* Linux kernel: 4.15.0-43-generic

Hardware
* CPU: Intel i5 processor
* RAM: 4GB
* Hard drive: 160G
* NIC card: 1Gbps ethernet card
* USRP B210

Our installation method requires that you first have installed [Docker](https://docs.docker.com/engine/install/), [Docker-Compose](https://docs.docker.com/compose/install/), and [Kubernetes](https://kubernetes.io/docs/setup/) in all cluster nodes. Our recommended quickstart method to deploy UFPA Live Network 4G/5G is using three cluster nodes (Antenna, Cloud, and Edge), or, another option is using only one node (Antenna).

## Installation

Firstly, [create a Kubernetes Cluster](https://kubernetes.io/docs/tutorials/kubernetes-basics/create-cluster/). In the Master node install a Container Network Interface (CNI) that will work as our network manager with the following command:

```
kubectl apply -f https://docs.projectcalico.org/v3.11/manifests/calico.yaml
```

The next step is to build the OAI-RAN and Free5GC Docker images. For this, clone this Git repository (and submodules):

```
git clone --recurse-submodules https://gitlab.lasse.ufpa.br/2020-ai-testbed/ai-testbed/connected-ai-testbed
```

And inside /oai-ran-docker and /free5gc-docker-kube/cluster paths run:

```
docker-compose build
```

Now, between your nodes you should label which you will use as Antenna, Edge or Cloud. In Master node run:

```
kubectl label nodes <nodename> environment=<antenna, edge or cloud>
```

Antenna | Edge | Cloud
:--------- | :------: | -------:
Core | AMF, UPF | Core
VNF, PNF, RCC, RRU | VNF, RCC | -
FLEXRAN-CONTROLLER | FLEXRAN-CONTROLLER| -

Last step, [install Helm](https://helm.sh/docs/intro/install/) in your Master Node.


## Create scenarios

To create the desired scenario, just access the scenario folder inside any of our categories folders and run:

```
bash create-scenario.sh
```

To end the scenario:

```
finish create-scenario.sh
```

## Logs 

Access logs of each pod through master node:

```shell
kubectl logs <pod name>
```
