import os
import time
import datetime
from typing import Dict, List
import requests

from biolib import utils
from biolib.compute_node.job_worker import job_worker_config
from biolib.compute_node.webserver.worker_thread import WorkerThread
from biolib.compute_node.webserver import webserver_config
from biolib.biolib_errors import BioLibError
from biolib.biolib_logging import logger

# Global constants
DEV_MODE = os.getenv('COMPUTE_NODE_ENV') == 'dev'
BASE_URL = ''

# Only for enclaves
COMPUTE_NODE_INFO: Dict = {}
ENCLAVE_ECR_TOKEN = ''

JOB_ID_TO_COMPUTE_STATE_DICT: Dict = {}
UNASSIGNED_COMPUTE_PROCESSES: List = []


def finalize_and_clean_up_compute_job(job_id: str):
    JOB_ID_TO_COMPUTE_STATE_DICT.pop(job_id)

    if utils.BIOLIB_IS_RUNNING_IN_ENCLAVE and not DEV_MODE:
        logger.debug('Deregistering and shutting down...')
        _deregister_and_shutdown()


def _deregister_and_shutdown():
    requests.post(url=f'{job_worker_config.PARENT_REST_SERVER_URL}/deregister_and_shutdown/')


def get_compute_state(unassigned_compute_processes):
    if len(unassigned_compute_processes) == 0:
        start_compute_process(unassigned_compute_processes)

    return unassigned_compute_processes.pop()


def start_compute_process(unassigned_compute_processes):
    compute_state = {
        'job_id': None,
        'status': {
            'status_updates': [
                {
                    'progress': 10,
                    'log_message': 'Initializing'
                }
            ],
        },
        'result': None,
        'attestation_document': b'',
        'received_messages_queue': None,
        'messages_to_send_queue': None,
        'worker_process': None
    }

    WorkerThread(compute_state).start()

    while True:
        if compute_state['attestation_document']:
            break
        time.sleep(1)

    unassigned_compute_processes.append(compute_state)


def start_shutdown_timer(shutdown_time):
    requests.post(
        url=f'{job_worker_config.PARENT_REST_SERVER_URL}/start_shutdown_timer/',
        json={
            'shutdown_time': shutdown_time
        })


def validate_saved_job(saved_job):
    if 'app_version' not in saved_job['job']:
        return False

    if 'access_token' not in saved_job:
        return False

    if 'module_name' not in saved_job:
        return False

    return True


def report_availability(compute_node_info, base_url, dev_mode):
    try:
        data = {
            'public_id': compute_node_info['public_id'],
            'auth_token': compute_node_info['auth_token'],
            'ip_address': compute_node_info['ip_address']
        }
        logger.debug(f'Registering with {data} to host {base_url}')
        logger.debug(f'Registering at {datetime.datetime.now()}')

        max_retries = 5
        for retry in range(max_retries):
            try:
                req = requests.post(f'{base_url}/api/jobs/report_available/', json=data)
            except Exception as error:  # pylint: disable=broad-except
                if retry >= max_retries:
                    logger.error(error)
                    raise BioLibError("Failed to register. Max retry limit reached") from error
                time.sleep(1)
                continue
            break

        if req.status_code != 201:
            raise Exception("Non 201 error code")

        if req.json()['is_reserved']:
            # Start running job shutdown timer if reserved. It restarts when the job is actually saved
            start_shutdown_timer(webserver_config.COMPUTE_NODE_RUNNING_JOB_SHUTDOWN_TIME_MINUTES)

        else:
            # Else start the longer auto shutdown timer
            start_shutdown_timer(webserver_config.COMPUTE_NODE_AUTO_SHUTDOWN_TIME_MINUTES)

    except Exception as exception:  # pylint: disable=broad-except
        logger.error(f'Could not self register because of: {exception}')
        logger.debug("Self destructing")
        if not dev_mode:
            _deregister_and_shutdown()
