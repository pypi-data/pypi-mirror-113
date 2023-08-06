import platform
import psutil


def os_platform():
    """
    This function will return current operating system name
    :return:
    """
    return platform.system()


def ram_usage(process_id):
    """
    get RAM usage os selected process
    :return:
    """
    return psutil.virtual_memory()[2]


def cpu_usage(process_id):
    """
    get CPU usage os selected process
    :return:
    """
    return psutil.Process(process_id).cpu_percent()


def disc_usages(path):
    """
    get Disk Usages
    path  = "/"
    :return:
    """
    return psutil.disk_usage(path)
