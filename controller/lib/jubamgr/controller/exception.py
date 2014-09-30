# -*- coding: utf-8 -*-

class ConfigurationError(Exception):
  pass

class DuplicateIDError(ConfigurationError):
  pass

class NoSuchIDError(Exception):
  def __init__(self, expected_class, expected_id, actual_obj=None):
    msg = ''
    if actual_obj:
      msg = 'Entity ' + expected_id + ' is ' + actual_obj.__class__.__name__ + \
            ' whereas ' + expected_class.__class__.__name__ + 'is expected'
    else:
      msg = 'No such entity found: ' + expected_id
    super(NoSuchIDError, self).__init__(msg)
