import os

"""
Download/push data between cloud and local directory
"""

# Google Cloud
class GCloudSync:
    
    def sync_to_gcloud(self, gcp_bucket_url, filepath, filename):
        command = f"gsutil cp {filepath}/{filename} gs://{gcp_bucket_url}/"
        # command = f"gcloud storage cp {filepath}/{filename} gs://{gcp_bucket_url}/"
        os.system(command)
            
    def sync_from_gcloud(self, gcp_bucket_url, filepath, filename):
        command = f"gsutil cp gs://{gcp_bucket_url}/{filename} {filepath}/{filename}"
        # command = f"gcloud storage cp gs://{gcp_bucket_url}/{filename} {filepath}/{filename}"
        os.system(command)