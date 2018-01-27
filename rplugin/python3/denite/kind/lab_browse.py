import subprocess

from .base import Base


class Kind(Base):
    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'lab_browse'
        self.default_action = 'lab_browse'

    def action_lab_browse(self, context):
        for target in context['targets']:
            iid = target['word']

        command = ['lab', 'browse', iid]
        process = subprocess.Popen(command,
                                   cwd=context['path'],
                                   universal_newlines=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        try:
            output, err_output = process.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            process.kill()
            output, err_output = process.communicate()
        exit_code = process.returncode

        if exit_code != 0:
            print('error')
