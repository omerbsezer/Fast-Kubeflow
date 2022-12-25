## LAB / PROJECT: Kubeflow Pipeline (From Scratch) with Custom Docker Images (Decision Tree, Logistic Regression, SVM, Naive Bayes, Xg Boost)

This lab/project shows:
- how to create Kubeflow Pipeline with Custom Docker Images 
- all files: https://github.com/omerbsezer/Fast-Kubeflow/tree/main/Project_Kubeflow_Pipeline_MLModels 

### Table of Contents
- [Download Data Component](#download_data)
- [Decision Tree Component](#decision_tree)
- [Logistic Regression Component](#logistic_regression)
- [SVM Component](#svm)
- [Naive Bayes Component](#naive_bayes)
- [Xg Boost Component](#xg_boost)
- [Show Results Component](#show_results)
- [Compiling, Uploading Pipeline into Kubeflow and Running](#compile_run)    

### Prerequisite

- You should have Kubeflow Environment (Easiest Way: Using MiniKF)
  - [LAB: Creating LAB Environment, Installing MiniKF with Vagrant](https://github.com/omerbsezer/Fast-Kubeflow/blob/main/Using-MiniKF.md)
  
**Steps:**
- Create Python codes and Pipeline Components (Docker Images) for each steps:
  - download_data.py and Dowload Data Component (Yaml file and docker image with dockerfile that includes dowload_data.py)
  - decision_tree.py and Decision Tree Component (Yaml file and docker image with dockerfile that includes decision_tree.py)
  - logistic_regression.py and Logistic Regression Component (Yaml file and docker image with dockerfile that includes logistic_regression.py)
  - svm.py and SVM Component (Yaml file and docker image with dockerfile that includes svm.py)
  - naive_bayes.py and Naive Bayes Component (Yaml file and docker image with dockerfile that includes naive_bayes.py)
  - xg_boost.py and XG Boost Component (Yaml file and docker image with dockerfile that includes xg_boost.py)
  - Show Results Component
  
### Steps

#### Download Data Component  <a name="download_data"></a>

- Dataset:
  - https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html
  - https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)  

- Creating download_data.py:
``` 
import json

import argparse
from pathlib import Path

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

def _download_data(args):

    # Gets data from sklearn library and split dataset
    x, y = load_breast_cancer(return_X_y=True)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    # Creates `data` structure to save 
    data = {'x_train' : x_train.tolist(),
            'y_train' : y_train.tolist(),
            'x_test' : x_test.tolist(),
            'y_test' : y_test.tolist()}

    # Creates a json object based on `data`
    data_json = json.dumps(data)

    # Saves the json object into a file
    with open(args.data, 'w') as output_file:
        json.dump(data_json, output_file)

if __name__ == '__main__':
    
    # This component does not receive any input, it only outputs one artifact which is `data`.
    parser = argparse.ArgumentParser()
    # Output argument: data
    parser.add_argument('--data', type=str)
    
    args = parser.parse_args()
    
    # Creating the directory where the OUTPUT file will be created, (the directory may or may not exist).
    # This will be used for other component's input (e.g. decision tree, logistic regression)
    Path(args.data).parent.mkdir(parents=True, exist_ok=True)

    _download_data(args)
``` 

- Create download data component (download_data.yaml)
```
name: Download Data Function
description: Download toy data from sklearn datasets

outputs:
- {name: Data, type: LocalPath, description: 'Path where data will be stored.'}

implementation:
  container:
    image: omerbsezer/kubeflow_component:download_breast_cancer_data_v1
    command: [
      python, download_data.py,

      --data,
      {outputPath: Data},
    ]
```

- Create requirements.txt:
``` 
scikit-learn
``` 

- Dockerfile:
``` 
FROM python:3.8-slim
WORKDIR /pipeline
COPY requirements.txt /pipeline
RUN pip install -r requirements.txt
COPY download_data.py /pipeline
``` 

- Go to the path where dockerfile is, then build Dockerfile and push the image to the Docker Registry:
``` 
docker image build -t omerbsezer/kubeflow_component:download_breast_cancer_data_v1 .
docker push omerbsezer/kubeflow_component:download_breast_cancer_data_v1
```

  ![image](https://user-images.githubusercontent.com/10358317/209472960-8d1c4031-22f3-41b5-a7e5-e69a30e6262a.png)


#### Decision Tree Component <a name="decision_tree"></a>

- Creating decision_tree.py:
``` 
import json

import argparse
from pathlib import Path

from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

def _decision_tree(args):

    # Open and reads file "data"
    with open(args.data) as data_file:
        data = json.load(data_file)
    
    # Data type is 'dict', however since the file was loaded as a json object, it is first loaded as a string
    # thus we need to load again from such string in order to get the dict-type object.
    data = json.loads(data)

    x_train = data['x_train']
    y_train = data['y_train']
    x_test = data['x_test']
    y_test = data['y_test']
    
    # Initialize and train the model
    model = DecisionTreeClassifier(max_depth=4)
    model.fit(x_train, y_train)

    # Get predictions
    y_pred = model.predict(x_test)
    
    # Get accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Save output into file
    with open(args.accuracy, 'w') as accuracy_file:
        accuracy_file.write(str(accuracy))

if __name__ == '__main__':

    # Defining and parsing the command-line arguments
    parser = argparse.ArgumentParser(description='My program description')
    # Input argument: data
    parser.add_argument('--data', type=str)
    # Output argument: accuracy
    parser.add_argument('--accuracy', type=str)

    args = parser.parse_args()

    # Creating the directory where the OUTPUT file will be created (the directory may or may not exist).
    Path(args.accuracy).parent.mkdir(parents=True, exist_ok=True)
    
    _decision_tree(args)
``` 

- Create decision tree component (decision_tree.yaml)
```
name: Decision Tree classifier
description: Trains a  decision tree classifier

inputs:
- {name: Data, type: LocalPath, description: 'Path where data is stored.'}
outputs:
- {name: Accuracy, type: Float, description: 'Accuracy metric'}

implementation:
  container:
    image: omerbsezer/kubeflow_component:decision_tree_v1
    command: [
      python, decision_tree.py,

      --data,
      {inputPath: Data},

      --accuracy,
      {outputPath: Accuracy},

    ]
```

- Create requirements.txt:
``` 
scikit-learn
``` 

- Dockerfile:
``` 
FROM python:3.8-slim
WORKDIR /pipelines
COPY requirements.txt /pipelines
RUN pip install -r requirements.txt
COPY decision_tree.py /pipelines
``` 

- Go to the path where dockerfile is, then build Dockerfile and push the image to the Docker Registry:
``` 
docker image build -t omerbsezer/kubeflow_component:decision_tree_v1 .
docker push omerbsezer/kubeflow_component:decision_tree_v1
```

#### Logistic Regression Component <a name="logistic_regression"></a>

- Creating logistic_regression.py:
``` 
import json

import argparse
from pathlib import Path

from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

def _logistic_regression(args):

    # Open and reads file "data"
    with open(args.data) as data_file:
        data = json.load(data_file)
    
    # Data type is 'dict', however since the file was loaded as a json object, it is first loaded as a string
    # thus we need to load again from such string in order to get the dict-type object.
    data = json.loads(data)

    x_train = data['x_train']
    y_train = data['y_train']
    x_test = data['x_test']
    y_test = data['y_test']
    
    # Initialize and train the model
    model = LogisticRegression()
    model.fit(x_train, y_train)

    # Get predictions
    y_pred = model.predict(x_test)
    
    # Get accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Save output into file
    with open(args.accuracy, 'w') as accuracy_file:
        accuracy_file.write(str(accuracy))

if __name__ == '__main__':

    # Defining and parsing the command-line arguments
    parser = argparse.ArgumentParser(description='My program description')
    # Input argument: data
    parser.add_argument('--data', type=str)
    # Output argument: accuracy
    parser.add_argument('--accuracy', type=str)

    args = parser.parse_args()

    # Creating the directory where the output file will be created (the directory may or may not exist).
    Path(args.accuracy).parent.mkdir(parents=True, exist_ok=True)
    
    _logistic_regression(args)
``` 

- Create logistic regression component (logistic_regression.yaml)
```
name: Logistic Regression Classifier
description: Trains a Logistic Regression Classifier

inputs:
- {name: Data, type: LocalPath, description: 'Path where data is stored.'}
outputs:
- {name: Accuracy, type: Float, description: 'Accuracy metric'}

implementation:
  container:
    image: omerbsezer/kubeflow_component:logistic_regression_v1
    command: [
      python, logistic_regression.py,

      --data,
      {inputPath: Data},

      --accuracy,
      {outputPath: Accuracy},

    ]
```

- Create requirements.txt:
``` 
scikit-learn
``` 

- Dockerfile:
``` 
FROM python:3.8-slim
WORKDIR /pipelines
COPY requirements.txt /pipelines
RUN pip install -r requirements.txt
COPY logistic_regression.py /pipelines
``` 

- Go to the path where dockerfile is, then build Dockerfile and push the image to the Docker Registry:
``` 
docker image build -t omerbsezer/kubeflow_component:logistic_regression_v1 .
docker push omerbsezer/kubeflow_component:logistic_regression_v1
```
#### SVM Component <a name="svm"></a>

- Creating svm.py:
``` 
import json

import argparse
from pathlib import Path

from sklearn.metrics import accuracy_score
from sklearn.svm import SVC

def _svm(args):

    # Open and reads file "data"
    with open(args.data) as data_file:
        data = json.load(data_file)
    
    # Data type is 'dict', however since the file was loaded as a json object, it is first loaded as a string
    # thus we need to load again from such string in order to get the dict-type object.
    data = json.loads(data)

    x_train = data['x_train']
    y_train = data['y_train']
    x_test = data['x_test']
    y_test = data['y_test']
    
    # Initialize and train the model
    model = SVC(kernel='linear')
    model.fit(x_train, y_train)

    # Get predictions
    y_pred = model.predict(x_test)
    
    # Get accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Save output into file
    with open(args.accuracy, 'w') as accuracy_file:
        accuracy_file.write(str(accuracy))

if __name__ == '__main__':

    # Defining and parsing the command-line arguments
    parser = argparse.ArgumentParser(description='My program description')
    # Input argument: data
    parser.add_argument('--data', type=str)
    # Output argument: accuracy
    parser.add_argument('--accuracy', type=str)

    args = parser.parse_args()

    # Creating the directory where the OUTPUT file will be created (the directory may or may not exist).
    Path(args.accuracy).parent.mkdir(parents=True, exist_ok=True)
    
    _svm(args)
``` 

- Create SVM component (svm.yaml)
```
name: Support Vector (svm) classifier
description: Trains a svm classifier

inputs:
- {name: Data, type: LocalPath, description: 'Path where data is stored.'}
outputs:
- {name: Accuracy, type: Float, description: 'Accuracy metric'}

implementation:
  container:
    image: omerbsezer/kubeflow_component:svm_v1
    command: [
      python, svm.py,

      --data,
      {inputPath: Data},

      --accuracy,
      {outputPath: Accuracy},

    ]
```

- Create requirements.txt:
``` 
scikit-learn
``` 

- Dockerfile:
``` 
FROM python:3.8-slim
WORKDIR /pipelines
COPY requirements.txt /pipelines
RUN pip install -r requirements.txt
COPY svm.py /pipelines
``` 

- Go to the path where dockerfile is, then build Dockerfile and push the image to the Docker Registry:
``` 
docker image build -t omerbsezer/kubeflow_component:svm_v1 .
docker push omerbsezer/kubeflow_component:svm_v1
```

#### Naive Bayes Component <a name="naive_bayes"></a>

- Creating naive_bayes.py:
``` 
import json

import argparse
from pathlib import Path

from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB

def _naive_bayes(args):

    # Open and reads file "data"
    with open(args.data) as data_file:
        data = json.load(data_file)
    
    # Data type is 'dict', however since the file was loaded as a json object, it is first loaded as a string
    # thus we need to load again from such string in order to get the dict-type object.
    data = json.loads(data)

    x_train = data['x_train']
    y_train = data['y_train']
    x_test = data['x_test']
    y_test = data['y_test']
    
    # Initialize and train the model
    model = GaussianNB()
    model.fit(x_train, y_train)

    # Get predictions
    y_pred = model.predict(x_test)
    
    # Get accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Save output into file
    with open(args.accuracy, 'w') as accuracy_file:
        accuracy_file.write(str(accuracy))

if __name__ == '__main__':

    # Defining and parsing the command-line arguments
    parser = argparse.ArgumentParser(description='My program description')
    # Input argument: data
    parser.add_argument('--data', type=str)
    # Output argument: accuracy
    parser.add_argument('--accuracy', type=str)

    args = parser.parse_args()

    # Creating the directory where the OUTPUT file will be created (the directory may or may not exist).
    Path(args.accuracy).parent.mkdir(parents=True, exist_ok=True)
    
    _naive_bayes(args)
``` 

- Create naive bayes component (naive_bayes.yaml)
```
name: Naive Bayes classifier
description: Trains a Naive Bayes classifier

inputs:
- {name: Data, type: LocalPath, description: 'Path where data is stored.'}
outputs:
- {name: Accuracy, type: Float, description: 'Accuracy metric'}

implementation:
  container:
    image: omerbsezer/kubeflow_component:naive_bayes_v1
    command: [
      python, naive_bayes.py,

      --data,
      {inputPath: Data},

      --accuracy,
      {outputPath: Accuracy},

    ]
```

- Create requirements.txt:
``` 
scikit-learn
``` 

- Dockerfile:
``` 
FROM python:3.8-slim
WORKDIR /pipelines
COPY requirements.txt /pipelines
RUN pip install -r requirements.txt
COPY naive_bayes.py /pipelines
``` 

- Go to the path where dockerfile is, then build Dockerfile and push the image to the Docker Registry:
``` 
docker image build -t omerbsezer/kubeflow_component:naive_bayes_v1 .
docker push omerbsezer/kubeflow_component:naive_bayes_v1
```

#### XG Boost Component <a name="xg_boost"></a>

- Creating xg_boost.py:
``` 
import json

import argparse
from pathlib import Path

from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

def _xg_boost(args):

    # Open and reads file "data"
    with open(args.data) as data_file:
        data = json.load(data_file)
    
    # Data type is 'dict', however since the file was loaded as a json object, it is first loaded as a string
    # thus we need to load again from such string in order to get the dict-type object.
    data = json.loads(data)

    x_train = data['x_train']
    y_train = data['y_train']
    x_test = data['x_test']
    y_test = data['y_test']
    
    # Initialize and train the model
    model = XGBClassifier()
    model.fit(x_train, y_train)

    # Get predictions
    y_pred = model.predict(x_test)
    
    # Get accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Save output into file
    with open(args.accuracy, 'w') as accuracy_file:
        accuracy_file.write(str(accuracy))

if __name__ == '__main__':

    # Defining and parsing the command-line arguments
    parser = argparse.ArgumentParser(description='My program description')
    # Input argument: data
    parser.add_argument('--data', type=str)
    # Output argument: accuracy
    parser.add_argument('--accuracy', type=str)

    args = parser.parse_args()

    # Creating the directory where the OUTPUT file will be created (the directory may or may not exist).
    Path(args.accuracy).parent.mkdir(parents=True, exist_ok=True)
    
    _xg_boost(args)
``` 

- Create XgBoost component (xg_boost.yaml)
```
name: Xg Boost classifier
description: Trains an xg boost classifier

inputs:
- {name: Data, type: LocalPath, description: 'Path where data is stored.'}
outputs:
- {name: Accuracy, type: Float, description: 'Accuracy metric'}

implementation:
  container:
    image: omerbsezer/kubeflow_component:xg_boost_v1
    command: [
      python, xg_boost.py,

      --data,
      {inputPath: Data},

      --accuracy,
      {outputPath: Accuracy},

    ]
```

- Create requirements.txt:
``` 
scikit-learn
xgboost
``` 

- Dockerfile:
``` 
FROM python:3.8-slim
WORKDIR /pipelines
COPY requirements.txt /pipelines
RUN pip install -r requirements.txt
COPY xg_boost.py /pipelines
``` 

- Go to the path where dockerfile is, then build Dockerfile and push the image to the Docker Registry:
``` 
docker image build -t omerbsezer/kubeflow_component:xg_boost_v1 .
docker push omerbsezer/kubeflow_component:xg_boost_v1
```

#### Show Results Component <a name="show_results"></a>


- This component contains following function. It does not needed seperate docker image file. 
``` 
@func_to_container_op
def show_results(decision_tree : float, logistic_regression : float, svm : float, naive_bayes : float, xg_boost : float) -> None:
    # Given the outputs from decision_tree, logistic regression, svm, naive_bayes, xg_boost components

    print(f"Decision tree (accuracy): {decision_tree}")
    print(f"Logistic regression (accuracy): {logistic_regression}")
    print(f"SVM (SVC) (accuracy): {svm}")
    print(f"Naive Bayes (Gaussian) (accuracy): {naive_bayes}")
    print(f"XG Boost (accuracy): {xg_boost}")
``` 


### Compiling, Uploading Pipeline into Kubeflow and Running <a name="compile_run"></a> 

- Install kfp package

``` 
pip install kfp
```

- Create pipeline.py
``` 
import kfp
from kfp import dsl
from kfp.components import func_to_container_op

@func_to_container_op
def show_results(decision_tree : float, logistic_regression : float, svm : float, naive_bayes : float, xg_boost : float) -> None:
    # Given the outputs from decision_tree, logistic regression, svm, naive_bayes, xg_boost components

    print(f"Decision tree (accuracy): {decision_tree}")
    print(f"Logistic regression (accuracy): {logistic_regression}")
    print(f"SVM (SVC) (accuracy): {svm}")
    print(f"Naive Bayes (Gaussian) (accuracy): {naive_bayes}")
    print(f"XG Boost (accuracy): {xg_boost}")

@dsl.pipeline(name='ML Models Pipeline', description='Applies Decision Tree, Logistic Regression, SVM, Naive Bayes, XG Boost for classification problem.')
def ml_models_pipeline():

    # Loads the yaml manifest for each component
    download = kfp.components.load_component_from_file('download_data/download_data.yaml')
    decision_tree = kfp.components.load_component_from_file('decision_tree/decision_tree.yaml')
    logistic_regression = kfp.components.load_component_from_file('logistic_regression/logistic_regression.yaml')
    svm = kfp.components.load_component_from_file('svm/svm.yaml')
    naive_bayes = kfp.components.load_component_from_file('naive_bayes/naive_bayes.yaml')
    xg_boost = kfp.components.load_component_from_file('xg_boost/xg_boost.yaml')

    # Run download_data task
    download_task = download()

    # Run ML models tasks with input data
    decision_tree_task = decision_tree(download_task.output)
    logistic_regression_task = logistic_regression(download_task.output)
    svm_task = svm(download_task.output)
    naive_bayes_task = naive_bayes(download_task.output)
    xg_boost_task = xg_boost(download_task.output)

    # Given the outputs from ML models tasks
    # the component "show_results" is called to print the results.
    show_results(decision_tree_task.output, logistic_regression_task.output, svm_task.output, naive_bayes_task.output, xg_boost_task.output)

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(ml_models_pipeline, 'MLModelsPipeline.yaml')
``` 

- Run pipeline (DSL Compile) to create Workflow Pipeline (Argoflow). After creating pipeline, it creates 'MLModelsPipeline.yaml'.
``` 
python pipeline.py
``` 

- Import Kubeflow created 'MLModelsPipeline.yaml':

  ![image](https://user-images.githubusercontent.com/10358317/209474987-491cc641-2dcf-4623-8559-8e24e569885e.png)

- Create an experiment:
  
  ![image](https://user-images.githubusercontent.com/10358317/209475006-08d4e3a0-2fd3-4ae6-b87f-1290b828ef79.png)

- Create a run:

  ![image](https://user-images.githubusercontent.com/10358317/209475058-42ddccdd-18a4-4d93-af10-48b36113a27b.png)

- Kubeflow creates pipeline and runs it: 
  
  ![image](https://user-images.githubusercontent.com/10358317/209475074-ee5f96d5-98a3-4e53-8f0a-2a37b8931b23.png)

- With 'kubectl get pods -n kubeflow-user', we can follow the status of the running pods in the K8s cluster (in our scenario, in MiniKF)

  ![image](https://user-images.githubusercontent.com/10358317/209475100-c50f9c87-383b-4293-b00a-0c3ae886d02a.png)
  
- When clicking on the each step, it can be seen the details

  ![image](https://user-images.githubusercontent.com/10358317/209475176-7f581ddb-c618-4815-bb5d-02c879fcbf22.png)

- When clicking on the last step:

  ![image](https://user-images.githubusercontent.com/10358317/209475212-0bb679b3-eedc-4bcc-823a-7c92bd098a77.png)
  
- We run multiple models in parallel, XGBoost and Decision Tree have best accuracy results:

  ![image](https://user-images.githubusercontent.com/10358317/209475281-4c33cff6-c056-4ee9-8c39-c5760dcfb4c6.png)


### References
- https://towardsdatascience.com/kubeflow-pipelines-how-to-build-your-first-kubeflow-pipeline-from-scratch-2424227f7e5
