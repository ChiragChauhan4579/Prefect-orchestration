# Prefect-orchestration

## Overview of the dataset
This project aims to analyze and predict accident severity using the RTA Dataset. The dataset contains information about accidents, including various attributes such as vehicle make, accident area, driver details, and more. The goal is to build a model that can predict the severity of accidents based on these attributes. Dataset from: https://www.kaggle.com/datasets/saurabhshahane/road-traffic-accidents

## Setup
To run the project, make sure you have Python 3.x installed. You'll also need to install the required libraries listed in requirements.txt. You can install them using pip:

`pip install -r requirements.txt
`

Clone the repository to use `git clone https://github.com/your_username/RTA-Dataset-Analysis.git
cd RTA-Dataset-Analysis`

## What is Prefect?
Prefect is an open-source library that enables you to orchestrate your data workflow in Python. Prefect's mission is to eliminate negative engineering, so that you can focus on positive engineering.

## Prefect Workflow

1. Loading Data: The data is loaded from the 'RTA Dataset.csv' file. Missing values are imputed using the mode of each column. The 'Vehicle_driver_relation' column is dropped as it is not relevant for the analysis.
2. Encoding Data: Categorical features are encoded using an ordinal encoder, mapping each unique value to an integer.
3. Upsampling: The dataset is upsampled using SMOTE to balance the classes.
4. Model Training: An ExtraTreesClassifier model is trained on the upsampled data.
5. Evaluation: The model's accuracy is evaluated using the test set.

Here are the Prefect commands that would help running this all

`prefect server start`: This command starts the Prefect Server, which is the central component for managing and orchestrating workflows. The Prefect Server provides a web interface and API for interacting with your workflows, including monitoring, logging, and management capabilities.

`prefect deployment build main.py:workflow -n deployment -q dev`: This command builds a deployment yaml file for your workflow defined in main.py file. The -n deployment flag specifies the name of the deployment, and -q dev specifies the queue for the deployment. The deployment yaml file includes all the necessary code and configuration for running your workflow.

`prefect deployment apply workflow-deployment.yaml`: This command applies the deployment configuration specified in the workflow-deployment.yaml file. This configuration file defines how your workflow should be deployed, including the deployment target, resource requirements, and any other deployment-specific settings.

`prefect agent start -q dev`: This command starts a Prefect Agent, which is responsible for executing the workflow on the deployment target. The -q dev flag specifies the queue that is to be run by the agent. The agent listens for instructions from the Prefect Server and manages the execution of workflow tasks on the deployment target.
