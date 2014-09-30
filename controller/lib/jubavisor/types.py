# This file is auto-generated from jubavisor.idl with jenerator version 0.5.4-224-g49229fa/develop
# *** DO NOT EDIT ***


import sys
import msgpack
import jubatus.common
from jubatus.common.types import *

class ServerArgv:
  TYPE = TTuple(TInt(True, 4), TString(), TString(), TInt(True, 4), TInt(True,
      4), TInt(True, 4), TInt(True, 4), TString(), TString(), TString(),
      TString(), TString(), TString(), TString(), TString(), TInt(True, 4),
      TInt(True, 4), TString(), TBool())

  def __init__(self, port, bind_address, bind_if, timeout, zookeeper_timeout,
      interconnect_timeout, threadnum, program_name, type, z, name, datadir,
      logdir, log_config, eth, interval_sec, interval_count, mixer, daemon):
    self.port = port
    self.bind_address = bind_address
    self.bind_if = bind_if
    self.timeout = timeout
    self.zookeeper_timeout = zookeeper_timeout
    self.interconnect_timeout = interconnect_timeout
    self.threadnum = threadnum
    self.program_name = program_name
    self.type = type
    self.z = z
    self.name = name
    self.datadir = datadir
    self.logdir = logdir
    self.log_config = log_config
    self.eth = eth
    self.interval_sec = interval_sec
    self.interval_count = interval_count
    self.mixer = mixer
    self.daemon = daemon

  def to_msgpack(self):
    t = (self.port, self.bind_address, self.bind_if, self.timeout,
        self.zookeeper_timeout, self.interconnect_timeout, self.threadnum,
        self.program_name, self.type, self.z, self.name, self.datadir,
        self.logdir, self.log_config, self.eth, self.interval_sec,
        self.interval_count, self.mixer, self.daemon)
    return self.__class__.TYPE.to_msgpack(t)

  @classmethod
  def from_msgpack(cls, arg):
    val = cls.TYPE.from_msgpack(arg)
    return ServerArgv(*val)

  def __repr__(self):
    gen = jubatus.common.MessageStringGenerator()
    gen.open("server_argv")
    gen.add("port", self.port)
    gen.add("bind_address", self.bind_address)
    gen.add("bind_if", self.bind_if)
    gen.add("timeout", self.timeout)
    gen.add("zookeeper_timeout", self.zookeeper_timeout)
    gen.add("interconnect_timeout", self.interconnect_timeout)
    gen.add("threadnum", self.threadnum)
    gen.add("program_name", self.program_name)
    gen.add("type", self.type)
    gen.add("z", self.z)
    gen.add("name", self.name)
    gen.add("datadir", self.datadir)
    gen.add("logdir", self.logdir)
    gen.add("log_config", self.log_config)
    gen.add("eth", self.eth)
    gen.add("interval_sec", self.interval_sec)
    gen.add("interval_count", self.interval_count)
    gen.add("mixer", self.mixer)
    gen.add("daemon", self.daemon)
    gen.close()
    return gen.to_string()

