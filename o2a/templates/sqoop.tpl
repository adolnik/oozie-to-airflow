{#
  Copyright 2019 Google LLC

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
 #}

{% import "macros/props.tpl" as props_macro %}
{{ task_id | to_var }} = SqoopOperator(
    task_id={{ task_id | to_python }},
    trigger_rule={{ trigger_rule | to_python }},
    {% if script %}query_uri='{}/{}'.format(CONFIG['gcp_uri_prefix'], {{ script | to_python }}),{% endif %}
    {% if query %}query={{ query | to_python }},{% endif %}
    {% if variables %}variables={{ variables | to_python }},{% endif %}
    dataproc_hive_properties={{ props_macro.props(action_node_properties=action_node_properties, xml_escaped=True) }},
    cluster_name=CONFIG['dataproc_cluster'],
    num_mappers=1,
    cmd_type="import",
    gcp_conn_id=CONFIG['gcp_conn_id'],
    region=CONFIG['gcp_region'],
    job_name={{ task_id | to_python }},
)
