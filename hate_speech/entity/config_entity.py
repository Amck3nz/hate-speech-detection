import os
from dataclasses import dataclass
from hate_speech.constants import *


@dataclass
class DataIngestionConfig:
    def __init__(self):
        self.BUCKET_NAME:str = BUCKET_NAME
        self.ZIP_FILE_NAME:str = ZIP_FILE_NAME

        self.DATA_INGESTION_ARTIFACTS_DIR:str = os.path.join(os.getcwd(), ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR)
        self.DATA_ARTIFACTS_DIR:str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_IMBALANCED_DATA_DIR)
        self.NEW_DATA_ARTIFACTS_DIR:str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESSTION_RAW_DATA_DIR)

        self.ZIP_FILE_DIR:str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR)
        self.ZIP_FILE_PATH:str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR, self.ZIP_FILE_NAME)