#!/usr/bin/env python

"""
A set of useful tools.
"""

import os
import shutil
import sys

from loguru import logger

LOG_FORMAT = '<light-green>[{time:HH:mm:ss}]</light-green> <level>{message}</level>'
LOG_LEVEL = 'TRACE'

logger.remove()
logger.add(sys.stderr, format=LOG_FORMAT, level=LOG_LEVEL)


def trace(s): logger.info(s) if s else ''
def debug(s): logger.debug(s) if s else ''
def info(s): logger.info(s) if s else ''
def success(s): logger.success(s) if s else ''
def warning(s): logger.warning(s) if s else ''
def error(s): logger.error(s) if s else ''
def critical(s): logger.critical(s) if s else ''


def error_and_exit(msg, code=1):
    """
    Logging an error message and exit with an exit code.
    
    :param msg: str, an error message.
    :param code: int, an exit code.
    """
    
    error(msg)
    sys.exit(code)
    
    
def mkdir(path):
    """
    Make a directory or exit on error.
    
    :param path: str, path to directory needs to be created.
    :return: str, path to a directory.
    """
    
    if not path:
        error_and_exit('Path for mkdir must be a non-empty string.')
    if not isinstance(path, str):
        error_and_exit(f'Path {path} for mkdir is not a string.')
    try:
        os.mkdir(path)
    except FileExistsError:
        debug(f'Directory {path} already exist.')
    except OSError as e:
        error_and_exit(f'{e}, create directory failed!')
    return path
    
    
def touch(path, overwrite=False):
    """
    Touch a empty file or exit on error.
    
    :param path: str, path to a file needs to be created.
    :param overwrite: bool, whether to overwrite an existing file.
    :return: str, path to a file.
    """
    
    if not path:
        error_and_exit('Path for touch must a be non-empty string.')
    if not isinstance(path, str):
        error_and_exit(f'Path {path} for touch is not a string.')
    if os.path.isfile(path):
        if overwrite:
            try:
                with open(path, 'w') as o:
                    o.write('')
            except OSError as e:
                error_and_exit(f'{e}, touch file (overwrite existing file) failed!')
        else:
            logger.debug(f'File {path} already exists and did not overwrite.')
    else:
        try:
            with open(path, 'w') as o:
                o.write('')
        except OSError as e:
            error_and_exit(f'{e}, touch file failed!')
    return path


def rm(path, exit_on_error=True):
    """
    Delete a path (to a file or directory).
    
    :param path: str, path to a file or directory needs to be deleted.
    :param exit_on_error: bool, whether to exit on error of deleting.
    :return: None
    """
    
    if not path:
        error_and_exit('Path for rm must be a non-empty string.')
    if not isinstance(path, str):
        error_and_exit(f'Path {path} for rm is not a string.')
    if os.path.exists(path):
        try:
            os.unlink(path)
        except IsADirectoryError:
            try:
                shutil.rmtree(path)
            except Exception as e:
                error(f'{e}, delete directory failed!')
                if exit_on_error:
                    sys.exit(1)
        except OSError as e:
            error(f'{e}, delete file failed!')
            if exit_on_error:
                sys.exit(1)
    else:
        debug(f"No such file or directory '{path}', delete file or directory aborted!")
        
        
def equal_len_lists(l1, l2, msg='', exit_if_unequal=True):
    """
    Check if two lists consist of same number of elements.
    
    :param l1: list, the first list.
    :param l2: list, the second list.
    :param msg: str, error message if two list consists of unequal number of elements.
    :param exit_if_unequal: bool, whether to exit on two list consists of unequal number of elements.
    :return: boo, True or False for equal or unequal number of elements, respectively.
    """
    
    equal = len(l1) == len(l2)
    if not equal:
        error(msg)
        if not exit_if_unequal:
            sys.exit(1)
    return equal
            

if __name__ == '__main__':
    pass
