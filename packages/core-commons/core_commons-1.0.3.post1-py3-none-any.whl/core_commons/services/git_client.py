import os

from core_commons.handlers import command_handler


class GitClient:
    """Basic client to clone, update or upload a git repository."""

    def __init__(self, local_path, repo_path="", repo_user="", repo_password=""):
        """
        Ensures that the repository is downloaded and updated, by updating or cloning it.

        :param str local_path: The folder where the repo will be cloned or updated.
        :param str repo_path: The scheme, host and path to the remote git repository.
        :param str repo_user: The username to use when connecting to the repository.
        :param str repo_password: The password to use when connecting to the repository.
        """
        self.local_path = local_path
        self.repo_path = repo_path
        self.repo_user = repo_user
        self.repo_pass = repo_password
        self.repo_url = self.__get_repository_url(repo_path, repo_user, repo_password)

    def update_or_clone_from_repository(self):
        """Tries to update the repository if it exists. If not, clones it."""
        if os.path.exists(self.local_path) and os.path.exists(self.local_path.rstrip("/") + "/.git"):
            self.__execute_command("git pull")
        else:
            self.__execute_command("git clone %s %s" % (self.repo_url, self.local_path), from_repo=False)

    def discard_changes_and_reset(self):
        """Discards tracked and untracked file changes, pruning the repository and resetting it to the last commit."""
        self.__execute_command("git reset --hard")
        self.__execute_command("git clean -fdx")

    def upload_to_repository(self, message):
        """
        Uploads the current state of the local repository to the remote. Assumes no collisions or errors from git.

        :param str message: The commit message. Should never be empty string.
        """
        self.__execute_command("git add .")
        self.__execute_command("git commit --allow-empty -m \"%s\"" % message)
        self.__execute_command("git push")

    def __execute_command(self, command, from_repo=True):
        """
        Executes a git command on the git repository folder. Raises an error if exit code is not 0.

        :param str command: The command to execute.
        :param bool from_repo: If set, the command will be executed from the local repository folder.
        :raises OSError: If command was not successful.
        """
        working_dir = self.local_path if from_repo else None
        exit_code, stdout, stderr = command_handler.run_command(command, working_directory=working_dir)
        if exit_code != 0:
            raise OSError("Could not execute Git command \"%s\". Returned with exit code %i."
                          "\nSTDOUT:\n%s\nSTDERR:\n%s" % (command, exit_code, stdout, stderr))

    @staticmethod
    def __get_repository_url(repository_path, repository_user, repository_password):
        """
        Returns a valid and authenticated repository url.

        :param str repository_path: The host and path of the repository.
        :param str repository_user: The user to use when connecting to the repository.
        :param str repository_password: The password to use when connecting to the repository.
        :return: The formatted and authenticated git url.
        :rtype: str
        """
        if "//" not in repository_path:
            return None

        scheme = repository_path.split("//")[0]
        host_and_path = "//".join(repository_path.split("//")[1:])
        return "%s//%s:%s@%s" % (scheme, repository_user, repository_password, host_and_path)
