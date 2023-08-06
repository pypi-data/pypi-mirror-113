import os

from typing import List, Dict, Union, Iterator, Optional
from subprocess import Popen, PIPE, STDOUT

from .base import IPCBase
from .exceptions.exceptions import IPCException, BashException


class IPCLauncher(IPCBase):
    __association = {
        'user': '-u',
        'password': '-p',
        'service': '-sv',
        'domain': '-d',
        'folder': '-f',
        'timeout': '-t',
        'instance': '-rin',
        'wait': '-wait',
        'paramfile': '-paramfile',
        'local_paramfile': '-lpf',
    }

    __cmd = 'startworkflow'

    __system_info = {
        'run_id': None,
        'workflow': None,
        'status': None,
    }

    valid_log = None

    def __generate_cmd(self) -> str:
        """Generating a command to run pmcmd"""
        cmd = '%s %s' % (self.main_path, self.__cmd)
        cmd_end = ''

        for attr in self.__dict__:
            if self.__getattribute__(attr) and attr in self.__association:
                if attr == 'wait':
                    cmd_end += ' %s %s' % (
                        self.__association.get(attr, ''),
                        self.__getattribute__(attr)
                    )
                else:
                    cmd += ' %s %s' % (
                        self.__association.get(attr, ''),
                        self.__getattribute__(attr)
                    )
        cmd += cmd_end

        return cmd

    def __fill_system_info(
            self,
            logs: List[Union[str, List[Optional[Union[int, str]]]]]
    ) -> None:
        """Collecting system parameters from stream logs"""
        logs = filter(
            lambda x: not len(x[0]) == 0,
            logs
        )

        logs = list(logs)

        for log in logs:
            if 'successfully' in log[0]:
                line = log[0].split()
                for i in range(len(line)):
                    if line[i] == 'id':
                        self.__system_info['run_id'] = int(line[i + 1][1:len(line[i + 1]) - 1])
                    if line[i] == 'Workflow':
                        self.__system_info['workflow'] = line[i + 1]
            elif 'INFO' == log[0]:
                self.__system_info['status'] = log[2][:-1].strip()

        if self.provide_full_log:
            self.__system_info['log'] = logs
            self.__system_info['cmd'] = self.__main_cmd

    @staticmethod
    def __search_error(logs):
        errors = ('WARNING', 'ERROR')

        for log in logs:
            if log[0] in errors:
                if len(log) == 3:
                    err = '{} {}'.format(log[1], log[2])
                else:
                    err = log[1] if log[0] == errors[1] else log[2]

                raise IPCException(err)

            if len(log) >= 2:
                if 'error' in log[1]:
                    err = ' '.join(log)

                    raise IPCException(err)

    @staticmethod
    def __get_valid_response(logs: Iterator[bytes]) -> List[str]:
        """We get only the parameters of stream"""

        lines = list()
        for raw_line in logs:
            line = raw_line.decode('utf-8').rstrip()

            line = line.split(': ')

            lines.append(line)

        return lines

    @staticmethod
    def __get_env(env: Dict[str, Union[int, str]]) -> Dict[str, str]:
        if env is None:
            env = os.environ.copy()

        return env

    def get_system_info(self):
        return self.__system_info

    def launch_workflow(
            self,
            env: Dict[str, Union[int, str]] = None
    ) -> None:

        env = self.__get_env(env)
        self.__main_cmd = self.__generate_cmd()
        print(self.__main_cmd)
        proc = Popen(
            ['bash', '-c', self.__main_cmd],
            stdout=PIPE,
            stderr=STDOUT,
            env=env
        )

        raw_log = iter(proc.stdout.readline, b'')

        self.valid_log = self.__get_valid_response(logs=raw_log)

        self.__fill_system_info(logs=self.valid_log)

        self.__search_error(logs=self.valid_log)

        if proc.returncode:
            raise BashException("Bash command failed")
