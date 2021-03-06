from .execution import Execution
from .executor_base import Executor

"""
Runs a local command using SSH CLI.
"""


class ExecutorLocal(Executor):
    """
    Executes a given command locally.
    """

    implementation = "local"

    def __init__(self, name: str = "ExecutorLocal", **kwargs):
        super(ExecutorLocal, self).__init__(**kwargs)
        self.name = name

    def _execute(self, command):
        return Execution(command, self)
