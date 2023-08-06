import collections
import json
import logging
import logging.handlers
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from subprocess import Popen
import contextlib

import backoff
import requests

log = logging.getLogger(__name__)


def is_windows():
    return sys.platform.startswith("win")


def prepare_path(path: str) -> None:
    """
    Prepares `path` by creating non-existing folders and checking
    whether the user can read and write `path`
    """
    # https://stackoverflow.com/a/51642916/14969816
    log.info(f"Validating path {path}")
    try:
        os.makedirs(path, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=path):
            pass
    except OSError as e:
        raise (e)


def get_working_dir() -> str:
    working_dir = os.getenv("NJINN_WORKER_WORKINGDIR")
    if working_dir:
        try:
            prepare_path(working_dir)
        except OSError as e:
            raise (e)

        return working_dir

    return os.path.dirname(os.path.realpath(__file__))


def get_pid_dir() -> Path:
    return Path(get_working_dir()) / "pids"


class ProcessTerminator:
    def __init__(self):
        self._kill_by: datetime = None
        self._proc: Popen = None

    def check(self):
        if (
            self._kill_by is not None
            and self._kill_by <= datetime.now()
            and self._proc.poll() is None
        ):
            try:
                pg = os.getpgid(self._proc.pid)
                log.info(
                    "Killing process group %s of action process %s still running after SIGTERM.",
                    pg,
                    self._proc.pid,
                )
                os.killpg(pg, 9)
            except Exception as e:
                log.info(
                    "Failed to kill action process %s: %s",
                    self._proc.pid,
                    e,
                    exc_info=e,
                )
            self._kill_by = None
            self._proc = None

    def terminate_then_kill(self, proc: Popen, kill_by: datetime):
        """Tries to terminate proc via SIGTERM (linux)
        and kill its process group if it is still running by kill_by.

        Args:
            proc (Popen): [description]
            kill_by (datetime): [description]
        """

        action = "Terminating" if is_windows() else "Killing"
        log.info(f"{action} action process {proc.pid} after timeout or cancel.")

        proc.terminate()

        log.info("Terminated action process %s after timeout or cancel.", proc.pid)

        if not is_windows():
            # on Windows, terminate() and kill() are equivalent
            # on Linux, we schedule a SIGKILL if the process is still runnign
            assert kill_by is not None and proc is not None
            self._kill_by = kill_by
            self._proc = proc


def read_stdout(proc: Popen, lines: list, process_terminator: ProcessTerminator = None):
    """Reads all remaining stdout"""
    # ensure finite memory use
    all_lines = collections.deque([], 1000000)
    buffer = []
    if proc and proc.stdout:
        while True:
            line = proc.stdout.readline()
            if process_terminator is not None:
                process_terminator.check()
            if not line and proc.poll() is not None:
                break
            log.debug("Action stdout: %s", line.rstrip())
            # under windows, there is a timing issue with poll() that can cause us
            # to append many empty lines at the end
            # We avoid this without truncating empty lines in the middle of the output by only
            # adding to lines when current line is nonempty.
            if line.strip():
                if buffer:
                    all_lines.extend(buffer)
                    buffer.clear()
                all_lines.append(line)
            else:
                buffer.append(line)
    lines.extend(all_lines)
    return None


# 24h is also equal to the maximum task timeout
MAXIMUM_API_REQUEST_RETRY_DURATION_SECONDS = 24 * 3600
# max. 5 minutes between attempts
MAXIMUM_API_REQUEST_WAIT_TIME_SECONDS = 300


def api_response_predicate(r):
    """
    Currently, we retry on
    502 Bad Gateway
    503 Service Unavailable
    504 Gateway Timeout
    """

    return r.status_code in [502, 503, 504]


def setup_backoff_handler(handler=None):
    bl = logging.getLogger("backoff")
    if len([h for h in bl.handlers if not isinstance(h, logging.NullHandler)]) == 0:
        if handler is None:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "[%(asctime)s %(levelname)s/%(threadName)s] %(name)s: %(message)s"
            )
            handler.setFormatter(formatter)
        logging.getLogger("backoff").addHandler(handler)


def truncated(action_output, message):
    truncated_output = action_output.copy()
    first_lines = "\n".join(action_output["log"][:1000].split("\n")[:-1])
    last_lines = "\n".join(action_output["log"][-1000:].split("\n")[1:])
    truncated_log = (
        message
        + " - Truncated version:\n\n"
        + first_lines
        + "\n...(output omitted here)...\n"
        + last_lines
    )
    truncated_output["log"] = truncated_log
    return truncated_output


@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_value=MAXIMUM_API_REQUEST_WAIT_TIME_SECONDS,
    max_time=MAXIMUM_API_REQUEST_RETRY_DURATION_SECONDS,
)
@backoff.on_predicate(
    backoff.expo,
    api_response_predicate,
    max_value=MAXIMUM_API_REQUEST_WAIT_TIME_SECONDS,
    max_time=MAXIMUM_API_REQUEST_RETRY_DURATION_SECONDS,
)
def report_action_result(
    njinn_api,
    action_output: dict,
    action_context,
    result_url="/api/v1/workercom/results",
):
    """
    Report action result of the task to the Njinn API.
    """

    config = njinn_api.config
    action_output["context"] = action_context
    if not "state_info" in action_output and "state" in action_output:
        action_output["state_info"] = action_output["state"]

    action_output["worker"] = config.worker_name

    loggable_output = action_output
    if "log" in loggable_output and len(action_output["log"]) > 10000:
        loggable_output = truncated(action_output, "Log too long for logging")

    log.info(f"Calling {result_url} with action output {json.dumps(loggable_output)}")

    r = njinn_api.put(result_url, json=action_output)
    if r.status_code == 413:
        if action_output["log"]:
            log.warning("Request too large, trying with a truncated log")
            r = njinn_api.put(result_url, json=truncated(action_output, "Log too long"))

    log.info(f"Response: {r.status_code} {r.text}")
    return r


class add_sys_path:
    """
    Temporarily append `path` arg to `sys.path`.
    """

    # https://stackoverflow.com/a/39855753
    def __init__(self, path: str):
        self.path = path

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, *args, **kwargs):
        try:
            sys.path.remove(self.path)
        except ValueError:
            pass


@contextlib.contextmanager
def change_working_directory(path: str):
    """
    Changes current working directory to specified path.
    Makes the directory if it does not exist.
    """
    prev_cwd = os.getcwd()

    os.makedirs(path, exist_ok=True)

    log.debug("Changing working directory to: %s", path)
    os.chdir(path)
    try:
        yield
    finally:
        log.debug("Changing working directory back to: %s", prev_cwd)
        os.chdir(prev_cwd)
