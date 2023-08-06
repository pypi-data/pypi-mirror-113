from mlsriracha.plugins.azureml.train import AzureMlTrain
from mlsriracha.plugins.gcpvertex.train import GcpVertexTrain
from mlsriracha.plugins.awssagemaker.train import AwsSageMakerTrain
from mlsriracha.plugins.mlflow.metadata import MlFlowMetadata

class TrainingAdapter:
    def __init__(self,
        providers):

        print('This is a training job')
        self.metadata_objs = []

        # add comma to make the array split work
        
        if providers is None:
            print('No providers were passed to sriracha, disabling in this run.')
            return
        elif providers.find(',') == -1:
            providers += ','

        # get list of providers added
        for provider in providers.split(','):
            
            try: provider
            except NameError: 
                raise RuntimeError(f'{str} is not a valid provider')

            
            
            if provider.lower() == 'azureml':
                print('Using Azure ML as a provider')
                self.provider_obj = AzureMlTrain()
                self.provider_name = provider.lower()
            
            elif provider.lower() == 'gcpvertex':
                print('Using GCP Vertex as a provider')
                self.provider_obj = GcpVertexTrain()
                self.provider_name = provider.lower()

            elif provider.lower() == 'awssagemaker':
                print('Using AWS SageMaker as a provider')
                self.provider_obj = AwsSageMakerTrain()
                self.provider_name = provider.lower()

            elif provider.lower() == 'mlflow':
                self.metadata_objs.append(MlFlowMetadata())

            else:
                raise RuntimeError(f'{provider} is not a valid provider')
        
            
    def input_as_dataframe(self, channel: str):
        return self.provider_obj.input_as_dataframe(channel=channel)

    def artifact_path(self, filename: str):
        return self.provider_obj.log_artifact(filename)

    def log_param(self, params):
        for metadata_obj in self.metadata_objs:
            metadata_obj.log_param(params)

    def log_artifact(self, object, type='model'):
        for metadata_obj in self.metadata_objs:
            metadata_obj.log_artifact(object, type)

    def log_metric(self, params):
        for metadata_obj in self.metadata_objs:
            metadata_obj.log_metric(params) 

    def finish(self):
        return self.provider_obj.finish()