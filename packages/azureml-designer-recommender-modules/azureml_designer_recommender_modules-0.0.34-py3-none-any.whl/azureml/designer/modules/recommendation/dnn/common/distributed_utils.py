import os
import json
import tensorflow as tf
from enum import Enum
from azureml.studio.core.logger import common_logger


class DistributedStrategy(Enum):
    MultiWorkerMirroredStrategy = "Multi Worker Mirrored Strategy"
    MultiDeviceMirroredStrategy = "Multi Device Mirrored Strategy"
    NonDistributedStrategy = "Non-distributed Strategy"


class DistributedEnv:
    # These environment variables are for multi nodes training, which represent the node ips, node count, process count.
    # Here is an example of those env vars and their values:
    # AZ_BATCH_HOST_LIST = 10.0.0.4,10.0.0.8,10.0.0.9
    # AZUREML_PARAMETER_Mpi_Process_Count_Per_Node = 2
    # AZUREML_NODE_COUNT = 3
    # AZ_BATCHAI_TASK_INDEX = 0
    HOST_LIST_ENV = "AZ_BATCH_HOST_LIST"
    PROCESS_PER_NODE_ENV = "AZUREML_PARAMETER_Mpi_Process_Count_Per_Node"
    # This environment variable has the same meaning with PROCESS_PER_NODE_ENV, and it's used for open mpi image
    OMPI_PROCESS_PER_NODE_ENV = "OMPI_COMM_WORLD_LOCAL_SIZE"
    NODE_COUNT_ENV = "AZUREML_NODE_COUNT"
    TASK_INDEX_ENV = "AZ_BATCHAI_TASK_INDEX"
    # Below env variables are for TensorFlow
    TF_CLUSTER_CONFIG_ENV = "TF_CONFIG"
    TF_CUDA_VISIBLE_DEVICES_ENV = "CUDA_VISIBLE_DEVICES"
    # The worker port is start from this number
    CHIEF_WORKER_PORT = 49152

    def __init__(self):
        self.hosts = os.environ.get(self.HOST_LIST_ENV, 'localhost')

        if self.PROCESS_PER_NODE_ENV in os.environ:
            self.process_per_node = int(os.environ[self.PROCESS_PER_NODE_ENV])
        elif self.OMPI_PROCESS_PER_NODE_ENV in os.environ:
            self.process_per_node = int(os.environ[self.OMPI_PROCESS_PER_NODE_ENV])
        else:
            self.process_per_node = None

        self.node_count = int(os.environ[self.NODE_COUNT_ENV]) if self.NODE_COUNT_ENV in os.environ else None
        self.task_index = int(os.environ[self.TASK_INDEX_ENV]) if self.TASK_INDEX_ENV in os.environ else None
        self.distributed_strategy = None

    def is_chief(self):
        return self.task_index == 0 or self.task_index is None

    def _init_strategy(self, use_gpu=True):
        if self.worker_count > 1:
            self.distributed_strategy = DistributedStrategy.MultiWorkerMirroredStrategy
            common_logger.info(f"Initialize distributed strategy: {self.distributed_strategy}.")
            return

        gpu_devices = tf.config.list_physical_devices('GPU')
        common_logger.info(f"Found {len(gpu_devices)} GPU devices.")

        if len(gpu_devices) <= 1 or not use_gpu:
            self.distributed_strategy = DistributedStrategy.NonDistributedStrategy
        else:
            self.distributed_strategy = DistributedStrategy.MultiDeviceMirroredStrategy

        common_logger.info(f"Initialize distributed strategy: {self.distributed_strategy}.")

    def init(self, use_gpu=True):
        self._init_strategy(use_gpu)
        if self.distributed_strategy == DistributedStrategy.MultiWorkerMirroredStrategy:
            self._init_multi_worker_mirrored_cluster()

    def _init_multi_worker_mirrored_cluster(self, use_gpu=True):
        if self.cluster_exists():
            common_logger.info("Training cluster exists, skip cluster setup.")
            common_logger.info(os.environ[self.TF_CLUSTER_CONFIG_ENV])
            return

        common_logger.info(f"Node List: {self.hosts}, "
                           f"Process Per Node: {self.process_per_node}, "
                           f"Task index: {self.task_index}")

        # the worker needs to know the explicit port each others use, the ports start from chief port number
        workers = [f'{node}:{port}' for node in self.hosts.split(',') for port in
                   range(self.CHIEF_WORKER_PORT, self.CHIEF_WORKER_PORT + self.process_per_node)]

        cluster_config = {
            'cluster': {
                'chief': workers[:1],
                'worker': workers[1:]
            },
        }
        if self.task_index == 0:
            cluster_config['task'] = {'type': 'chief', 'index': 0}
        else:
            cluster_config['task'] = {'type': 'worker', 'index': self.task_index - 1}

        os.environ[self.TF_CLUSTER_CONFIG_ENV] = json.dumps(cluster_config)
        if use_gpu:
            os.environ[self.TF_CUDA_VISIBLE_DEVICES_ENV] = str(self.task_index % self.process_per_node)
        else:
            os.environ[self.TF_CUDA_VISIBLE_DEVICES_ENV] = '-1'
        common_logger.info(f"Setup training cluster for multi worker mirrored strategy: {cluster_config}")

        return

    @property
    def worker_count(self):
        # if self.node_count or self.process_per_node is None, that is only one worker/node.
        if self.node_count is None or self.process_per_node is None:
            return 1

        return self.node_count * self.process_per_node

    def cluster_exists(self):
        return os.environ.get(self.TF_CLUSTER_CONFIG_ENV, None) is not None


distributed_env = DistributedEnv()
