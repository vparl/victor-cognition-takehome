# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
Demo test: PlaywrightTimeout environment drift

Reproduces a real CI reliability issue:
- Passes locally when playwright is NOT installed (fallback to Exception)
- Fails in CI where playwright IS installed (requires message argument)

Root cause: conditional import creates different behavior across environments.
"""

try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeout
except ImportError:
    PlaywrightTimeout = Exception


def test_playwright_timeout_handles_timeout_gracefully():
    """Test that PlaywrightTimeout can be instantiated in timeout handling code."""
    timeout = PlaywrightTimeout("timeout exceeded")
    assert timeout is not None


def test_playwright_timeout_with_message():
    """Test that PlaywrightTimeout works with message argument."""
    timeout = PlaywrightTimeout("timeout exceeded")
    assert timeout is not None
