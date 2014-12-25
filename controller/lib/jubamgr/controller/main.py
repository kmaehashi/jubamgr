# -*- coding: utf-8 -*-

import threading

import msgpackrpc

from jubavisor.client import Jubavisor
from jubavisor.types import ServerArgv

from .config import JubaManagerConfig
from .zk import get_zk, JubatusClientCancelOnDown

class JubaManagerController():
  @classmethod
  def main(cls, args):
    myself = args.pop(0)

    # TODO externalize config field name

    with open('config.json') as f:
      cfg = JubaManagerConfig.from_json(f.read())

    # TODO assert length of args

    subcmd = args[0]
    if subcmd == 'start':
      process_type = args[1]
      target_id = args[2]
      cls.start(cfg, process_type, target_id)
    elif subcmd == 'stop':
      process_type = args[1]
      target_id = args[2]
      cls.stop(cfg, process_type, target_id)
    elif subcmd == 'save':
      target_id = args[1]
      cls.local_model(cfg, target_id, 'save')
    elif subcmd == 'load':
      target_id = args[1]
      cls.local_model(cfg, target_id, 'load')
    elif subcmd == 'status':
      # TODO implement
      print "Not implemented yet: {0}".format(subcmd)
    else:
      print "Unknown subcmd: {0}".format(subcmd)

  @classmethod
  def start(cls, cfg, process_type, target_id):
    server = cfg.lookup(process_type, target_id)
    visor = cfg.lookup('visor', server._visor)
    cluster = cfg.lookup('cluster', server._cluster)

    client = Jubavisor(visor._host, visor._port, 'juba' + cluster._type + '/' + cluster._id, 10)
    argv = ServerArgv(server._port, "", "", 10, 10, 10, 2, 'juba' + cluster._type, cluster._type, cfg._global_zookeeper,
                      cluster._id, "", "", "", "", 16, 512, "linear_mixer", False)
    client.start(1, argv)

  @classmethod
  def stop(cls, cfg, process_type, target_id):
    server = cfg.lookup(process_type, target_id)
    visor = cfg.lookup('visor', server._visor)
    cluster = cfg.lookup('cluster', server._cluster)

    client = Jubavisor(visor._host, visor._port, 'juba' + cluster._type + '/' + cluster._id, 10)
    client.stop(1)

  @classmethod
  def local_model(cls, cfg, target_id, method):
    cluster = cfg.lookup('cluster', target_id)
    servers = []

    if cluster is None:
      server = cfg.lookup('server', target_id)
      if server is None:
        print "No such cluster or server matching the ID"
        return
      servers.append(server)
      cluster = cfg.lookup('cluster', server._cluster)
    else:
      servers = filter(lambda x: x._cluster == cluster._id, cfg.get_all('server'))

    threads = []
    zk = get_zk()
    for s in servers:
      host = cfg.lookup('visor', s._visor)._host
      client = msgpackrpc.Client(msgpackrpc.Address(host, s._port), 30)
      future = client.call_async(method, cluster._id, 'jubamgr',)
      w = JubatusClientCancelOnDown(client, future, zk, host, s._port, cluster._type, cluster._id)
      future.get()
    zk.stop()
