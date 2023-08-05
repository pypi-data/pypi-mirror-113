import logging
import os
import random
import subprocess
import sys
import time
import threading
import socket
from queue import Queue

from biolib.compute_node.socker_listener_thread import SocketListenerThread
from biolib.compute_node.socket_sender_thread import SocketSenderThread
from biolib.compute_node.webserver import webserver_utils
from biolib.biolib_binary_format import AttestationDocument, SystemStatusUpdate, SystemException
from biolib.compute_node.utils import get_package_type, WorkerThreadException, SystemExceptionCodes
from biolib.biolib_logging import logger

SOCKET_HOST = '127.0.0.1'


class WorkerThread(threading.Thread):
    def __init__(self, compute_state, is_running_in_enclave=False):
        try:
            super().__init__()
            self.compute_state = compute_state
            self.is_running_in_enclave = is_running_in_enclave
            self.socket_port = random.choice(range(6000, 65000))
            self.socket = None
            self.connection = None
            self.compute_process = None
            self.connection_thread = None
            self.listener_thread = None
            self.sender_thread = None
            self._start_and_connect_to_compute_process()

            logger.debug(f"WorkerThread connected to port {self.socket_port}")

        except Exception as exception:
            raise WorkerThreadException(exception, SystemExceptionCodes.FAILED_TO_INITIALIZE_WORKER_THREAD.value,
                                        worker_thread=self) from exception

    def run(self):
        try:
            while True:
                package = self.compute_state['received_messages_queue'].get()
                package_type = get_package_type(package)

                if package_type == 'AttestationDocument':
                    self.compute_state['attestation_document'] = AttestationDocument(package).deserialize()

                elif package_type == 'SystemStatusUpdate':
                    progress, log_message = SystemStatusUpdate(package).deserialize()
                    self.compute_state['status']['status_updates'].append({'progress': progress,
                                                                           'log_message': log_message})

                elif package_type == 'SystemException':
                    error_code = SystemException(package).deserialize()
                    self.compute_state['status']['error_code'] = error_code
                    logger.debug("Hit error. Terminating Worker Thread and Compute Process")
                    self.terminate()

                elif package_type == 'ModuleOutput' or package_type == 'AesEncryptedPackage':
                    self.compute_state['result'] = package
                    self.compute_state['status']['status_updates'].append({'progress': 95,
                                                                           'log_message': 'Result Ready'})
                    self.terminate()

                else:
                    raise Exception(f'Package type from child was not recognized: {package}')

                self.compute_state['received_messages_queue'].task_done()

        except Exception as exception:
            raise WorkerThreadException(exception, SystemExceptionCodes.FAILED_TO_HANDLE_PACKAGE_IN_WORKER_THREAD.value,
                                        worker_thread=self) from exception

    def _start_and_connect_to_compute_process(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.debug(f"Trying to bind to socket on {SOCKET_HOST}:{self.socket_port}")
        self.socket.bind((SOCKET_HOST, self.socket_port))

        logger.debug(f"Starting to listen to socket on port {self.socket_port}")
        self.socket.listen()
        logger.debug(f"Listening to port {self.socket_port}")

        received_messages_queue = Queue()
        messages_to_send_queue = Queue()

        # Starting a thread for accepting connections before starting the process that should to connect to the socket
        logger.debug("Starting connection thread")
        self.connection_thread = threading.Thread(target=self._accept_new_socket_connection, args=[
            received_messages_queue,
            messages_to_send_queue
        ])
        self.connection_thread.start()
        logger.debug("Started connection thread")
        logger.debug("Starting compute process")

        compute_process_cmd = ['biolib', 'start-compute-process', '--port', str(self.socket_port)]
        if self.is_running_in_enclave:
            compute_process_cmd.append('--enclave')

        self.compute_process = subprocess.Popen(
            args=compute_process_cmd,
            env=dict(os.environ, BIOLIB_LOG=logging.getLevelName(logger.level))
        )

        self.compute_state['received_messages_queue'] = received_messages_queue
        self.compute_state['messages_to_send_queue'] = messages_to_send_queue
        self.compute_state['worker_thread'] = self

    def _accept_new_socket_connection(self, received_messages_queue, messages_to_send_queue):
        self.connection, _ = self.socket.accept()
        self.listener_thread = SocketListenerThread(self.connection, received_messages_queue)
        self.listener_thread.start()

        self.sender_thread = SocketSenderThread(self.connection, messages_to_send_queue)
        self.sender_thread.start()

    def terminate(self):
        if self.compute_process:
            logger.debug(f"Terminating Compute Process with PID {self.compute_process.pid}")
            self.compute_state['messages_to_send_queue'].put(b'STOP')

        if self.socket:
            self.socket.close()

        if self.connection:
            self.connection.close()

        if self.compute_state['result']:
            seconds_to_sleep = 60
            job_id = self.compute_state['job_id']
            logger.debug(f'Worker thread sleeping for {seconds_to_sleep} seconds before cleaning up job {job_id}')
            # sleep to see if the user has begun downloading the result
            time.sleep(seconds_to_sleep)
            if self.compute_state['result']:
                logger.debug(f'Cleaning up job {job_id} as result was not fetched within {seconds_to_sleep} seconds')
                webserver_utils.finalize_and_clean_up_compute_job(job_id)
            else:
                logger.debug(f'Job {job_id} already cleaned up')

        logger.debug("Terminating Worker Thread")
        sys.exit()
