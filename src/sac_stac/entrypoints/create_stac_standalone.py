import logging

# So that we can run as a standalone script
import sys
sys.path.append('../../')

from sac_stac.adapters import repository
from sac_stac.domain.s3 import S3
from sac_stac.service_layer.services import add_stac_collection
from sac_stac.load_config import LOG_LEVEL, LOG_FORMAT, get_s3_configuration
from sac_stac.domain.model import SacCollection


import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import boto3

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

S3_ACCESS_KEY_ID = get_s3_configuration()["key_id"]
S3_SECRET_ACCESS_KEY = get_s3_configuration()["access_key"]
S3_REGION = get_s3_configuration()["region"]
S3_ENDPOINT = get_s3_configuration()["endpoint"]
S3_BUCKET = get_s3_configuration()["bucket"]
S3_STAC_KEY = get_s3_configuration()["stac_key"]
S3_HREF = f"{S3_ENDPOINT}/{S3_BUCKET}"

s3 = S3(key=S3_ACCESS_KEY_ID, secret=S3_SECRET_ACCESS_KEY,
        s3_endpoint=S3_ENDPOINT, region_name=S3_REGION)
repo = repository.S3Repository(s3)

# Allows for extra functionality - list_objects_v2
s3_resource = boto3.resource(
"s3",
endpoint_url=S3_ENDPOINT,
region_name=S3_REGION,
aws_access_key_id=S3_ACCESS_KEY_ID,
aws_secret_access_key=S3_SECRET_ACCESS_KEY,
)

def main():
    # Lists all platforms in the S3 'Directory'
    platforms = s3_resource.meta.client.list_objects_v2(Bucket=S3_BUCKET, Prefix='common_sensing/fiji/', Delimiter='/')
    
    # Loops through each platform
    for platform in platforms.get('CommonPrefixes', []):
        try:
            sensor_name = platform['Prefix'].split('/')[-2]
            add_stac_collection(repo=repo, sensor_key=platform['Prefix'], update_collection_on_item=False)
            collection_key = f"{S3_STAC_KEY}/{sensor_name}/collection.json"
            collection_dict = repo.get_dict(bucket=S3_BUCKET, key=collection_key)
            
            # Rather than looping this everytime, we can do this at the end (saves a lot of time)
            collection = SacCollection.from_dict(collection_dict)
            collection.update_extent_from_items()
            collection.normalize_hrefs(f"{S3_HREF}/{S3_STAC_KEY}/{collection.id}")
        except Exception as e:
            logger.error(f"Error adding collection for {platform['Prefix']} :: {e}")
    
if __name__ == '__main__':
    main()