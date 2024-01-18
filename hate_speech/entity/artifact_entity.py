
from dataclasses import dataclass 

# Data ingestion artifacts
@dataclass
class DataIngestionArtifacts:
    imbalanced_data: str
    raw_data_file_path: str
    