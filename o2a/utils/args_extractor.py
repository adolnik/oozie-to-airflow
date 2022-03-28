# -*- coding: utf-8 -*-
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Extract params from oozie's action node"""
from _elementtree import Element

from o2a.o2a_libs import el_parser
from o2a.utils import xml_utils

TAG_ARG = "arg"


def extract_arg_values_from_action_node(oozie_node: Element):
    arg_nodes = xml_utils.find_nodes_by_tag(oozie_node, TAG_ARG)

    new_args = {}
    ln = len(arg_nodes)
    i = 0
    if (ln % 2) == 0:
        while i < ln:
            if not arg_nodes[i].text or not arg_nodes[i+1].text or (not arg_nodes[i].text.startswith('--')):
                i = i + 2
                continue
            key = el_parser.translate(arg_nodes[i].text)[2:]
            value = el_parser.translate(arg_nodes[i+1].text)
            new_args[key] = value
            i = i + 2
    return new_args
