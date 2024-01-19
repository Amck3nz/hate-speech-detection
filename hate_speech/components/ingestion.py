import os
import sys
from zipfile import ZipFile
from hate_speech.logger import logging
from hate_speech.exception import CustomException
from hate_speech.data.data_sync import GCloudSync
from hate_speech.configuration.config_entity import DataIngestionConfig
from hate_speech.configuration.artifact_entity import DataIngestionArtifacts


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        """
        [Param] data_ingestion_config: Configuration for data ingestion
        """
        self.data_ingestion_config = data_ingestion_config
        self.gcloud = GCloudSync()

    def get_gcloud_data(self) -> None:
        try:
            logging.info("---------- STAGE [get_gcloud_data] STARTED ---------- /n")

            os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR, exist_ok=True)

            self.gcloud.sync_from_gcloud(self.data_ingestion_config.BUCKET_NAME,
                                         self.data_ingestion_config.ZIP_FILE_NAME,
                                         self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR)
            
            logging.info("---------- STAGE [get_gcloud_data] COMPLETED ---------- /n")

        except Exception as e:
            raise CustomException(e, sys) from e
        


    def unzip_and_clean(self):
        logging.info("Entered unzip_and_clean method of Data Ingestion class")
        try:
            with ZipFile(self.data_ingestion_config.ZIP_FILE_PATH, 'r') as zip_ref:
                zip_ref.extractall(self.data_ingestion_config.ZIP_FILE_DIR)
            
            logging.info("Exited unzip_and_clean method of Data Ingestion class")

            return self.data_ingestion_config.DATA_ARTIFACTS_DIR, self.data_ingestion_config.NEW_DATA_ARTIFACTS_DIR
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def process(self) -> DataIngestionArtifacts:
        """
        Description :  Initiates the data ingestion steps
        Output      :  Data ingestion artifact
        On Failure  :  Write exception log and raise exception
        """

        logging.info("Initiating data ingestion stage ----------/n")
        try:

            self.get_gcloud_data()

            logging.info("Data retrieved ----------/n")
            
            imbalanced_data_file_path, raw_data_file_path = self.unzip_and_clean()

            logging.info("File unzipped and split into train and valid data sets ----------/n")

            data_ingestion_artifacts = DataIngestionArtifacts(imbalanced_data_file_path=imbalanced_data_file_path, raw_data_file_path=raw_data_file_path)

            logging.info("Data ingestion intiation completed ----------/n")
            logging.info("Data ingestion artifact: {data_ingestion_artifacts}")

            return data_ingestion_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e
