import os
import shutil
import sys

import click

from worker import shared_logging

# use absolute paths to be consistent & compatible bewteen worker code and the scripts
from worker.config import get_config_path
from worker.njinnworker import NjinnWorker
from worker.utils import get_working_dir


@click.command()
@click.option("-a", "--api", "api", help="Njinn API url.")
@click.option(
    "--clear-packs",
    "clear_packs",
    is_flag=True,
    help="Remove all packs and environments",
)
@click.option(
    "--no-default-queues",
    "no_default_queues",
    is_flag=True,
    help="Don't join default queues during registration (no effect after registration).",
)
@click.option(
    "--configure-systemd",
    "configure_systemd",
    is_flag=True,
    help="A helper script to aid in the installation of a systemd service unit file.",
)
@click.argument("token", required=False)
def main(
    api=None,
    clear_packs=False,
    token=None,
    no_default_queues=False,
    configure_systemd=False,
):
    if configure_systemd:
        from subprocess import call

        parent_dir = os.path.dirname(os.path.realpath(__file__))
        install_script_path = os.path.join(parent_dir, "install.sh")
        call(install_script_path)
        return
    # windows celery fix: https://github.com/celery/celery/issues/4081
    os.environ["FORKED_BY_MULTIPROCESSING"] = "1"
    os.environ["GIT_TERMINAL_PROMPT"] = "0"
    if clear_packs:
        base_path = get_working_dir()
        for subdirectory_name in ["bundle_status", "packs", "venv"]:
            subdirectory = os.path.join(base_path, subdirectory_name)
            if os.path.exists(subdirectory):
                print("Deleting", os.path.abspath(subdirectory))
                shutil.rmtree(subdirectory)
    njinn_url = sys.argv[-2] if len(sys.argv) > 2 else os.getenv("NJINN_URL")
    registration_token = token or os.getenv("NJINN_WORKER_TOKEN")
    print("Config file:", get_config_path())
    shared_logging.initialize()
    worker = NjinnWorker(
        registration_token=registration_token,
        njinn_url=njinn_url,
        no_default_queues=no_default_queues,
    )
    print("Working Directory:", worker.working_dir)
    print("PID File:", worker.config.pidfile)
    worker.start()


if __name__ == "__main__":
    main()
