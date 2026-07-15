#! /bin/bash -e
# Copyright (c) 2025-2026, NVIDIA CORPORATION.
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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
JVM_DIR="$REPO_ROOT/jvm"

MVN_ARGS=()
if [[ -z "${ART_URL:-}" && -n "${ARTIFACTORY_NAME:-}" ]]; then
    export ART_URL="https://${ARTIFACTORY_NAME}/artifactory/sw-spark-maven"
fi
if [[ -n "${ART_URL:-}" ]]; then
    MVN_ARGS+=(--settings "$REPO_ROOT/ci/settings.xml")
fi

pip install pyspark==4.0.0
pushd "$JVM_DIR"
mvn "${MVN_ARGS[@]}" clean test
popd
pip install -r "$SCRIPT_DIR/requirements_dev.txt"
