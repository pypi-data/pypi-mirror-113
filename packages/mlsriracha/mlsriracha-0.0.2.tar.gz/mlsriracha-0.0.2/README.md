# MLsriracha

MLsriracha is a Python library intended to be used with the mlctl and MLbaklava universal MLOps container ecosystem. This SDK is intended to reduce boilerplate code when adopting MLOps system. MLsriracha acts as a common communication layer between your model code and the container deployment requirements for data and metadata in MLOps providers. The intended usage pattern is for ML engineers to build a container with MLSriracha integrated into the model code, and you can use that container in any provider, like SageMaker or Azure ML. 

MLsriracha providers a number of helper functions that handles communications with each provider's opinionated runtime. The functions currently include loading data, storing artifacts, and metadata logging.

Today, MLsriracha helper functions integrate with AzureML and AWS SageMaker as runtime providers, that supports metadata logging to MLFlow.

Roadmap:
- Plugin to run MLsriracha in GCP Vertex
- Plugin to run MLsriracha in Kubeflow Pipelines
- Plugin system to run in a Kubernetes based DIY deployment environment