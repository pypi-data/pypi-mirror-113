import os
import xml.etree.ElementTree as et

from typing import Union, Dict, List, Tuple

from ceh_core_infa.config import (
    IPC_HOST,
    IPC_PORT,
    SYSTEM_FOLDER,
    TEMPLATE_DOMAIN,
    INFA_DOMAINS_FILE,
    IPC_DOMAIN
)


def _check_for_file_availability(path: str) -> bool:
    if not os.path.exists(path):
        return False
    return True


def _parse_domain_ipc(path: str) -> Union[Dict[str, List], None]:
    tree = et.parse(path)

    host_obj = tree.findall('.//host')
    port_obj = tree.findall('.//port')
    domain_obj = tree.findall('.//domainName')

    if not host_obj or not port_obj or not domain_obj:
        return

    return {'host': host_obj, 'port': port_obj, 'domain': domain_obj}


def _search_current_value(data, value) -> bool:
    tmp = list(filter(lambda x: x.text == value, data))

    if len(tmp) > 0:
        return True
    return False


def _create_file_parameters(
        params: Tuple[Union[str, int], ...],
        path: str,
        dft_fld: str = SYSTEM_FOLDER,
        domain: str = TEMPLATE_DOMAIN,
        template_name: str = 'ipc_domain.infa'
):
    with open(f'{dft_fld}{domain}/{template_name}') as ptr:
        txt = ptr.read() % params
        with open(path, 'w') as tmp:
            tmp.write(txt)


def rebuild_domain_ipc(path_domain_file: str = INFA_DOMAINS_FILE):
    check_path = _check_for_file_availability(path_domain_file)

    if check_path:
        parse_result = _parse_domain_ipc(path_domain_file)
        if parse_result:
            result = all(
                [
                    _search_current_value(parse_result['host'], IPC_HOST),
                    _search_current_value(parse_result['port'], str(IPC_PORT)),
                    _search_current_value(parse_result['domain'], IPC_DOMAIN)
                ]
            )
            if not result:
                _create_file_parameters(
                    (IPC_DOMAIN, IPC_HOST, IPC_PORT), path_domain_file
                )
        else:
            _create_file_parameters(
                (IPC_DOMAIN, IPC_HOST, IPC_PORT), path_domain_file
            )
    else:
        _create_file_parameters(
            (IPC_DOMAIN, IPC_HOST, IPC_PORT), path_domain_file
        )
