## LAB: Creating LAB Environment (WSL2), Installing Kubeflow

This lab shows:
- how to install Kubeflow using Juju, MicroK8s on WSL2

### Kubeflow

- If you are using Win 10 or Win 11, you should have Linux OS to install kubeflow
  - Install WSL2: https://pureinfotech.com/install-windows-subsystem-linux-2-windows-10/#:~:text=To%20install%20WSL2%20on%20Windows,%E2%80%9Cwsl%20%E2%80%93update%E2%80%9D%20command.
  - Use Ubuntu 20.04
  
- On Powershell:
``` 
wsl --setdefault Ubuntu-20.04
wsl -l -v   # list all wsls
wsl --shutdown  # to shutdown all wsl
``` 

- WSL2 has snap problem:

``` 
sudo apt-get update && sudo apt-get install -yqq daemonize dbus-user-session fontconfig
sudo daemonize /usr/bin/unshare --fork --pid --mount-proc /lib/systemd/systemd --system-unit=basic.target 
exec sudo nsenter -t $(pidof systemd) -a su - $LOGNAME
``` 

- Install MicroK8s:

```
microk8s status
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
# after commands, logout
exit
# if necessary, on the other powershell terminal, run
wsl -l -v   # list all wsls
wsl --shutdown  # to shutdown all wsl
# run again Ubuntu 20.04
```

- Install MicroK8s Plugins:

```
microk8s enable dns storage ingress metallb:10.64.140.43-10.64.140.49
# wait 3-4 mins
microk8s status --wait-ready
```

- Install Juju:

```
sudo snap install juju --classic
```

- Juju bootstrap existed K8s cluster, add-model and deploy:

```
juju bootstrap microk8s
juju add-model kubeflow
juju deploy kubeflow-lite --trust
```

- It will take time (20mins-45mins):

```
# monitoring the creating of the apps / containers
juju status --color
```

![image](https://user-images.githubusercontent.com/10358317/206735424-24995cdf-8e21-4020-9547-6675ad92ca76.png)

```
# monitoring the pods
microk8s kubectl get pods --all-namespaces
```

![image](https://user-images.githubusercontent.com/10358317/206735586-44c64733-f4cb-43a6-b716-01ca7429a819.png)

```
# monitoring K8s services
microk8s kubectl get svc -n kubeflow
```

![image](https://user-images.githubusercontent.com/10358317/206735752-5423629b-628f-4ae1-bae0-c4cff9c6ef67.png)

```
# monitoring K8s all objects: services, pods, deployment, statefulset, daemonsets.
microk8s kubectl get all --all-namespaces
```

- After everything runs in normal (juju status --color), it is required to configure ingress to reach using browser

```
juju config dex-auth public-url=http://10.64.140.43.nip.io
juju config oidc-gatekeeper public-url=http://10.64.140.43.nip.io

juju config dex-auth static-username=admin
juju config dex-auth static-password=admin
```

- Install Ubuntu-Desktop, XRDP

```
sudo apt update
sudo apt install ubuntu-desktop xrdp
sudo apt install net-tools
ifconfig # to get IP of WSL Ubuntu
# use RDP (remote desktop application) to reach desktop
```

- Go to browser:
```
http://10.64.140.43.nip.io
```

- If it does not work:
```
microk8s kubectl get gateway -A
#If the response is No resources found you can force the charm to create it the following way:
juju run --unit istio-pilot/0 -- "export JUJU_DISPATCH_PATH=hooks/config-changed; ./dispatch"
```

![image](https://user-images.githubusercontent.com/10358317/206737626-25a90c69-e59c-4028-9bac-91fb1e24d565.png)

![image](https://user-images.githubusercontent.com/10358317/206737813-0d8b1c5f-a665-4bbd-bfb0-68fd39c0cd27.png)


### Minio

- Minio is a object storage to store data (pipeline, output data, etc.)
- To see Minio console in browser:
```
microk8s kubectl get svc -n kubeflow | grep minio
microk8s kubectl port-forward svc/minio -n kubeflow 8081:9001 --address=0.0.0.0
http://localhost:8081/login
```

- To get Minio username and password:
```
microk8s kubectl get secrets -n kubeflow | grep minio
microk8s kubectl get secret minio-secret -n kubeflow -o yaml
```

```
data:
  MINIO_ACCESS_KEY: bWluaW8=
  MINIO_SECRET_KEY: UUhWTjJRVU5CNTlEMVVaTlpYVDVQWUczOVVRRjBN
```

```
echo bWluaW8= | base64 --decode
minio  # username

echo UUhWTjJRVU5CNTlEMVVaTlpYVDVQWUczOVVRRjBN | base64 --decode
QHVN2QUNB59D1UZNZXT5PYG39UQF0M  # password
```

![image](https://user-images.githubusercontent.com/10358317/206738886-dac004c0-d7d0-4962-8912-0f1dfa6c55e8.png)

![image](https://user-images.githubusercontent.com/10358317/206738980-e33100c4-b219-4172-9037-4c886d70db23.png)


### Troubleshoot

- If one of the pod has always error,  delete it, k8s automatically creates it:

```
microk8s kubectl delete pod dex-auth-0 -n kubeflow
```

- If there is still problem, shutdown WSL2 and restart WSL2.

### Restarting WSL2, Kubeflow

``` 
sudo apt-get update && sudo apt-get install -yqq daemonize dbus-user-session fontconfig
sudo daemonize /usr/bin/unshare --fork --pid --mount-proc /lib/systemd/systemd --system-unit=basic.target 
exec sudo nsenter -t $(pidof systemd) -a su - $LOGNAME

microk8s status --wait-ready
juju status --color
response: ERROR cannot connect to k8s api server; try running 'juju update-k8s --client <k8s cloud name>'
juju clouds
juju update-k8s --client microk8s

``` 
- Monitor until all apps running correctly (all active)

``` 
juju status --color
microk8s kubectl get pods --all-namespaces
``` 

### References
- Juju, MicroK8s, Kubeflow: https://charmed-kubeflow.io/docs/quickstart?_ga=2.224818008.37303802.1670432683-702060604.1670151120#heading--install-juju
