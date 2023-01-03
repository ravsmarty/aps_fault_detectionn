from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from typing import Optional
import os,sys
from sklearn.preprocessing import Pipeline 
import pandas as pd 
from sensor import utils
import numpy as np
from sklearn.preprocessing import LabelEncoder
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessig import RobustScaler
from sensor.config import TARGET_COLUMN


class DataTransformation:

    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
                    try:
                        self.data_transformation_config=data_transformation_config
                        self.data_ingestion_artifact=data_ingestion_artifact
                    except Exception as e:
                        raise SensorException(e, sys)
    
    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            simple_imputer = SimpleImputer(strategy="constant",fill_value=0)
            robust_scaler = RobustScaler() 
            pipeline = Pipeline(steps=[
                ('Imputer',simple_imputer),
                ('RobustScaler',robust_scaler)
            ]     
            )
            return pipeline
        except Exception as e:
            raise SensorException(e,sys)

    
    def initiate_data_transformation(self,) -> artifact_entity.DataTransformationArtifact:
        try:
            #reading trainig and testing file path
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #selecting input feature for train and test dataframe
            input_feature_train_df = train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN,axis=1)
            
            #selecting target feature for train and test dataframe
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]


            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)
             
            #transformation on target columns
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)
             
             #transforming input features
            transformation_pipeline = DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)
            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)
        except Exception as e:
            raise SensorException(e, sys)


                     