import logging
import weakref
import time

import msgpackrpc.error

import kazoo
import kazoo.client
import kazoo.exceptions

logging.basicConfig()

def get_zk():
  zk = kazoo.client.KazooClient(hosts='127.0.0.1:2181')
  zk.start()
  return zk

class JubatusNodeDown(msgpackrpc.error.TransportError):
  pass

def cancel_if_down(client, zk, host, port, jubatus_type, name):
  client_ref = weakref.ref(client)
  def _handle():
    c = client_ref()
    if c is not None:
      c.on_connect_failed(JubatusNodeDown('ZooKeeper detected the node down'))
  watcher = JubatusNodeWatcher(zk)
  if not watcher.set_callback(host, port, jubatus_type, name, _handle):
    raise RuntimeError('failed to set callback; maybe the node does not exist?')

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
