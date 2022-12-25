## LAB / PROJECT: Kubeflow Pipeline (From Scratch) with Custom Docker Images (Decision Tree, Logistic Regression)

This lab/project shows:
- how to create Kubeflow Pipeline with Custom Docker Images

**Steps:**
- Create Python codes and Pipeline Components (Docker Images) for each steps:
  - Download_data.py and Dowload Data Component (Yaml file and docker image with dockerfile that includes dowload_data.py)
  - Decision_tree.py and Decision Tree Component (Yaml file and docker image with dockerfile that includes decision_tree.py)
  - Logistic_regression.py and Logistic Regression Component (Yaml file and docker image with dockerfile that includes logistic_regression.py)
  - Show Results Component
  
### Steps

#### Download Data Component

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


#### Decision Tree Component

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

#### Logistic Regression Component

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
#### SVM Component

- Creating svm.py:
``` 

``` 

- Create SVM component (svm.yaml)
```

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

#### Naive Bayes Component

- Creating naive_bayes.py:
``` 

``` 

- Create naive bayes component (naive_bayes.yaml)
```

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

#### XG Boost Component

- Creating xg_boost.py:
``` 

``` 

- Create XgBoost component (xg_boost.yaml)
```

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
COPY xg_boost.py /pipelines
``` 

- Go to the path where dockerfile is, then build Dockerfile and push the image to the Docker Registry:
``` 
docker image build -t omerbsezer/kubeflow_component:xg_boost_v1 .
docker push omerbsezer/kubeflow_component:xg_boost_v1
```

#### Show Results Component


- This component contains following function. It does not needed seperate docker image file. 
``` 
@func_to_container_op
def show_results(decision_tree : float, logistic_regression : float) -> None:
    # Given the outputs from decision_tree and logistic regression components
    # the results are shown.

    print(f"Decision tree (accuracy): {decision_tree}")
    print(f"Logistic regression (accuracy): {logistic_regression}")
``` 


### Compiling and Uploading Pipeline into Kubeflow 

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
def show_results(decision_tree : float, logistic_regression : float) -> None:
    # Given the outputs from decision_tree and logistic regression components
    # the results are shown.

    print(f"Decision tree (accuracy): {decision_tree}")
    print(f"Logistic regression (accuracy): {logistic_regression}")


@dsl.pipeline(name='First Pipeline', description='Applies Decision Tree and Logistic Regression for classification problem.')
def first_pipeline():

    # Loads the yaml manifest for each component
    download = kfp.components.load_component_from_file('download_data/download_data.yaml')
    decision_tree = kfp.components.load_component_from_file('decision_tree/decision_tree.yaml')
    logistic_regression = kfp.components.load_component_from_file('logistic_regression/logistic_regression.yaml')

    # Run download_data task
    download_task = download()

    # Run tasks "decison_tree" and "logistic_regression" given
    # the output generated by "download_task".
    decision_tree_task = decision_tree(download_task.output)
    logistic_regression_task = logistic_regression(download_task.output)

    # Given the outputs from "decision_tree" and "logistic_regression"
    # the component "show_results" is called to print the results.
    show_results(decision_tree_task.output, logistic_regression_task.output)

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(first_pipeline, 'FirstPipeline.yaml')
    # kfp.Client().create_run_from_pipeline_func(basic_pipeline, arguments={})
``` 

- Run pipeline (DSL Compile) to create Workflow Pipeline (Argoflow). After creating pipeline, it creates 'FirstPipeline.yaml'.
``` 
python pipeline.py
``` 

### References
- https://towardsdatascience.com/kubeflow-pipelines-how-to-build-your-first-kubeflow-pipeline-from-scratch-2424227f7e5
