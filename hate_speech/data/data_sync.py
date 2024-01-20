import os

"""
Download/push data between cloud and local directory
"""

class GCloudSync:

    def sync_to_gcloud(self, gcp_bucket_url, filepath, filename):
        
        command = f"gsutil cp {filepath}/{filename} gs://hate-speech-project-bucket/"
        #command = f"gsutil cp {filepath}/{filename} gs://{gcp_bucket_url}/"
        # command = f"gcloud storage cp {filepath}/{filename} gs://{gcp_bucket_url}/"
        os.system(command)

    def sync_from_gcloud(self, gcp_bucket_url, filename, destination):

        command = f"gsutil cp gs://hate-speech-project-bucket/{filename} {destination}/{filename}"
        #command = f"gsutil cp gs://{gcp_bucket_url}/{filename} {destination}/{filename}"
        # command = f"gcloud storage cp gs://{gcp_bucket_url}/{filename} {destination}/{filename}"
        os.system(command)