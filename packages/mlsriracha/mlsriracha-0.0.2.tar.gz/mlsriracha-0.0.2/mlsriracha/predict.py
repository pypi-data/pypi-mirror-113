from mlsriracha.plugins.azureml.predict import AzureMlPredict
from mlsriracha.plugins.gcpvertex.predict import GcpVertexPredict
from mlsriracha.plugins.awssagemaker.predict import AwsSageMakerPredict

class PredictAdapter:
    def __init__(self, provider: str):
        self.provider_name = provider.lower()

        print('This is a prediction job')
        try: provider
        except NameError: 
            raise RuntimeError(f'{str} is not a valid provider')
        
        if provider.lower() == 'azureml':
            print('Using Azure ML as a provider')
            self.provider_obj = AzureMlPredict()
        elif provider.lower() == 'gcpvertex':
            print('Using GCP Vertex as a provider')
            self.provider_obj = GcpVertexPredict()
        elif provider.lower() == 'awssagemaker':
            print('Using AWS SageMaker as a provider')
            self.provider_obj = AwsSageMakerPredict()
        else:
            raise RuntimeError(f'{str} is not a valid provider')

    def model_artifact(self, filename: str):
        return self.provider_obj.model_artifact(filename)

    def endpoint_metadata(self):
        return self.provider_obj.endpoint_metadata()