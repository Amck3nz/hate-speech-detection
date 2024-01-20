import os
import sys
import io
from PIL import Image
import pickle
import keras
from keras.utils import pad_sequences

from hate_speech.logger import logging
from hate_speech.constants import *
from hate_speech.exception import CustomException
from hate_speech.data.data_sync import GCloudSync
from hate_speech.components.transformation import DataTransformation
from hate_speech.configuration.configs import DataTransformationConfig
from hate_speech.configuration.artifacts import DataIngestionArtifacts



class PredictionPipeline:
    def __init__(self):
        self.bucket_name = BUCKET_NAME
        self.model_name = MODEL_NAME
        self.model_path = os.path.join("artifacts", "PredictModel")
        self.gcloud = GCloudSync()
        self.data_transformation = DataTransformation(data_transformation_config= DataTransformationConfig,data_ingestion_artifacts=DataIngestionArtifacts)

    
    def get_model_from_gcloud(self) -> str:
        """
        Method Name :   get_model_from_gcloud
        Description :   This method to get best model from google cloud storage
        Output      :   best_model_path
        """
        logging.info("STAGE [get_model_from_gcloud] STARTED ----------/n")
        try:
            # Loading the best model from s3 bucket
            os.makedirs(self.model_path, exist_ok=True)
            self.gcloud.sync_from_gcloud(self.bucket_name, self.model_name, self.model_path)
            best_model_path = os.path.join(self.model_path, self.model_name)
            logging.info("STAGE [get_model_from_gcloud] COMPLETED ----------/n")
            return best_model_path

        except Exception as e:
            raise CustomException(e, sys) from e

    
    def predict(self,best_model_path,text):
        """load image, returns cuda tensor"""
        
        logging.info("Predicting...")
        try:
            best_model_path:str = self.get_model_from_gcloud()
            load_model=keras.models.load_model(best_model_path)
            with open('tokenizer.pickle', 'rb') as handle:
                load_tokenizer = pickle.load(handle)
            
            text=self.data_transformation.concat_data_cleaning(text)
            text = [text]            
            print(text)
            seq = load_tokenizer.texts_to_sequences(text)
            padded = pad_sequences(seq, maxlen=300)
            print(seq)
            pred = load_model.predict(padded)
            #pred
            print("pred", pred)
            if pred>0.3:

                print("hate and abusive")
                return "hate and abusive"
            else:
                print("no hate")
                return "no hate"
        except Exception as e:
            raise CustomException(e, sys) from e

    
    def run_pipeline(self,text):
        logging.info("STAGE [run_pipeline] STARTED ----------/n")
        try:

            best_model_path: str = self.get_model_from_gcloud() 
            predicted_text = self.predict(best_model_path,text)
            logging.info("STAGE [run_pipeline] COMPLETED ----------/n")
            return predicted_text
        except Exception as e:
            raise CustomException(e, sys) from e