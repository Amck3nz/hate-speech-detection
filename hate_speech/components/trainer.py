import os 
import sys
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences

from hate_speech.logger import logging
from hate_speech.constants import *
from hate_speech.exception import CustomException
from hate_speech.models.model import ModelArchitecture
from hate_speech.configuration.configs import ModelTrainerConfig
from hate_speech.configuration.artifacts import ModelTrainerArtifacts, DataTransformationArtifacts


class ModelTrainer:
    def __init__(self, data_transformation_artifacts: DataTransformationArtifacts,
                model_trainer_config: ModelTrainerConfig):

        self.data_transformation_artifacts = data_transformation_artifacts
        self.model_trainer_config = model_trainer_config

    
    def spliting_data(self, csv_path):
        try:
            logging.info("STAGE [spliting_data] STARTED ----------/n")
            logging.info("Reading data...")
            df = pd.read_csv(csv_path, index_col=False)
            logging.info("Splitting data into x and y...")
            x = df[TWEET]
            y = df[LABEL]

            logging.info("Creating train_test_split...")
            x_train,x_test,y_train,y_test = train_test_split(x, y, test_size=0.3, random_state=42)
            print(len(x_train),len(y_train))
            print(len(x_test),len(y_test))
            print(type(x_train),type(y_train))
            logging.info("STAGE [splitting_data] COMPLETED ----------/n")
            return x_train,x_test,y_train,y_test

        except Exception as e:
            raise CustomException(e, sys) from e

    def tokenizing(self, x_train):
        try:
            logging.info("Begining data tokenization...")
            tokenizer = Tokenizer(num_words=self.model_trainer_config.MAX_WORDS)
            tokenizer.fit_on_texts(x_train)
            sequences = tokenizer.texts_to_sequences(x_train)
            logging.info(f"Converting text to sequences: {sequences}")
            sequences_matrix = pad_sequences(sequences,maxlen=self.model_trainer_config.MAX_LEN)
            logging.info(f" Sequence matrix is: {sequences_matrix}")
            return sequences_matrix,tokenizer
        
        except Exception as e:
            raise CustomException(e, sys) from e


    
    def train_model(self,) -> ModelTrainerArtifacts:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        """
        Method Name :   initiate_model_trainer
        Description :   This function initiates a model trainer steps
        
        Output      :   Returns model trainer artifact
        On Failure  :   Write an exception log and then raise an exception
        """

        try:
            logging.info("STAGE [initiate_model_trainer] STARTED ----------/n ")
            x_train, x_test, y_train, y_test = self.spliting_data(csv_path=self.data_transformation_artifacts.transformed_data_path)
            model_architecture = ModelArchitecture()   

            model = model_architecture.get_model()



            logging.info(f"Xtrain size is : {x_train.shape}")

            logging.info(f"Xtest size is : {x_test.shape}")

            sequences_matrix,tokenizer =self.tokenizing(x_train)


            logging.info("Model training STARTED ----------/n")
            model.fit(sequences_matrix, y_train, 
                        batch_size=self.model_trainer_config.BATCH_SIZE, 
                        epochs = self.model_trainer_config.EPOCH, 
                        validation_split=self.model_trainer_config.VALIDATION_SPLIT, 
                        )
            logging.info("Model training COMPLETE ----------/n")
            with open('tokenizer.pickle', 'wb') as handle:
                pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
            os.makedirs(self.model_trainer_config.TRAINED_MODEL_DIR, exist_ok=True)



            logging.info("Saving model...")
            model.save(self.model_trainer_config.TRAINED_MODEL_PATH)
            x_test.to_csv(self.model_trainer_config.X_TEST_DATA_PATH)
            y_test.to_csv(self.model_trainer_config.Y_TEST_DATA_PATH)

            x_train.to_csv(self.model_trainer_config.X_TRAIN_DATA_PATH)

            model_trainer_artifacts = ModelTrainerArtifacts(
                trained_model_path = self.model_trainer_config.TRAINED_MODEL_PATH,
                x_test_path = self.model_trainer_config.X_TEST_DATA_PATH,
                y_test_path = self.model_trainer_config.Y_TEST_DATA_PATH)
            logging.info("Returning ModelTrainerArtifacts...")
            return model_trainer_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e