#!/usr/bin/env python
# coding: utf-8

import unittest
from ..image_widget import ImageWidget


def test_image_widget_creation_blank():
  w = ImageWidget()
  assert w.description == 'A widget to visualize image attributions.'


def test_image_widget_load_dict():
  mock_data = {
      'attributions': {
          'data': [[[255, 255, 255], [200, 0, 111]]]
      },
      'debug_raw_attribution_dict': {
          'data': [[[0.1, 0.1, 0.1], [0.2, 0.2, 0.3]]]
      },
      'debug_input_values': {
          'data': [[[255, 255, 255], [200, 0, 111]]]
      },
      'baseline_score': 0.1,
      'label_index': 0,
      'example_score': 0.0,
      'output_name': 'output_name',
  }
  mock_metadata = {'inputs': {'data': {}}, 'outputs': {}}

  w = ImageWidget()
  w.load_data_from_dict(mock_data, mock_metadata)
  unittest.TestCase().assertDictEqual(w._data_dict, mock_data)
