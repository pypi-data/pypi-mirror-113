import subprocess
import threading


def run_command(command, working_directory=None, timeout=None):
    """
    Executes a command and waits for the output

    :param str or list[str] command: Command in compact or expanded form.
    :param str working_directory: The working directory for the command line execution.
    :param str working_directory: The working directory for the command line.
    :param float or None timeout: Optional timeout for the command.
    :return: The command return code and output or None if timeout was triggered.
    :rtype: (int, str) or None
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_directory)
    output = {}

    def get_command_output():
        output["stdout"] = process.stdout.read()
        output["stderr"] = process.stderr.read()
        process.terminate()
        output["return_code"] = process.returncode

    thread = threading.Thread(target=get_command_output)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        process.terminate()
        thread.join()
        raise OSError("Timeout triggered on command \"%s\"" % command)
    else:
        return output["return_code"], output["stdout"], output["stderr"]
