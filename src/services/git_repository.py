import os
import git
import shutil
from .abstract_repository import AbstractRepository
from .console_logger import ColorPrint


class GitRepository(AbstractRepository):

    def __init__(self, target_dir, url, branch, git_ssh_identity_file=None, force=False):
        super(GitRepository, self).__init__(target_dir)
        self.branch = branch
        try:
            if url is None:
                ColorPrint.exit_after_print_messages(message="GIT URL is empty")
            if git_ssh_identity_file is None:
                git_ssh_identity_file = os.path.expanduser("~/.ssh/id_rsa")
            with git.Git().custom_environment(GIT_SSH=git_ssh_identity_file):
                if not os.path.exists(target_dir) or not os.listdir(target_dir):
                    self.repo = git.Repo.clone_from(url=url, to_path=target_dir)
                else:
                    self.repo = git.Repo(target_dir)
                    old_url = self.repo.remotes.origin.url
                    if old_url != url:
                        shutil.rmtree(target_dir)
                        self.repo = git.Repo.clone_from(url=url, to_path=target_dir)
                self.set_branch(branch=branch, force=force)
        except git.GitCommandError as exc:
            ColorPrint.exit_after_print_messages(message=exc.stderr)

    def get_branches(self):
        return self.repo.branches

    def set_branch(self, branch, force):
        try:
            if branch not in self.repo.branches and branch == 'master':
                '''Make init commit'''
                self.repo.index.add(["*"])
                self.repo.index.commit("init")
                remote = self.repo.create_remote('master', self.repo.remotes.origin.url)
                remote.push(refspec='{}:{}'.format(self.repo.active_branch, 'master'))
            if str(self.repo.active_branch) != branch:
                self.repo.git.checkout(branch, force=force)
            else:
                self.pull()
        except git.GitCommandError as exc:
            ColorPrint.exit_after_print_messages(message=exc.stderr)

    def push(self):
        if self.repo is None:
            ColorPrint.exit_after_print_messages(message="It is not an git repository: " + self.target_dir)
        if self.repo.is_dirty(untracked_files=True):
            self.repo.index.add(["*"])
            self.repo.index.commit("Change from project-compose")
            self.repo.git.push()

    def pull(self):
        if self.repo is None:
            ColorPrint.exit_after_print_messages(message="It is not an git repository: " + self.target_dir)
        ColorPrint.print_with_lvl(message="Repository " + self.repo.remotes.origin.url + " with "
                                          + str(self.repo.active_branch) + " branch pull response:", lvl=1)
        ColorPrint.print_with_lvl(message=self.repo.git.pull(), lvl=1)

    def get_actual_branch(self):
        return str(self.repo.active_branch)
