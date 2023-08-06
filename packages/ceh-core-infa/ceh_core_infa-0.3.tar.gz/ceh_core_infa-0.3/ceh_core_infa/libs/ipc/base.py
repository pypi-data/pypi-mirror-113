from .descriptors.descriptors import (
    ValidateIPCParam,
    ValidatePathIPCClient,
    ValidatePathParams
)

from ...config import (
    IPC_CLIENT_FOLDER,
    IPC_LOGIN,
    IPC_PASSWORD,
)


class IPCBase:
    main_path = ValidatePathIPCClient()
    user = ValidateIPCParam()
    password = ValidateIPCParam()
    local_paramfile = ValidatePathParams()
    main_path = ValidatePathParams()

    def __init__(
            self,
            service: str,
            domain: str,
            folder: str,
            instance: str,
            wait: str,
            user: str = IPC_LOGIN,
            password: str = IPC_PASSWORD,
            main_path: str = IPC_CLIENT_FOLDER,
            paramfile: str = None,
            local_paramfile: str = None,
            timeout: int = None,
            provide_full_log: bool = False,
    ):
        self.main_path = main_path
        self.user = user
        self.password = password
        self.service = service
        self.domain = domain
        self.folder = folder
        self.instance = instance
        self.timeout = timeout
        self.provide_full_log = provide_full_log
        self.wait = wait
        self.paramfile = paramfile
        self.local_paramfile = local_paramfile
        self.__main_cmd = None
