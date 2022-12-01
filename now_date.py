from time import sleep

import requests

token = "Bearer glpat-xFvFZvEks4P6u8qS4AtJ"

def get_merge_request(merge_request_id):
    response = requests.get(f'https://gitlab.litebox.ru/api/v4/projects/53/merge_requests/{merge_request_id}',
                            headers={"Authorization": token})
    return response.json()


def get_pipeline_jobs(pipeline_id):
    response = requests.get(f'https://gitlab.litebox.ru/api/v4/projects/53/pipelines/{pipeline_id}/jobs',
                            headers={"Authorization": token})
    return response.json()


def retry_job(job_id):
    response = requests.post(f'https://gitlab.litebox.ru/api/v4/projects/53/jobs/{job_id}/retry',
                             headers={"Authorization": token})
    return response.json()


def get_job(job_id):
    response = requests.get(f'https://gitlab.litebox.ru/api/v4/projects/53/jobs/{job_id}',
                             headers={"Authorization": token})
    return response.json()


def check_pipeline(mr_id):
    mr = get_merge_request(mr_id)
    pipeline_id = mr.get('head_pipeline').get('id')
    jobs = get_pipeline_jobs(pipeline_id)
    failed_e2e_id = None
    build_e2e_id = None
    for job in jobs:
        if job['status'] == 'failed' and job['name'] == 'test:e2eTestDevelop':
            failed_e2e_id = job['id']
        elif job['name'] == 'build:e2eDevelopTests':
            build_e2e_id = job['id']
    if failed_e2e_id:
        retry_job(build_e2e_id)
        sleep(3)
        for job in get_pipeline_jobs(pipeline_id):
            if job['name'] == 'build:e2edeveloptests':
                build_e2e_id = job['id']
        while get_job(build_e2e_id)['status'] == 'running':
            sleep(30)
        retry_job(failed_e2e_id)
    sleep(60)


mrs_id = [7114, 7111]

while True:
    for mr_id in mrs_id:
        mr = get_merge_request(mr_id)
        pipeline_id = mr.get('head_pipeline').get('id')
        jobs = get_pipeline_jobs(pipeline_id)
        failed_e2e_id = None
        build_e2e_id = None
        for job in jobs:
            if job['status'] == 'failed' and job['name'] == 'test:e2eTestDevelop':
                failed_e2e_id = job['id']
            elif job['name'] == 'build:e2eDevelopTests':
                build_e2e_id = job['id']
        if failed_e2e_id:
            retry_job(build_e2e_id)
            sleep(3)
            for job in get_pipeline_jobs(pipeline_id):
                if job['name'] == 'build:e2edeveloptests':
                    build_e2e_id = job['id']
            while get_job(build_e2e_id)['status'] == 'running':
                sleep(30)
            retry_job(failed_e2e_id)
    sleep(60)
