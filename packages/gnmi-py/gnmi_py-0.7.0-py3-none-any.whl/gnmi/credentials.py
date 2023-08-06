# -*- coding: utf-8 -*-
# Copyright (c) 2021 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

try:
    import keyring
except ImportError:
    pass

from typing import Optional
from dataclasses import dataclass
from collections import abc

@dataclass
class BaseCredentials(): ...

class SSLCredentials(BaseCredentials):
    ca_cert: str
    client_cert: str
    client_key: str

    @classmethod
    def import(cert_file: str, key_file: str, ca_file: Optional[str]): ...

class UserPassCredentials(BaseCredentials):
    username: str
    password: str