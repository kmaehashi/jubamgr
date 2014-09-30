# -*- coding :utf-8 -*-

from weakref import WeakValueDictionary
from .exception import DuplicateIDError

class JubaManagerEntity(object):
  _id2entity = WeakValueDictionary()

  def __init__(self, my_id):
    if my_id is not None and my_id in self._id2entity:
      raise DuplicateIDError(my_id)
    self._id2entity[my_id] = self
    self._id = my_id

  @classmethod
  def lookup(cls, query_id):
    if query_id in _id2entity:
      v = _id2entity[query_id]
      if isinstance(v, cls):
        return v
      raise NoSuchIDError(cls, query_id, v)
    raise NoSuchIDError(cls, query_id)

  def get_id(self):
    return self._id

class JubaVisor(JubaManagerEntity):
  def __init__(self, my_id, host, port, options):
    super(JubaVisor, self).__init__(my_id)
    self._host = host
    self._port = port
    self._options = options

  @classmethod
  def create(cls, c):
    return cls(c['id'], c['host'], c['port'], c['options'])

class JubaCluster(JubaManagerEntity):
  def __init__(self, my_id, type, is_standalone):
    super(JubaCluster, self).__init__(my_id)
    self._type = type
    self._is_standalone = is_standalone

  @classmethod
  def create(cls, c):
    return cls(c['id'], c['type'], c['is_standalone'])

class JubaServer(JubaManagerEntity):
  def __init__(self, my_id, visor, cluster, port, options):
    super(JubaServer, self).__init__(my_id)
    self._visor = visor
    self._cluster = cluster
    self._port = port
    self._options = options

  @classmethod
  def create(cls, c):
    return cls(c['id'], c['visor'], c['cluster'], c['port'], c['options'])

class JubaProxy(JubaManagerEntity):
  def __init__(self, my_id, visor, type, port, options):
    super(JubaProxy, self).__init__(my_id)
    self._visor = visor
    self._type = type
    self._port = port
    self._options = options

  @classmethod
  def create(cls, c):
    return cls(c['id'], c['visor'], c['type'], c['port'], c['options'])
