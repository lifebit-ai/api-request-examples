#!/usr/bin/env python3

"""
Submit job to CloudOS via the API.
depends on:
> python 3
> argparse==1.1
> json==2.0.9
> requests==2.21.0
"""

import argparse
import json
import requests

def send_job_request_to_cloudos(apikey, team_id, cloudos_url, project_id, workflow_id, workflow_flag, instance_type, instance_disk_space, job_name, s3_filename, s3_bucket, s3_key):
    # Prepare api request for CloudOS to run a job
    headers = {
        "Content-type": "application/json",
        "apikey": apikey
    }

    workflow_params = [
        {
            "name": workflow_flag,
            "prefix": "--",
            "dataItemEmbedded": {
                "type": "S3File",
                "data": {
                    "name": s3_filename,
                    "s3BucketName": s3_bucket,
                    "s3ObjectKey": s3_key
                }
            }
        }
    ]

    params = {
        "executionPlatform": "aws",
        "project": project_id,
        "workflow": workflow_id,
        "parameters": workflow_params,
        "instanceType": instance_type,
        "storageSizeInGb": instance_disk_space,
        "name": job_name
    }

    r = requests.post("{}/api/v1/jobs".format(cloudos_url), data=json.dumps(params), headers=headers)
    return (json.loads(r.content)["_id"])

def split_s3_path(s3_path):
    path_parts=s3_path.replace("s3://","").split("/")
    s3_filename=path_parts[-1]
    s3_bucket=path_parts.pop(0)
    s3_key="/".join(path_parts)
    return s3_filename, s3_bucket, s3_key

def parse_cli_arguments():
    parser = argparse.ArgumentParser(description='Submit job to CloudOS via the API.')
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('-a', '--apikey', help='API key for CloudOS', required=True)
    required.add_argument('-p', '--project_id', help='ID of CloudOS project', required=True)
    optional.add_argument('-s', '--s3_path', help='S3 file path of input parameter', default='s3://lifebit-featured-datasets/modules/beagle5/test/8982.23andme.7325')
    optional.add_argument('-t', '--team_id', help='CloudOS team ID', default='myTeamId')	
    optional.add_argument('-c', '--cloudos_url', help='CloudOS API URL', default='https://cloudos.lifebit.ai')
    optional.add_argument('-w', '--workflow_id', help='ID of CloudOS workflow', default='d4b6f1351d411e8ef0d78256') # default = Fast Imputation
    optional.add_argument('-f', '--workflow_flag', help='Workflow flag name to specify input parameter(s)', default='genotypes_path')
    optional.add_argument('-y', '--instance_type', help='Instance type used to run the job', default='m4.2xlarge')
    optional.add_argument('-d', '--instance_disk_space', help='Disk space in GB of instance used to run the job', default=500)
    optional.add_argument('-n', '--job_name', help='Name of job on CloudOS', default='Jeff')
    return parser

if __name__ == "__main__":
    args = parse_cli_arguments().parse_args()

    apikey = args.apikey
    team_id = args.team_id
    cloudos_url = args.cloudos_url
    project_id = args.project_id
    workflow_id = args.workflow_id
    workflow_flag = args.workflow_flag
    instance_type = args.instance_type
    instance_disk_space = args.instance_disk_space
    job_name = args.job_name
    s3_path = args.s3_path
    s3_filename, s3_bucket, s3_key = split_s3_path(s3_path)
    
    job_id = send_job_request_to_cloudos(apikey, team_id, cloudos_url, project_id, workflow_id, workflow_flag, instance_type, instance_disk_space, job_name, s3_filename, s3_bucket, s3_key)
    if job_id:
        print("Job successfully sent to CloudOS. You can check the status " +
              "of the job in https://cloudos.lifebit.ai/app/jobs/{}".format(job_id))