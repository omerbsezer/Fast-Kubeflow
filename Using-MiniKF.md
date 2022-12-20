## LAB: Creating LAB Environment, MiniKF with Vagrant

This lab shows:
- how to install and use MiniKF
- how to solve problems while installing MiniKF

### Kubeflow

#### What is MiniKF?
- MiniKF is a virtual machine that is created by Arrikto. 
- MiniKF = Minikube + Kubeflow + ROK (Rok: Data Management Platform on Kubernetes, developed by Arrikto)

#### Why should we use MiniKF?
- It is free and easy to use quickly for learning and developing Kubeflow pipelines in a one-virtual-machine. 

#### How do we install MiniKF?

- Install Virtualbox 6.1.40 (stable with Vagrant and MiniKF)=> https://download.virtualbox.org/virtualbox/6.1.40/

- Install Vagrant => https://developer.hashicorp.com/vagrant/docs/installation

- What is Vagrant? 
  - Vagrant is the command line utility for managing the lifecycle of virtual machines.
  
- On the powershell:

``` 
vagrant init arrikto/minikf
vagrant up
``` 

  ![image](https://user-images.githubusercontent.com/10358317/208669384-edfea023-ba37-4b05-8e2b-76fbd69b108b.png)


- On browser, open http://10.10.10.10/

  ![image](https://user-images.githubusercontent.com/10358317/208669490-a46d7635-547c-4f4b-97ee-a8bab0fc172b.png)
  
  ![image](https://user-images.githubusercontent.com/10358317/208669765-79a05bce-5bdf-42dd-af87-de7e45b0c0df.png)
  
  ![image](https://user-images.githubusercontent.com/10358317/208669809-f194eea6-3ddb-4176-922f-da689d50147f.png)

- With Kubectl on the host PC, we can see the running Kubernetes Objects 

  ![image](https://user-images.githubusercontent.com/10358317/208669969-fe96554c-5533-4de2-993e-1b2162384c2c.png)

- Run commands on the powershell on the host PC:

``` 
kubectl -n kubeflow get pods
``` 

  ![image](https://user-images.githubusercontent.com/10358317/208670491-aeb9f5ae-8fd9-4e26-8e32-e45d4fdcc344.png)

- Connect to the Kubeflow

  ![image](https://user-images.githubusercontent.com/10358317/208674906-221c1675-e9d7-4fc9-91f6-81d0ab23c3d0.png)

### Troubleshooting

#### One of the pod is not ready (34/35 remaining)

  ![image](https://user-images.githubusercontent.com/10358317/208670873-eca5f940-db9b-40fe-83b0-01415327e0d9.png)

  ![image](https://user-images.githubusercontent.com/10358317/208670947-1ba7e918-1e2a-48a7-a079-0700360c2b4d.png)

- Delete the pod that is 'CrashLoopBackOff', deleted service is restarted automatically.

```
kubectl delete pod notebook-controller-deployment-7c46fdd957-87zfw -n kubeflow
```

  ![image](https://user-images.githubusercontent.com/10358317/208671362-80ccc638-402a-4d1c-afd6-cd3960215c61.png)

- Connect MiniKF with clicking button

  ![image](https://user-images.githubusercontent.com/10358317/208675116-a686a234-c9d1-4b38-bdef-302edf857bf6.png)


#### Can't connect to MiniKF landing page on http://10.10.10.10 after installing MiniKF

- According to this post: https://stackoverflow.com/questions/60820998/cant-connect-to-minikf-landing-page-on-http-10-10-10-10-after-installing-mini

- Stop VM using VirtualBox GUI and run 'vagrant up' again, then http://10.10.10.10

#### Increasing 'config.vm.boot_timeout' 

- According to this post: https://stackoverflow.com/questions/32731629/where-to-find-config-vm-boot-timeout

- Go to this file (VagrantFile), if your installation is default path: C:\HashiCorp\Vagrant\embedded\gems\2.3.4\gems\vagrant-2.3.4\Vagrantfile
- In the root directory of your Vagrant install, there's the Vagrantfile file. There, I added config.vm.boot_timeout = 600 just after Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|.

```
config.vm.boot_timeout = 600
```
