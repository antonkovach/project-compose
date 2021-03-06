import datetime
import git
import os
import yaml
from .console_logger import ColorPrint


class FileUtils:

    @staticmethod
    def make_empty_file(directory, file):
        file = os.path.join(directory, file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(file):
            with open(file, 'w') as stream:
                stream.write(" ")

    @staticmethod
    def make_empty_file_with_empty_dict(directory, file):
        file = os.path.join(directory, file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(file):
            with open(file, 'w') as stream:
                content = dict()
                stream.write(yaml.dump(data=content, default_flow_style=False))

    @staticmethod
    def write_compose_log(directory, project, data):
        file = os.path.join(directory, project + "-" + datetime.datetime.now().strftime("%Y.%m.%d-%H-%M-%S") + ".log")
        if not os.path.exists(file):
            with open(file, 'w') as stream:
                stream.write(str(data))

    @staticmethod
    def get_directory_name():
        return os.path.basename(os.getcwd())

    @staticmethod
    def get_relative_path(base_path, target_path):
        return os.path.relpath(path=target_path, start=os.path.commonprefix([target_path, base_path])) + "/"

    @staticmethod
    def get_normalized_dir(target_dir):
        if target_dir is not None:
            if not os.path.exists(target_dir):
                if os.path.exists(os.path.join(os.getcwd(), target_dir)):
                    target_dir = os.path.join(os.getcwd(), target_dir)
                else:
                    ColorPrint.exit_after_print_messages(message="Directory not exists: " + target_dir)
        else:
            target_dir = os.getcwd()
        if not os.path.isdir(target_dir):
            ColorPrint.exit_after_print_messages(message=target_dir + " is not a directory")

        return os.path.normpath(target_dir)

    @staticmethod
    def get_git_repo(base_dir):
        if not os.path.isdir(base_dir):
            ColorPrint.exit_after_print_messages(message="Target directory is not a valid git repository: "
                                                         + base_dir)
        try:
            repo = git.Repo(base_dir)
            return repo, base_dir
        except git.exc.InvalidGitRepositoryError as exc:
            if base_dir == os.path.dirname(base_dir):
                ColorPrint.exit_after_print_messages(message="Target directory or parents are"
                                                             " not a valid git repository")
            return FileUtils.get_git_repo(os.path.dirname(base_dir))

