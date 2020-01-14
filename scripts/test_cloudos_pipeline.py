#!/usr/bin/env python3

"""
Submit multiple jobs with different inputs to CloudOS via the API, to test pipelines.
depends on:
> python 3
> argparse==1.1
> json==2.0.9
> requests==2.21.0
> run_cloudos_job.py
> time
"""

import argparse
import json
import time
import run_cloudos_job

def send_job_requests_to_cloudos(inputs):
    for job_name_suffix, s3_path in inputs.items():
        job_name = "{}{}".format(job_name_prefix,job_name_suffix)
        s3_filename, s3_bucket, s3_key = run_cloudos_job.split_s3_path(s3_path)
        job_id = run_cloudos_job.send_job_request_to_cloudos(apikey, team_id, cloudos_url, project_id, workflow_id, workflow_flag, instance_type, instance_disk_space, job_name, s3_filename, s3_bucket, s3_key)
        if job_id:
            print("Job successfully sent to CloudOS. You can check the status " +
                "of the job in https://cloudos.lifebit.ai/app/jobs/{}".format(job_id))
        time.sleep(2)


def load_inputs(json_inputs_path):
    with open(json_inputs_path) as inputs_json:
        return json.load(inputs_json)

def add_cli_arguments():
    # get existing args from run_cloudos_job
    parser_run_cloudos_job = run_cloudos_job.parse_cli_arguments()
    # add new args
    new_parser=argparse.ArgumentParser()
    optional = new_parser.add_argument_group('optional arguments')
    optional.add_argument('-i','--json_inputs_path', help='File path to JSON input containing job name suffixes & S3 files', default='inputs.json')
    optional.add_argument('-j', '--job_name_prefix', help='Prefix for CloudOS job name', default='test_impute_updates_')
    # combine args
    parser_test_cloudos_pipeline = argparse.ArgumentParser(
        description='Submit multiple jobs with different inputs to CloudOS via the API.',
        conflict_handler='resolve',
        parents=[parser_run_cloudos_job, new_parser]
    )
    return parser_test_cloudos_pipeline.parse_args()

if __name__ == "__main__":

    args = add_cli_arguments()

    apikey = args.apikey
    team_id = args.team_id
    cloudos_url = args.cloudos_url
    project_id = args.project_id
    workflow_id = args.workflow_id
    workflow_flag = args.workflow_flag
    instance_type = args.instance_type
    instance_disk_space = args.instance_disk_space
    job_name = args.job_name
    json_inputs_path = args.json_inputs_path
    job_name_prefix = args.job_name_prefix

    inputs = load_inputs(json_inputs_path)

    send_job_requests_to_cloudos(inputs)