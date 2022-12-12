# Fast-Kubeflow
This repo covers Kubeflow Environment with LABs: Kubeflow, Pipeline, Experiments, Run, Minio, etc. Possible usage scenarios are aimed to update over time.

Kubeflow supposes Machine Learning (ML) Pipeline that runs on Kubernetes (K8s) Cluster. Kubeflow uses the power of the K8s (Clusters and Autoscaling). Each step of the process in the ML Pipeline is container. Hence, each step can be isolated, run parallel (if they are not in sequence). 

## Prerequisite
- Have a knowledge of 
  - Container Technology (Docker). You can learn it from here => [Fast-Docker](https://github.com/omerbsezer/Fast-Docker)
  - Container Orchestration Technology (Kubernetes). You can learn it from here => [Fast-Kubernetes](https://github.com/omerbsezer/Fast-Kubernetes)
  
**Keywords:** Kubeflow, ML Pipeline, MLOps, AIOps

# Quick Look (HowTo): Scenarios - Hands-on LABs
- [LAB: Creating LAB Environment (WSL2), Installing Kubeflow with MicroK8s, Juju on Ubuntu 20.04](https://github.com/omerbsezer/Fast-Kubeflow/blob/main/Installing-Kubeflow.md)
- [LAB: Creating LAB Environment, Installing MiniKF with Vagrant]()
- [LAB: Kubeflow: Decision Tree, Logistic Regression Example]()

# Table of Contents
- [Motivation](#motivation)
- [What is Kubelow?](#whatIsKubeflow)
- [How Kubeflow Works?](#howKubeflowWorks)
- [What is Kubernetes?](#whatisKubeflow)
- [What are Containers (Docker)?](#whatareContainers)
- [Installing Kubeflow](#labEnvironment)
- [Kubeflow Basics](#basics)
- [Kubeflow Jupyter Notebook](#notebook)
- [Kubeflow Pipeline](#pipeline)
- [KALE (Kubeflow Automated PipeLines Engine)](#kale)
- [Katib](#katib)
- [Minio (Object Storage)](#minio)
- [Project1: Creating ML Pipeline with Custom Docker Images (Decision Tree, Logistic Regression)](#project1)
- [Project2: KALE Use Case (Titanic)](#project2)
- [Project3: CNN Kubeflow (Mnist)](#project3)
- [Project4: LSTM, RNN Kubeflow (NLP)](#project4)
- [Project5: Distributed Training with TFServing](#project5)
- [Other Useful Resources Related Kubeflow](#resource)
- [References](#references)

## Motivation <a name="motivation"></a>

Why should we use / learn Kubeflow? 

- Kubeflow uses containers to run steps of ML algorithms on PC cluster.
- Kubeflow supports parallel training (with Tensorflow).
- Kubeflow provides Machine Learning (ML) data pipeline.
- It saves pipelines, experiments, run (experiment tracking on Kubeflow).
- Kubeflow is free, open source platform that runs on on-premise or any cloud (AWS, Google Cloud, Azure).
- It includes Jupyter Notebook to develop ML algorithms, user interface to show pipeline.

## What is Kubelow <a name="whatIsKubeflow"></a>


## How Kubeflow Works? <a name="howKubeflowWorks"></a>


## What is Kubernetes? <a name="whatisKubeflow"></a>

- To learn about Kubernetes: https://github.com/omerbsezer/Fast-Kubernetes 

## What are Containers (Docker)? <a name="#whatareContainers"></a>


- To learn about Docker and Containers: https://github.com/omerbsezer/Fast-Docker

## Installing Kubeflow <a name="labEnvironment"></a>

- [LAB: Creating LAB Environment (WSL2), Installing Kubeflow](https://github.com/omerbsezer/Fast-Kubeflow/blob/main/Installing-Kubeflow.md) 

## Kubeflow Basics <a name="basics"></a>


## Kubeflow Jupyter Notebook <a name="notebook"></a>

## Kubeflow Pipeline <a name="pipeline"></a>

## KALE (Kubeflow Automated PipeLines Engine) <a name="kale"></a>

## Katib <a name="katib"></a>


## Minio (Object Storage) <a name="minio"></a>

- [LAB: Creating LAB Environment (WSL2), Installing Kubeflow](https://github.com/omerbsezer/Fast-Kubeflow/blob/main/Installing-Kubeflow.md) 

## Other Useful Resources Related Kubeflow <a name="resource"></a>


## References <a name="references"></a>

