# This file is auto-generated from jubavisor.idl with jenerator version 0.5.4-224-g49229fa/develop
# *** DO NOT EDIT ***


import msgpackrpc
import jubatus.common
from .types import *
from jubatus.common.types import *

class Jubavisor(jubatus.common.ClientBase):
  def __init__(self, host, port, name, timeout=10):
    super(Jubavisor, self).__init__(host, port, name, timeout)

  def start(self, num, argv):
    return self.jubatus_client.call("start", [num, argv], TInt(True, 4), [TInt(
        False, 4), TUserDef(ServerArgv)])

  def stop(self, num):
    return self.jubatus_client.call("stop", [num], TInt(True, 4), [TInt(False,
        4)])
