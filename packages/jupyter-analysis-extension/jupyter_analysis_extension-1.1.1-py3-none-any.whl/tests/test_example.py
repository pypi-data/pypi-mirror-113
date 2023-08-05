#!/usr/bin/env python
# coding: utf-8

# Copyright (c) kyoungjun.
# Distributed under the terms of the Modified BSD License.

from jupyter_analysis_extension.example import ExampleWidget
from jupyter_analysis_extension.widget_func import WidgetFunc



def test_example_creation_blank():
    w = ExampleWidget()
    assert w.value == 'Hello World'
