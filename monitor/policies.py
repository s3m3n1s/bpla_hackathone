from multiprocessing.resource_sharer import stop
import os
import threading
import time
from uuid import uuid4
from producer import proceed_to_deliver

ordering = False
UNIC_NAME_AUTH = uuid4().__str__()
UNIC_NAME_CAMERA = uuid4().__str__()
UNIC_NAME_FLY_CONTROL = uuid4().__str__()
UNIC_NAME_HW_CONTROLLER = uuid4().__str__()
UNIC_NAME_LIDAR = uuid4().__str__()
UNIC_NAME_MONITOR = uuid4().__str__()
UNIC_NAME_NAVIGATE_GLONAS = uuid4().__str__()
UNIC_NAME_NAVIGATE_INERTIAL = uuid4().__str__()
UNIC_NAME_NAVIGATE_GPS = uuid4().__str__()
UNIC_NAME_NAVIGATE_SPRAYER = uuid4().__str__()

err_resp_timout = 10

time_period = 60

rate_limit = { # messages per minute
    'default': 20,
    'advanced': 60
}

default_rules = {
    'sensor':{
        'send_to': ['fly_control'],
        'rate_limit': rate_limit['default'],
        'initiator': True,
        'data_type': ['data']
    },
    'actor':{
        'send_to': ['fly_control'],
        'rate_limit': rate_limit['default'],
        'initiator': False,
        'data_type': ['data']
    }
}

rules = {
    'auth': {
        'send_to': ['fly_control', 'connector'],
        'rate_limit': rate_limit['default'],
        'initiator': ['connector'],
        'data_type': ['data', 'ation']
    },
    'camera':{
        **default_rules['sensor'],
        'rate_limit': rate_limit['advanced']
    },
    'connector':{
        'send_to': ['auth'],
        'rate_limit': rate_limit['default'],
        'initiator': False
    },
    'fly_control':{
        'send_to': ['auth', 'sprayer'],
        'rate_limit': rate_limit['advanced'],
        'initiator': ['auth', 'sprayer'],
        'data_type': ['data', 'action']
    },
    'hw_control':{
        **default_rules['actor'],
        'recieve_from': ['sprayer'],
        'initiator': True
    },
    'lidar':{
        **default_rules['sensor'],
        'rate_limit': rate_limit['advanced']
    },
    'navigate_inertional':{
        **default_rules['sensor']
    },
    'navigate_glonas':{
        **default_rules['sensor']
    },
    'navigate_gps':{
        **default_rules['sensor']
    },
    'sprayer':{
        **default_rules['actor'],
        'send_to': ['hw_control']
    }
}

active_connections = {}

action_connections = {}

def error_msg(event_id):
    err_details = {
        "id": event_id,
        "operation": "internal_error",
        "deliver_to": "monitor",
        "source": UNIC_NAME_MONITOR
    }
    proceed_to_deliver(event_id, err_details)


def set_names(id):
    comm_out_details = {
        "id": id,
        "operation": "set_name",
        "deliver_to": "communication_out",
        "source": "",
        "name": UNIC_NAME_COMMUNICATION_OUT
    }
    proceed_to_deliver(id, comm_out_details)
    camera_details = {
        "id": id,
        "operation": "set_name",
        "deliver_to": "camera",
        "source": "",
        "name": UNIC_NAME_CAMERA
    }
    proceed_to_deliver(id, camera_details)
    central_details = {
        "id": id,
        "operation": "set_name",
        "deliver_to": "central",
        "source": "",
        "name": UNIC_NAME_CENTRAL
    }
    proceed_to_deliver(id, central_details)
    communication_details = {
        "id": id,
        "operation": "set_name",
        "deliver_to": "communication_IN",
        "source": "",
        "name": UNIC_NAME_COMMUNICATION_IN
    }
    proceed_to_deliver(id, communication_details)
    gps_details = {
        "id": id,
        "operation": "set_name",
        "deliver_to": "gps",
        "source": "",
        "name": UNIC_NAME_GPS
    }
    proceed_to_deliver(id, gps_details)
    motion_details = {
        "id": id,
        "operation": "set_name",
        "deliver_to": "motion",
        "source": "",
        "name": UNIC_NAME_MOTION
    }
    proceed_to_deliver(id, motion_details)
    position_details = {
        "id": id,
        "operation": "set_name",
        "deliver_to": "position",
        "source": "",
        "name": UNIC_NAME_POSITION
    }
    proceed_to_deliver(id, position_details)
    sensors_details = {
        "id": id,
        "operation": "set_name",
        "deliver_to": "sensors",
        "source": "",
        "name": UNIC_NAME_SENSORS
    }
    proceed_to_deliver(id, sensors_details)


def check_operation(event_id, details) -> bool:
    authorized = False
    # print(f"[debug] checking policies for event {id}, details: {details}")
    # print(f"[info] checking policies for event {id},"\
    #       f" {details['source']}->{details['deliver_to']}: {details['operation']}")

    src = details['source']
    dst = details['deliver_to']
    dtype = details['type']

    if src not in rules or dst not in rules:
        return False

    from_rule = rules[src]

    allowed_dtype = from_rule.get('data_type', True)
    if allowed_dtype != True:
        if allowed_dtype == False or allowed_dtype is None or dtype not in allowed_dtype:
            return False
    
    dest = from_rule.get('send_to', False)
    if  dest != True:
        if dest == False or dest is None or dst not in dest:
            return False
        

    allowed_conn_start = from_rule.get('initiator', False)
    action_connections_sub = action_connections.get(dst, [])
    pop_list = []
    t = time.time()
    for i, conn in enumerate(action_connections_sub):
        if t - conn[2] < err_resp_timout:
                pop_list.append(i)
        if conn[0] == src and conn[1] == event_id and not authorized:
            pop_list.append(i)
            pop_list = list(set(pop_list))
            authorized = True
    pop_list.reverse()
    for i in pop_list:
        action_connections_sub.pop(i)
    if not authorized:
        if allowed_conn_start == False or allowed_conn_start is None or dst not in allowed_conn_start:
            return False 
    
    authorized = False

    max_rate = rules.get('rate_limit', False)
    if max_rate is None:
        return False
    if max_rate != False:
        active = active_connections.get(src, None)
        if active:
            if (t-active[1]) < time_period:
                if active[0] < max_rate:
                    active[0] += 1
                else:
                    return False
            else:
                active[0] = 1
                active[1] = t
        else:
            active_connections[src] = [1, t]

    if dtype == 'action':
        arr = action_connections.get(src, [])
        arr.append(tuple(dst, event_id, time.time()))
    authorized = True
    return authorized