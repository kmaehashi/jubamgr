import logging
import weakref
import time

import kazoo
import kazoo.client
import kazoo.exceptions

logging.basicConfig()

def get_zk():
  zk = kazoo.client.KazooClient(hosts='127.0.0.1:2181')
  zk.start()
  return zk

class JubatusClientCancelOnDown(object):
  def __init__(self, client, future, zk, host, port, jubatus_type, name):
    self._client_ref = weakref.ref(client)
    self._future_ref = weakref.ref(future)
    self._watcher = JubatusNodeWatcher(zk)
    r = self._watcher.set_callback(host, port, jubatus_type, name, self._got_down)
    if not r:
      raise RuntimeError('failed to set callback; maybe the node does not exist?')

  def _got_down(self):
    c = self._client_ref()
    f = self._future_ref()
    if c is not None:
      c.on_connect_failed('ZooKeeper detected that the node went down')
    if f is not None:
      f.set_error('node down')

class JubatusNodeWatcher():
  def __init__(self, zk):
    """
    Kazoo ZK client to use; must be started beforehand.
    """
    self._zk = zk

  def set_callback(self, host, port, jubatus_type, name, callback):
    """
    Set a one-shot callback to detect down of the specified Jubatus node.
    """
    path = '/jubatus/actors/{0}/{1}/nodes/{2}_{3}'.format(jubatus_type, name, host, port)
    try:
      self._zk.get(path, self._get_event_handler(callback))
      return True
    except kazoo.exceptions.NoNodeError as e:
      return False

  def _get_event_handler(self, callback):
    def _event_handler(event):
      if event.type == 'DELETED':
        callback()
      return False
    return _event_handler
