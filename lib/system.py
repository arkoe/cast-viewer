import requests
import re
import pytz
import sys
import sh

def get_status():
    throttled = get_throttled()
    return {
        'version': get_git_tag(),
        'throttled': throttled,
        'is_under_voltage': is_under_voltage(throttled),
        'temp': vcgencmd('measure_temp').rstrip().replace('temp=', ''),
        'firmware': vcgencmd('version').split('\n'),
        'cec': [i for i in sh.cec_client('-s', d=1, _in='pow 0').split('\n') if i][-1]
    }

def vcgencmd(command):
    return sh.vcgencmd(command).rstrip()

def get_throttled():
    return vcgencmd('get_throttled').replace('throttled=', '')

def is_under_voltage(throttled=None):
    if throttled is None:
        throttled = get_throttled()

    return throttled in ['0x50005', '0x50000']

def get_git_tag():
    commit = sh.git("rev-list", "--tags", "--max-count=1").rstrip()
    return sh.git("describe", "--tags", commit).rstrip()