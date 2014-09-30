# -*- coding: utf-8 -*-

from jubavisor.client import Jubavisor
from jubavisor.types import ServerArgv

from .config import JubaManagerConfig

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
    else:
      # TODO support save,load,status subcmd
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


