## LAB / PROJECT: KALE (Kubeflow Automated PipeLines Engine) and KServe

This lab/project shows:
- how to use KALE and KServe in a project.

### Prerequisite

- You should have Kubeflow Environment (Easiest Way: Using MiniKF)
  - [LAB: Creating LAB Environment, Installing MiniKF with Vagrant](https://github.com/omerbsezer/Fast-Kubeflow/blob/main/Using-MiniKF.md)
  
### Steps

- Create a new notebook server pod and connect:

  ![image](https://user-images.githubusercontent.com/10358317/209570057-a90362d4-b554-45c2-ad9c-d7a80e46cc82.png)

- Run Terminal to download examples:
  
  ![image](https://user-images.githubusercontent.com/10358317/209569680-9e5db88e-4349-4049-ad2b-e78b532cb073.png)

- Clone Kale Examples:
 
``` 
git clone https://github.com/kubeflow-kale/kale
``` 

- Open the ipynb file (kale/examples/serving/sklearn/iris.ipynb)

  ![image](https://user-images.githubusercontent.com/10358317/209675801-d006fb7a-9916-4054-8b0e-e74048200c6f.png)

- Run the cell "pip install -r requirements.txt" to install requirements
- Then, after installing required packages, restart the kernel.

  ![image](https://user-images.githubusercontent.com/10358317/209676318-60839c0e-9711-4add-8c3f-8642f76300a5.png)
  
- Open the KALE section from left and enable KALE

  ![image](https://user-images.githubusercontent.com/10358317/209570645-a1e44bf4-e10a-4846-88c5-bbf9330d1ff3.png)
  
- After opening KALE feature, it is seen that each cells are tagged with steps (e.g. imports, pipeline-parameters, etc.) 
- Use "gcr.io/arrikto/jupyter-kale-py36:develop-l0-release-1.2-pre-295-g622fe91aca" as docker image if you encounter with another image. 
  
  ![image](https://user-images.githubusercontent.com/10358317/209676588-5ea8b39b-3dbe-446f-be28-351daea14142.png)
  
- Before compiling, add tagging to "serving_model", this enables to create model in Kubeflow. 

  ![image](https://user-images.githubusercontent.com/10358317/209677273-10fa21c2-5589-45b3-9002-a967e0818416.png)
  
 - Run "Compile and Run" to create Kubeflow pipeline from the notebook (this is KALE feature)
 - It creates pipeline: 

  ![image](https://user-images.githubusercontent.com/10358317/209677781-ddae3901-8253-41a8-aa98-3c7aaac12c2b.png)
  
- When monitoring pods in K8s, it can be seen that pods are running and completed for each step.

  ![image](https://user-images.githubusercontent.com/10358317/209712597-54ac29eb-5855-41f8-b29f-6e8a6c71b729.png)

- For each task details can be viewed.
  
  ![image](https://user-images.githubusercontent.com/10358317/209713088-85cb2bda-047b-496a-8242-a8a5e84e7ebb.png)
  
- For each step logs and data are stored in ROK and Minio (if MiniKF is used).

  ![image](https://user-images.githubusercontent.com/10358317/209713199-6c1504dc-8d5a-4f0f-90f9-5f2591950203.png)

- After running pipeline, it can be seen the result parameters (accuracy)

  ![image](https://user-images.githubusercontent.com/10358317/209677953-75456ff8-eb11-40bf-9df8-42a019b93b96.png)

- KServe creates model:

  ![image](https://user-images.githubusercontent.com/10358317/209678023-abcff783-49af-47dc-b9f7-0b944dcd6097.png)
  
- From model section, detail information can be reachable:

  ![image](https://user-images.githubusercontent.com/10358317/209715143-3c7ee97f-8138-473d-867f-69dffcb7e981.png)

  ![image](https://user-images.githubusercontent.com/10358317/209715204-a20f8675-ec7f-4dc9-9a61-82b82d96d618.png)

  ![image](https://user-images.githubusercontent.com/10358317/209715268-12d341ef-51e9-40a9-be8e-bae3efa86284.png)

  ![image](https://user-images.githubusercontent.com/10358317/209715310-02b8d854-e878-4a9f-a6e9-8a427829d518.png)
  
- Open launcher:

  ![image](https://user-images.githubusercontent.com/10358317/209678243-353b7271-7241-4899-bcd3-c3c58ee5de53.png)
  
- Run Terminal:
  
  ![image](https://user-images.githubusercontent.com/10358317/209569680-9e5db88e-4349-4049-ad2b-e78b532cb073.png)
  
- Run following commands to create JSON file to send the model.
 
``` 
cat <<EOF > "./iris-input.json"
{
  "instances": [
    [6.8,  2.8,  4.8,  1.4],
    [6.0,  3.4,  4.5,  1.6]
  ]
}
EOF
``` 

- Run curl command to send JSON file to the model.
- This "http://iris-pipeline-xchh4-3630146895-2r0st.kubeflow-user.svc.cluster.local/v1/models/iris-pipeline-xchh4-3630146895-2r0st:predict" is written in the model URL internal, please have a look in the model to get correct path.

``` 
curl -v http://iris-pipeline-xchh4-3630146895-2r0st.kubeflow-user.svc.cluster.local/v1/models/iris-pipeline-xchh4-3630146895-2r0st:predict -d @./iris-input.json
``` 

- After sending file with curl command, the prediction is responded, this shows that KServe serve the model:

  ![image](https://user-images.githubusercontent.com/10358317/209678618-bdca8552-571c-4844-a16a-290ffd694fd5.png)

- For different training run, reaching served model:
  
  ![image](https://user-images.githubusercontent.com/10358317/209715713-91d356a8-8d85-4d87-bed9-339a7b72cb2a.png)
