import numpy as np
import tensorflow as tf
from azureml.core.run import Run
from time import time
from contextlib import contextmanager
from azureml.studio.core.logger import common_logger


@contextmanager
def run_log_error_handler():
    try:
        yield
    except BaseException as ex:
        common_logger.warning(
            f"Failed to upload training metrics. Reason: {ex}")


class LogHook(tf.estimator.SessionRunHook):
    """This class inherits from tf.estimator.SessionRunHook, the hook to extend calls for each session run.
    For details, please see: https://www.tensorflow.org/api_docs/python/tf/estimator/SessionRunHook
    """

    LOSS_TABLE_NAME = "Loss"
    THROUGHPUT_TABLE_NAME = "Train samples per second"

    def __init__(self, total_steps, log_steps, batch_per_step, replica_count):
        self.log_every_n_steps = np.ceil(total_steps / log_steps)
        self.batch_per_step = batch_per_step
        self.steps = 0
        self.run = Run.get_context()
        self.cum_loss = 0.0
        self.start_time = time()
        self.replica_count = replica_count

    def after_run(self, run_context, run_values):
        """Called after each call to run. We compute loss, the cost time after each run."""
        self.steps += 1
        self.cum_loss += run_values.results[1]

        if self.steps % self.log_every_n_steps == 0:
            avg_loss = self.cum_loss / self.log_every_n_steps
            avg_samples_per_second = (self.log_every_n_steps * self.batch_per_step * self.replica_count) / (
                    time() - self.start_time)
            self.cum_loss = 0.0
            self.start_time = time()

            with run_log_error_handler():
                self.run.log_row(self.LOSS_TABLE_NAME, **{"Global step": self.steps, "Loss": avg_loss})
                self.run.log_row(self.THROUGHPUT_TABLE_NAME,
                                 **{"Global step": self.steps, "Train samples per second": avg_samples_per_second})

    def before_run(self, run_context):
        """Called before each call to run. We simply return the session run args here."""
        return run_context.original_args

    def end(self, session):
        """Called at the end of session. We flush the metrics after the session completes."""
        with run_log_error_handler():
            self.run.flush()
