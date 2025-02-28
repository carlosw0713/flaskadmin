# -*- coding: utf-8 -*-
"""
Author: <carlos>
Email: <carlos.w.0713@outlook.com>
Date: 2024/12/26
Description: <Brief description of the file>
"""

import json
import time
from datetime import datetime

from common.Logger import logger
from quickfaas.global_dict import get_global_parameter
from quickfaas.remotebus import publish

gwsn = get_global_parameter()

zero_kWhPEPA = 0
allow_change_zero_kWhPEPA = True

def main(message, wizard_api):
    global zero_kWhPEPA
    global allow_change_zero_kWhPEPA

    mess={
        "ver": "1.0",
        "msgId": SnowFlake(message['timestamp']) * -1,
        "ts": message['timestamp'],
        "data": {}
        }

    for device, measures in message["values"].items():
        mess["data"][device]={}
        for measure, value in measures.items():
            mess["data"][device][measure] = value["raw_data"]

        if ("kWhPEPA" in set(mess["data"][device].keys())) and ("DkWh" not in set(mess["data"][device].keys())):
            time_date = datetime.fromtimestamp(message['timestamp'])
            if (time_date.hour == 0) and (time_date.minute == 0):
                if allow_change_zero_kWhPEPA:
                    zero_kWhPEPA = mess["data"][device]["kWhPEPA"]
                    allow_change_zero_kWhPEPA = False
            else:
                allow_change_zero_kWhPEPA = True
            mess["data"][device]["DkWh"] = mess["data"][device]["kWhPEPA"] - zero_kWhPEPA
    logger.info(mess)
    publish(__topic__, json.dumps(mess), __qos__,cloud_name="MQTT云服务")
    # publish(__topic__, json.dumps(mess), __qos__)


def SnowFlake(time_a):
    twepoch = 1640966400000
    currentSequence = 0
    timestampOffset = 22
    machineID_IMEI=gwsn["SN"]
    if len(machineID_IMEI) > 12:
        machineID_IMEI = machineID_IMEI[-12:]
    machineIDOffset = 12
    timestamp = time_a
    return (((timestamp - twepoch) << timestampOffset) | (int(machineID_IMEI) << machineIDOffset) | currentSequence)
