#!/usr/bin/env python

# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import uuid, json

from datetime import datetime
from locust import HttpLocust, TaskSet, task


class MetricsTaskSet(TaskSet):
    _deviceid = None

    def on_start(self):
        self._deviceid = str(uuid.uuid4())

    @task(1)
    def test_root(self):
        self.client.get('/')

    @task(1)
    def test_load(self):
        with open('json_input.json') as f:
            d = json.load(f)
            e = json.dumps(d)
        data = {'json': e}
        response = self.client.post("/detect-boundaries-gps-test", data=data, follow_redirects=True,
                                    content_type='multipart/form-data')


class MetricsLocust(HttpLocust):
    task_set = MetricsTaskSet