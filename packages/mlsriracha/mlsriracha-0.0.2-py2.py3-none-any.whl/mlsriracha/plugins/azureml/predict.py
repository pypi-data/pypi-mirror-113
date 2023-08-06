import os

from mlsriracha.interfaces.predict import PredictInterface

class AzureMlPredict(PredictInterface):

    def __init__(self):
        print('Selected Azure ML profile')

    def model_artifact(self, filename: str):
        """
        The path to model artifacts.

        Loads from the environmental variable set by mlctl where 
        to retrieve the artifact from Azure ML's mount points. 

        Arguments:
            filename (str): The name of the file which will be written back to S3

        Returns:
            path (str): The absolute path to the model output directory
        """
        model_uri = os.environ.get('AZUREML_MODEL_DIR')
        return os.path.join(model_uri, filename)

    def endpoint_metadata(self):
        return {}