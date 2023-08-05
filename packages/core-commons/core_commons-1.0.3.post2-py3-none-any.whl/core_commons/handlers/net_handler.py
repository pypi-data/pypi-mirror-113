# IPV4 and IPV6 Regex by (https://gist.github.com/dfee/6ed3a4b05cfe7a6faf40a2102408d5d8)

import re
import socket

from core_commons.handlers.command_handler import run_command

IPV4_SEG = r'(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])'
CIDR = r'/(?:3[0-2]|[0-2][0-9])'
IPV4_ADDR = r'(?:(?:' + IPV4_SEG + r'\.){3,3}' + IPV4_SEG + r')'
IPV4_ADDR_CIDR = r'(?:(?:' + IPV4_ADDR + r')' + CIDR + r')'

IPV6_SEG = r'(?:(?:[0-9a-fA-F]){1,4})'
IPV6_GROUPS = (
    r'(?:' + IPV6_SEG + r':){7,7}' + IPV6_SEG,
    r'(?:' + IPV6_SEG + r':){1,7}:',
    r'(?:' + IPV6_SEG + r':){1,6}:' + IPV6_SEG,
    r'(?:' + IPV6_SEG + r':){1,5}(?::' + IPV6_SEG + r'){1,2}',
    r'(?:' + IPV6_SEG + r':){1,4}(?::' + IPV6_SEG + r'){1,3}',
    r'(?:' + IPV6_SEG + r':){1,3}(?::' + IPV6_SEG + r'){1,4}',
    r'(?:' + IPV6_SEG + r':){1,2}(?::' + IPV6_SEG + r'){1,5}',
    IPV6_SEG + r':(?:(?::' + IPV6_SEG + r'){1,6})',
    r':(?:(?::' + IPV6_SEG + r'){1,7}|:)',
    r'fe80:(?::' + IPV6_SEG + r'){0,4}%[0-9a-zA-Z]{1,}',
    r'::(?:ffff(?::0{1,4}){0,1}:){0,1}[^\s:]' + IPV4_ADDR,
    r'(?:' + IPV6_SEG + r':){1,4}:[^\s:]' + IPV4_ADDR,
)
IPV6_ADDR = '|'.join(['(?:{})'.format(g) for g in IPV6_GROUPS[::-1]])


def check_ipv4(addr):
    """
    Checks if address is a valid IPV4 address.

    :param str addr: The address to check.
    :return: True, if the address is a valid IPV4 address. False otherwise.
    :rtype: bool
    """
    return __check_valid(IPV4_ADDR, addr)


def check_ipv4_cidr(addr):
    """
    Checks if address is a valid IPV4 address with CIDR.

    :param str addr: The address to check.
    :return: True, if the address is a valid IPV4 address with CIDR. False otherwise.
    :rtype: bool
    """
    return __check_valid(IPV4_ADDR_CIDR, addr)


def check_ipv6(addr):
    """
    Checks if address is a valid IPV6 address.

    :param str addr: The address to check.
    :return: True, if the address is a valid IPV6 address. False otherwise.
    :rtype: bool
    """
    return __check_valid(IPV6_ADDR, addr)


def resolve_addr(to_resolve):
    """
    Resolves an IP address or host name from the default system DNS.

    :param to_resolve: The IP address or hostname to resolve.
    :return: The resolved hostname, a list of host name aliases, and a list of IP addresses that were resolved.
    :rtype: str, list[str], list[str]
    """
    try:
        if re.search(IPV4_ADDR, to_resolve) or re.search(IPV6_ADDR, to_resolve):
            return socket.gethostbyaddr(to_resolve)
        else:
            ip_addr = socket.gethostbyname(to_resolve)
            return socket.gethostbyaddr(ip_addr)
    except (socket.herror, socket.gaierror):
        return "UNKNOWN HOST", [], []


def resolve_addr_dns(to_resolve, dns):
    """
    Resolves an IP address or host name using the specified DNS address.

    :param str to_resolve: The IP address or hostname to resolve.
    :param str dns: The IP address or hostname of the DNS to use when resolving.
    :return: The resolved hostname, and a list of IP addresses that were resolved.
    :rtype: str, list[str]
    """
    # Execute the lookup command.
    command = ["nslookup", to_resolve, dns]
    output = __execute_and_get_output(command)

    # Retrieve the name from the command output if it exists.
    name_match_es = re.search(r"Nombre:\s+([^\s]+)", output)
    name_match_en = re.search(r"Name:\s+([^\s]+)", output)
    name_match = name_match_es or name_match_en
    resolved_name = name_match.group(1) if name_match else "UNKNOWN HOST"

    # Retrieve the name from the command output if it exists.
    ipv4_address_match = re.findall(IPV4_ADDR, output)
    ipv6_address_match = re.findall(IPV6_ADDR, output)
    resolved_addresses = set()
    resolved_addresses.update(ipv4_address_match)
    resolved_addresses.update(ipv6_address_match)
    if dns in resolved_addresses:
        resolved_addresses.remove(dns)

    # Return the resolved name and addresses.
    return resolved_name, resolved_addresses


def __check_valid(regex, item):
    """
    Auxiliary method that returns true if item

    :param str regex: Regex string to test against the item.
    :param str item: Item to test.
    :return: True, if the item matches the regex. False otherwise.
    :rtype: bool
    """
    match = re.search(regex, item)
    return match.group() == item if match is not None else False


def __execute_and_get_output(command):
    """
    Executes a local command with set timeout and returns the output.

    :param str or list[str] command: The command to execute
    :return: The output from the command
    :rtype: str
    :raises OSError: If timeout is triggered or command exit code is not 0.
    """
    exit_code, output, error = run_command(command, timeout=10)
    if exit_code is not None and exit_code != 0:
        raise OSError("Bad command execution. \"%s\" returned exit code %s.\n"
                      "STDOUT:\n%s\nSTDERR:\n%s" % (command, exit_code, output, error))
    else:
        return output
