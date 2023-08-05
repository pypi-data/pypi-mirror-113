# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""PyPI package definition."""

from setuptools import setup

setup(name="CTG Surface Distance Based Measures",
      version="0.1",
      description=(
          "Library containing utilities to compute performance metrics for "
          "segmentation"),
      url="https://github.com/capitaltg/surface-distance",
      author="DeepMind",
      license="Apache License, Version 2.0",
      packages=["surface_distance"],
      install_requires=["numpy", "scipy", "absl-py"])
