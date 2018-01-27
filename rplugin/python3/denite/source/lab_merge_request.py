import re
import subprocess

from .base import Base


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'lab_merge_request'
        self.kind = 'lab_browse'

    def on_init(self, context):
        print('on_init')

    def on_close(self, context):
        print('on_close')

    def gather_candidates(self, context):
        command = ['lab', 'merge-request']
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
            return []

        candidates = []
        for value in [value for value in output.split('\n') if len(value) > 0]:
            splits = re.split(" +", value, maxsplit=1)
            iid = splits[0]
            candidates.append({
                'word': iid,
                'abbr': value,
            })
        return candidates
