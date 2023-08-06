#!/usr/bin/env python
# coding: utf-8
"""The python widget for image attribution that will be mapped to the typescript widget."""

import datetime
import json
from ._frontend import module_name
from ._frontend import module_version
from ipywidgets import DOMWidget
from traitlets import Bool
from traitlets import Dict
from traitlets import Unicode


class ImageWidget(DOMWidget):
  """A class to store the widget's model and view and properties that will be synced."""
  _model_name = Unicode('ImageWidgetModel').tag(sync=True)
  _model_module = Unicode(module_name).tag(sync=True)
  _model_module_version = Unicode(module_version).tag(sync=True)
  _view_name = Unicode('ImageWidgetView').tag(sync=True)
  _view_module = Unicode(module_name).tag(sync=True)
  _view_module_version = Unicode(module_version).tag(sync=True)

  description = Unicode('A widget to visualize image attributions.').tag(sync=True)
  ready = Bool(False).tag(sync=True)
  latest_update = Unicode('Latest update time').tag(sync=True)

  _data_url = Unicode('A url for loading data').tag(sync=True)
  _data_dict = Dict().tag(sync=True)
  _metadata_url = Unicode('A url for loading metadata').tag(sync=True)
  _metadata_dict = Dict().tag(sync=True)

  def __init__(self):
    super(ImageWidget, self).__init__()

    self._data_url = ''
    self._data_json_str = ''
    self._data_dict = {}
    self._metadata_url = ''
    self._metadata_json_str = ''
    self._metadata_dict = {}
    self.ready = False
    self.latest_update = ''

  def load_data_from_url(self, data_url, metadata_url):

    self._data_dict = {}
    self._metadata_url = metadata_url  # This needs to go first
    self._data_url = ''  # resets first to ensure it detects changes
    self._data_url = data_url

  def load_data_from_dict(self, data_dict, metadata_dict):

    self._data_url = ''
    self._metadata_dict = metadata_dict  # This needs to go first
    self._data_dict = {}  # resets first to ensure it detects changes
    self._data_dict = data_dict

  def load_data_from_json_str(self, data_json_str, metadata_json_str):

    metadata = json.loads(metadata_json_str)
    data = json.loads(data_json_str)
    self.load_data_from_dict(data, metadata)

  def update(self):
    self.latest_update = str(datetime.datetime.now())
