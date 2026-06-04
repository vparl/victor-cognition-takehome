<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

# Root Cause Analysis: Playwright Environment Drift (Issue #7)

## Summary

| Field | Value |
|-------|-------|
| **Issue** | #7 |
| **Test File** | `tests/unit_tests/utils/devin_demo/test_playwright_environment.py` |
| **Root Cause Category** | `explicit_test_setup` |
| **Fix PR** | #8 |
| **Risk** | None — test-only change, no production behavior affected |

## Problem

The test `test_playwright_timeout_handles_timeout_gracefully` passed locally but failed in CI.

### Mechanism

```python
try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeout
except ImportError:
    PlaywrightTimeout = Exception
```

This conditional import creates **environment-dependent behavior**:

| Environment | `PlaywrightTimeout` resolves to | `PlaywrightTimeout()` (no args) |
|-------------|--------------------------------|----------------------------------|
| Local (no playwright) | `Exception` | ✅ Works (Exception accepts no args) |
| CI (playwright installed) | `playwright.sync_api.TimeoutError` | ❌ Fails (requires `message` arg) |

### Root Cause

Line 21 called `PlaywrightTimeout()` with no arguments, relying on the implicit assumption that the fallback class (`Exception`) would always be used. In CI, playwright is installed, so the real `TimeoutError` class is imported — and it requires a `message` argument.

## Fix

Provide the `message` argument explicitly so the test passes regardless of which class is resolved:

```python
# Before (broken in CI)
timeout = PlaywrightTimeout()

# After (works everywhere)
timeout = PlaywrightTimeout("timeout exceeded")
```

## Pattern: Conditional Import Environment Drift

**When this happens:** A try/except import block assigns a fallback class with a different constructor signature than the real class.

**Why it's subtle:** Tests pass locally because the fallback class is used, but fail in CI where the real dependency is installed.

**How to prevent:**
1. Always use the most restrictive calling convention (provide all args the real class requires)
2. If testing the fallback path, mock the import explicitly rather than relying on absence
3. Consider adding a CI-reproducing `conftest.py` fixture that forces the real import

## Validation

```bash
pytest tests/unit_tests/utils/devin_demo/test_playwright_environment.py -v --noconftest
```
