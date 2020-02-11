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
from random import randint
from locust import HttpLocust, TaskSet, task

class MetricsTaskSet(TaskSet):
    _deviceid = None

    def on_start(self):
        self._deviceid = str(uuid.uuid4())

    @task(1)
    def test_root(self):
        self.client.get('/')

    @task(5)
    def test_load(self):
        with open('./json_input.json') as f:
            d = json.load(f)
            e = json.dumps(d)

        #json_str = '{"fx": 1024.6653,"fy": 1023.67645,"height": 720,"pitch_box_height": 40.3,"pitch_box_width": 16.5,"pitch_height": 66.0,"pitch_width": 104.6,"origin_point": "e", "stadium_a": {"lat": 51.262193,"long": 6.733061},        "stadium_b": {"lat": 51.261808,"long": 6.732308}, "stadium_c": {"lat": 51.261828,"long": 6.733535},"stadium_center": {"lat": 51.261636,"long": 6.733158},"stadium_d": {"lat": 51.261445,"long": 6.732780},"stadium_e": {"lat": 51.261465,"long": 6.734012},"stadium_f": {"lat": 51.261076,"long": 6.733260},"user_position": {"lat": 51.260778,"long": 6.733281},"width": 1280}'
        #e = json.dumps(json_str)
        data = {'json': e}
        response = self.client.post("/detect-boundaries-gps-test", data=data, follow_redirects=True,
                                    content_type='multipart/form-data')


class MetricsLocust(HttpLocust):
    task_set = MetricsTaskSet
    wait_time = randint(5, 15)