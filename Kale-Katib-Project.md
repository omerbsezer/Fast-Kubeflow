## LAB / PROJECT: KALE 

This lab/project shows:
- how to run Kale


### Steps

- Create a new notebook server pod and connect:

  ![image](https://user-images.githubusercontent.com/10358317/209570057-a90362d4-b554-45c2-ad9c-d7a80e46cc82.png)

- Run Terminal to download examples:
  
  ![image](https://user-images.githubusercontent.com/10358317/209569680-9e5db88e-4349-4049-ad2b-e78b532cb073.png)

- Clone Kale Examples:
 
``` 
git clone https://github.com/kubeflow-kale/kale
``` 

- Open the ipynb file (open-vaccine.ipynb)
- Run the cell "pip install -r requirements.txt" to install requirements

  ![image](https://user-images.githubusercontent.com/10358317/209570256-2adda5b9-4694-4230-bded-25041171f367.png)

- Then, after installing required packages, restart the kernel.

  ![image](https://user-images.githubusercontent.com/10358317/209570566-498650c3-3a0c-4c74-82d2-9beecbe533df.png)

- Open the KALE section from left and enable KALE

  ![image](https://user-images.githubusercontent.com/10358317/209570645-a1e44bf4-e10a-4846-88c5-bbf9330d1ff3.png)
  
- After opening KALE feature, it is seen that each cells are tagged with steps (e.g. imports, pipeline-parameters, etc.)   
  
  ![image](https://user-images.githubusercontent.com/10358317/209570786-e88cb620-74b6-4284-bfb9-43f385c48cdc.png)
  
- At the end of the notebook, add new cell with "print(validation_loss)" and change the tag (cell-type) "Pipeline Metrics"

  ![image](https://user-images.githubusercontent.com/10358317/209571039-83f08b7c-2cf2-4c7a-b3c9-2327b5a7e22f.png)
 
- Enable KATIB:
 
  ![image](https://user-images.githubusercontent.com/10358317/209571140-047d3b27-51b4-4e6f-8f7a-13f8b98850ca.png)
  
- After opening KATIB setting parameters: 

  ![image](https://user-images.githubusercontent.com/10358317/209571226-511b9df1-877c-4b9c-86a0-8723f396f320.png)
 
  ![image](https://user-images.githubusercontent.com/10358317/209571315-d8f82bbd-d820-400d-92cc-5d971198843f.png)

- Run "Compile and Run KATIB Job", this will run KALE and KATIB:

  ![image](https://user-images.githubusercontent.com/10358317/209571431-dde222f6-2e1e-4e42-98e2-bfed24d580cf.png)

- After running, click "View" button:

  ![image](https://user-images.githubusercontent.com/10358317/209571735-9b522220-3dfa-4187-927f-5442a2c9e67a.png)
  
- We can see the hyperparameter and trials:
 
  ![image](https://user-images.githubusercontent.com/10358317/209571847-1da5a75c-a7f4-428e-af1c-4dd14867e729.png)
  
  
- After waiting some time to finish all trials to find best hyperparameters:

  ![image](https://user-images.githubusercontent.com/10358317/209573641-b20c09b2-3f37-4cd3-a930-c0cce45a00e4.png)
  
  ![image](https://user-images.githubusercontent.com/10358317/209573771-52842638-6ba2-4d65-8b29-3b232ee7f365.png)

- In the "Run" section, it can be seen that pipeline is completed and details can be reachable clicking on the each block step:

  ![image](https://user-images.githubusercontent.com/10358317/209573921-57ff4731-4a5d-4ae8-8e93-e5093daee365.png)



  
