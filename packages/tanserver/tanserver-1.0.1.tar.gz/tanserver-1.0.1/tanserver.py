# -*- coding: utf-8 -*-

# Copyright (C) tanserver.org
# Copyright (C) Chen Daye

import json
from ctypes import *

# shm_open()
CDLL('librt.so', mode=RTLD_GLOBAL)

# PostgreSQL C Client
CDLL('libpq.so', mode=RTLD_GLOBAL)

# libconfuse
CDLL('/usr/local/tanserver/lib/libconfuse.so',
     mode=RTLD_GLOBAL)

# JsonCpp
CDLL('/usr/local/tanserver/lib/libjsoncpp.so',
     mode=RTLD_GLOBAL)

# Currently supports pg_query(), json_append_status()
core = CDLL('/usr/local/tanserver/lib/libcore.so')

# Set argtypes
core.pg_query.argtypes           = [c_char_p]
core.json_append_status.argtypes = [c_char_p]

# Set restype
core.pg_query.restype           = c_char_p
core.json_append_status.restype = c_char_p

# Query database and get the first field of the first row.
def pg_query(hostaddr, query, *args):
  res = core.pg_query(hostaddr, query, *args)

  # pg_query() returned NULL in C.
  if res == None:
    raise Exception("Query failed.")

  return res

# Append status code and message to a JSON string.
def json_append_status(json_string, status_code, message):
  return core.json_append_status(json_string, status_code, message)
