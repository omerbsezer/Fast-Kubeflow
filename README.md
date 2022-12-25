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
- [LAB: Creating LAB Environment, Installing MiniKF with Vagrant](https://github.com/omerbsezer/Fast-Kubeflow/blob/main/Using-MiniKF.md)
- [LAB: Project1, Kubeflow Pipeline (From Scratch) with Custom Docker Images (Decision Tree, Logistic Regression)]()

# Table of Contents
- [Motivation](#motivation)
- [What is Kubelow?](#whatIsKubeflow)
- [How Kubeflow Works?](#howKubeflowWorks)
- [What is Container (Docker)?](#whatareContainers)
- [What is Kubernetes?](#whatisKubeflow)
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
- It saves pipelines, experiments, and runs (experiment tracking on Kubeflow). 
- It provides easy, repeatable, portable deployments on a diverse infrastructure (for example, experimenting on a laptop, then moving to an on-premises cluster or to the cloud).
- Kubeflow provides deploying and managing loosely-coupled microservices and scaling based on demand.
- Kubeflow is free, open source platform that runs on on-premise or any cloud (AWS, Google Cloud, Azure).
- It includes Jupyter Notebook to develop ML algorithms, user interface to show pipeline.
- "Kubeflow started as an open sourcing of the way Google ran TensorFlow internally, based on a pipeline called TensorFlow Extended. It began as just a simpler way to run TensorFlow jobs on Kubernetes, but has since expanded to be a multi-architecture, multi-cloud framework for running entire machine learning pipelines." (ref: [kubeflow.org](https://v0-7.kubeflow.org/docs/)) 
- **Kubeflow applies to become a CNCF incubating project**, it is announced on 24 October 2022 (ref: [opensource.googleblog.com](https://opensource.googleblog.com/2022/10/kubeflow-applies-to-become-a-cncf-incubating-project.html)).

## What is Kubelow <a name="whatIsKubeflow"></a>
- "The Kubeflow project is dedicated to making deployments of machine learning (ML) workflows on Kubernetes simple, portable and scalable." (ref: kubeflow.org) 
- "Kubeflow has developed into an end-to-end, extendable ML platform, with multiple distinct components to address specific stages of the ML lifecycle: model development (**Kubeflow Notebooks**), model training (**Kubeflow Pipelines** and **Kubeflow Training Operator**), model serving (**KServe**), and automated machine learning (**Katib**)" (ref: opensource.googleblog.com).
- Kubeflow is a type of ML data pipeline application that provides to create ML data pipeline (saving model and artifacts, running multiple times) like [Airflow](https://airflow.apache.org/)

## How Kubeflow Works? <a name="howKubeflowWorks"></a>
- **Kubeflow** works on **Kubernetes** platform with **Docker Containers**.
- Kubernetes creates the node clusters with many servers and PCs. Kubeflow is a distributed application (~35 pods) running on the Kubernetes platform. Kubeflow pods are running on the different nodes if there are several nodes connected to the Kubernetes cluster. 
- Containers include Python Machine learning (ML) codes that are each step of the ML pipeline (e.g. Dowloading data function, decision tree classifier, linear regression classifier, evaluation part, etc.) 

  ![image](https://user-images.githubusercontent.com/10358317/209439403-97e1d4b0-846f-486e-b2e7-950f9708d8ba.png)
  
- Containers' outputs can be able to connect to the other containers' inputs. With this feature, it is possible to create DAG (Directed Acyclic Graph) with containers. Each function can be able to run on the seperate containers. 

  ![image](https://user-images.githubusercontent.com/10358317/209439487-214d6be2-5845-4548-81ec-79895fecd7d9.png)
  (ref: kubeflow-pipelines towardsdatascience)
  
- If you want to learn the details of the working of Kubeflow, you should learn:
  - 1. Docker Containers
  - 2. Kubernetes    

## What is Container (Docker)? <a name="#whatareContainers"></a>
- Docker is a tool that reduces the gap between Development/Deployment phase of a software development cycle.
- Docker is like VM but it has more features than VMs (no kernel, only small app and file systems, portable)
    - On Linux Kernel (2000s) two features are added (these features support Docker):
        - Namespaces: Isolate process.
        - Control Groups: Resource usage (CPU, Memory) isolation and limitation for each process. 
- Without Docker containers, each VM consumes 30% resources (Memory, CPU)

  ![image](https://user-images.githubusercontent.com/10358317/113183089-ef51fa00-9253-11eb-9ade-771905ce8ebd.png) (Ref: Docker.com)

  ![image](https://user-images.githubusercontent.com/10358317/113183210-0db7f580-9254-11eb-9716-0de635f3cbdf.png) (Ref: docs.docker.com)
  
- **To learn about Docker and Containers, please go to this repo:** https://github.com/omerbsezer/Fast-Docker

## What is Kubernetes? <a name="whatisKubeflow"></a>
- "Kubernetes is a portable, extensible, open-source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation. It has a large, rapidly growing ecosystem. Kubernetes services, support, and tools are widely available." (Ref: Kubernetes.io)

  ![image](https://user-images.githubusercontent.com/10358317/146247396-5bc3bbf9-41fa-47ff-b10d-cac305379e21.png) (Ref: Kubernetes.io)
  
  ![image](https://user-images.githubusercontent.com/10358317/146250114-18759a06-e6a6-4554-bc7f-b23a13534f77.png) (Ref: Kubernetes.io)

- **To learn about Kubernetes, please go to this repo:** https://github.com/omerbsezer/Fast-Kubernetes 

## Installing Kubeflow <a name="labEnvironment"></a>
- How to install Kubeflow on WSL2 with Juju:
  - [LAB: Creating LAB Environment (WSL2), Installing Kubeflow](https://github.com/omerbsezer/Fast-Kubeflow/blob/main/Installing-Kubeflow.md) 

- To get more features like KALE, and to install in easy way: Use Kubeflow with MiniKF below (preferred)
- **Kubeflow with MiniKF:** How to install MiniKF with Vagrant and VirtualBox:
  - [LAB: Creating LAB Environment, Installing MiniKF with Vagrant](https://github.com/omerbsezer/Fast-Kubeflow/blob/main/Using-MiniKF.md)

## Kubeflow Basics <a name="basics"></a>
- Kubeflow is an ML distributed application that contains following parts:
  - Kubeflow Jupyter Notebook
  - Kubeflow Pipelines
  - KALE (Kubeflow Automated PipeLines Engine)


## Kubeflow Jupyter Notebook <a name="notebook"></a>

## Kubeflow Pipeline <a name="pipeline"></a>
- Kubeflow Pipelines is based on [Argo Workflows](https://github.com/argoproj/argo-workflows) which is a container-native workflow engine for kubernetes.
- Kubeflow Pipelines consists of (ref: Kubeflow-Book):
  - **Python SDK:** allows you to create and manipulate pipelines and their components using Kubeflow Pipelines domain-specific language.
  - **DSL compiler:** allows you to transform your pipeline defined in python code into a static configuration reflected in a YAML file. 
  - **Pipeline Service:** creates a pipeline run from the static configuration or YAML file.
  - **Kubernetes Resources:** the pipeline service connects to kubernetes API in order to define the resources needed to run the pipeline defined in the YAML file.
  - **Artifact Storage:** Kubeflow Pipelines storages metadata and artifacts. Metadata such as experiments, jobs, runs and metrics are stored in a MySQL database. Artifacts such as pipeline packages, large scale metrics and views are stored in an artifact store such as MinIO server.

- Have a look to Kubeflow Pipeline Project:
  - [LAB: Project1, Kubeflow Pipeline (From Scratch) with Custom Docker Images (Decision Tree, Logistic Regression)]()
  
## KALE (Kubeflow Automated PipeLines Engine) <a name="kale"></a>

## Katib <a name="katib"></a>

## KFServing <a name="kfserving"></a>

## Minio (Object Storage) <a name="minio"></a>

- [LAB: Creating LAB Environment (WSL2), Installing Kubeflow](https://github.com/omerbsezer/Fast-Kubeflow/blob/main/Installing-Kubeflow.md) 

## Other Useful Resources Related Kubeflow <a name="resource"></a>


## References <a name="references"></a>
- kubeflow.org: (kubeflow documentation) https://v0-7.kubeflow.org/docs/
- opensource.googleblog.com: https://opensource.googleblog.com/2022/10/kubeflow-applies-to-become-a-cncf-incubating-project.html
- kubeflow-pipelines towardsdatascience: https://towardsdatascience.com/kubeflow-pipelines-how-to-build-your-first-kubeflow-pipeline-from-scratch-2424227f7e5
- Kubernetes.io: https://kubernetes.io/docs/concepts/overview/
- docs.docker.com: https://docs.docker.com/get-started/overview/
- Argo Worflow: https://github.com/argoproj/argo-workflows
- Kubeflow-Book: https://www.amazon.com.mx/Kubeflow-Machine-Learning-Lab-Production/dp/1492050121
