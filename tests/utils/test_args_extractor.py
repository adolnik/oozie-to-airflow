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
"""Tests for arg extractor"""
import unittest

from xml.etree import ElementTree as ET

from o2a.utils.args_extractor import extract_arg_values_from_action_node


class ParamExtractorModuleTestCase(unittest.TestCase):
    def test_extract_arg_values_from_action_node_should_return_empty_dict_when_not_found(self):
        node = ET.fromstring("<dummy></dummy>")
        result = extract_arg_values_from_action_node(node)
        self.assertEqual({}, result)

    def test_extract_arg_values_from_action_node_should_parse_single_value(self):
        # language=XML
        xml_content = """
        <fragment>
            <arg>--INPUT</arg>
            <arg>VALUE</arg>
        </fragment>
        """
        node = ET.fromstring(xml_content)
        result = extract_arg_values_from_action_node(node)
        self.assertEqual({"INPUT": "VALUE"}, result)

    def test_extract_arg_values_from_action_node_should_parse_multiple_value(self):
        # language=XML
        xml_content = """
        <fragment>
            <arg>--INPUT1</arg>
            <arg>VALUE1</arg>
            <arg>--INPUT2</arg>
            <arg>VALUE2</arg>
        </fragment>
        """
        node = ET.fromstring(xml_content)
        result = extract_arg_values_from_action_node(node)
        self.assertEqual({"INPUT1": "VALUE1", "INPUT2": "VALUE2"}, result)

    def test_extract_arg_values_from_action_node_should_support_el_value(self):
        # language=XML
        xml_content = """
        <fragment>
            <arg>--INPUT</arg>
            <arg>/user/${userName}/${examplesRoot}/apps/hive/input/</arg>
            <arg>--OUTPUT</arg>
            <arg>/user/${userName}/${examplesRoot}/apps/hive/output/</arg>
        </fragment>
        """
        node = ET.fromstring(xml_content)
        result = extract_arg_values_from_action_node(node)
        self.assertEqual(
            {
                "INPUT": "/user/{{userName}}/{{examplesRoot}}/apps/hive/input/",
                "OUTPUT": "/user/{{userName}}/{{examplesRoot}}/apps/hive/output/",
            },
            result,
        )
