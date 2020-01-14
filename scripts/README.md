## Quick start

The following contains two python scripts which can be used to submit jobs to CloudOS via the API. Either a single job can be submitted (with `run_cloudos_job.py`) or multiple jobs with different input parameters (using `test_cloudos_pipeline.py`).

![multiple_api_jobs](https://raw.githubusercontent.com/lifebit-ai/images/master/api-jobs/multiple_api_jobs.gif)

### Install dependencies
```python
python3 -m venv .venv # create virtual env
source ./.venv/bin/activate # start using virtual env
pip install -r requirements.txt # install requirements
```

## 1) Submit *one* job to CloudOS via the API - `run_cloudos_job.py`

Submit job to CloudOS via the API.

*Please note that currently this script can only run for pipelines which require a single input file on S3 using AWS cloud.*

### Run script
```bash
python3 run_cloudos_job.py [-h] --apikey APIKEY --project_id PROJECT_ID
                          [--s3_path S3_PATH]
                          [--team_id TEAM_ID]
                          [--cloudos_url CLOUDOS_URL]
                          [--workflow_id WORKFLOW_ID]
                          [--workflow_flag WORKFLOW_FLAG]
                          [--instance_type INSTANCE_TYPE]
                          [--instance_disk_space INSTANCE_DISK_SPACE]
                          [--job_name JOB_NAME]
```

## Arguments:
### Required:
`-a`, `--apikey` API key for CloudOS

`-p`, `--project_id` ID of CloudOS project

#### Optional:
`-s`, `--s3_path` S3 file path of input parameter

`-t`, `--team_id` CloudOS team ID

`-c`, `--cloudos_url` CloudOS API URL

`-w`, `--workflow_id` ID of CloudOS workflow

`-f`, `--workflow_flag` Workflow flag name to specify input parameter(s)

`-y`, `--instance_type` Instance type used to run the job

`-d`, `--instance_disk_space` Disk space in GB of instance used to run the job

`-n`, `--job_name` Name of job on CloudOS

### Example usage
To run the `Fast Imputation` pipeline (the default workflow):
```bash
python3 run_cloudos_job.py \
  --apikey $my_apikey \
  --project_id $my_project_id \
  --job_name test_impute_23andme \
  --s3_path s3://lifebit-featured-datasets/modules/beagle5/test/9135.23andme.7478
```

## 2) Submit *multiple* different jobs to CloudOS via the API with different input parameters - `test_cloudos_pipeline.py`

Submit multiple jobs to CloudOS via the API.

*Please note that currently this script can only be used to test multiple different input files for a given pipeline, however, this could be extended. For example, to test different instance types.*

### Run script
```bash
python3 test_cloudos_pipeline.py --apikey APIKEY --project_id PROJECT_ID
                                [--team_id TEAM_ID]
                                [--cloudos_url CLOUDOS_URL]
                                [--workflow_id WORKFLOW_ID]
                                [--workflow_flag WORKFLOW_FLAG]
                                [--instance_type INSTANCE_TYPE]
                                [--instance_disk_space INSTANCE_DISK_SPACE]
                                [--job_name JOB_NAME] [-h]
                                [--json_inputs_path JSON_INPUTS_PATH]
                                [--job_name_prefix JOB_NAME_PREFIX]
```

## Arguments:
This pipeline has the same arguments as the script above as well as the following optional arguments:

`-i`, `--json_inputs_path` File path to JSON input containing job name suffixes & S3 files

`-j`, `--job_name_prefix` Prefix for CloudOS job name (to be combined with the job name suffix in `-i`)

### Example usage
Test multiple different input formats to the `Fast Imputation` pipeline:
```bash
python3 test_cloudos_pipeline.py \
  --apikey $my_apikey \
  --project_id $my_project_id \
  --json_inputs_path inputs.json \
  --job_name_prefix test_impute_dtc_formats_
```