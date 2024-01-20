import sys
from hate_speech.logger import logging
from hate_speech.exception import CustomException
from hate_speech.data.data_sync import GCloudSync
from hate_speech.configuration.configs import ModelPusherConfig
from hate_speech.configuration.artifacts import ModelPusherArtifacts

class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig):
        """
        [param] model_pusher_config: Configuration for model pusher
        """
        self.model_pusher_config = model_pusher_config
        self.gcloud = GCloudSync()

    
    
    def push_model(self) -> ModelPusherArtifacts:
        """
            Method Name :   initiate_model_pusher
            Description :   This method initiates model pusher.

            Output      :    Model pusher artifact
        """
        logging.info("---------- STAGE [initiate_model_pusher] STARTED ---------- /n")
        try:
            # Uploading model to gcloud storage

            self.gcloud.sync_to_gcloud(self.model_pusher_config.BUCKET_NAME,
                                              self.model_pusher_config.TRAINED_MODEL_PATH,
                                              self.model_pusher_config.MODEL_NAME)

            logging.info("Uploaded best performing model to gcloud storage")

            # Saving model pusher outputs
            model_pusher_artifact = ModelPusherArtifacts(
                bucket_name=self.model_pusher_config.BUCKET_NAME
            )
            logging.info("---------- STAGE [initiate_model_pusher] COMPLETED ---------- /n")
            return model_pusher_artifact

        except Exception as e:
            raise CustomException(e, sys) from e