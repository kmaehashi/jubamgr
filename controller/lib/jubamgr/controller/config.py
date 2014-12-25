# -*- coding: utf-8 -*-

import json

from .entity import *

class JubaManagerConfig(object):
  def __init__(self):
    self._global_zookeeper = ''
    self._visors = []
    self._clusters = []
    self._servers = []
    self._proxies = []

  @classmethod
  def from_json(cls, data):
    # TODO handle errors

    cfg = json.loads(data)
    obj = cls()

    # TODO assert values of config file

    obj._global_zookeeper = cfg['global']['zookeeper']
    obj._visors = map(lambda x: JubaVisor.create(x), cfg['visors'])
    obj._clusters = map(lambda x: JubaCluster.create(x), cfg['clusters'])
    obj._servers = map(lambda x: JubaServer.create(x), cfg['servers'])
    obj._proxies = map(lambda x: JubaProxy.create(x), cfg['proxies'])

    return obj

  def lookup(self, process_type, query_id):
    if process_type == 'server':
      return filter(lambda x: x.get_id() == query_id, self._servers)[0]
    elif process_type == 'proxy':
      return filter(lambda x: x.get_id() == query_id, self._proxies)[0]
    elif process_type == 'visor':
      return filter(lambda x: x.get_id() == query_id, self._visors)[0]
    elif process_type == 'cluster':
      return filter(lambda x: x.get_id() == query_id, self._clusters)[0]

  def get_all(self, process_type):
    if process_type == 'server':
      return self._servers
    elif process_type == 'proxy':
      return self._proxies
    elif process_type == 'visor':
      return self._visors
    elif process_type == 'cluster':
      return self._clusters
