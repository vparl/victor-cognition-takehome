---
title: CI/CD and Automation
sidebar_position: 5
---

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

# CI/CD and Automation

🚧 **Coming Soon** 🚧

Understanding Superset's continuous integration and deployment pipelines.

## Topics to be covered:

- GitHub Actions workflows
- Pre-commit hooks configuration
- Automated testing pipelines
- Code quality checks (ESLint, Prettier, Black, MyPy)
- Security scanning (Dependabot, CodeQL)
- Docker image building and publishing
- Release automation
- Performance benchmarking
- Coverage reporting and tracking

## Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks on staged files
pre-commit run

# Run specific hook
pre-commit run mypy

# Run on all files (not just staged)
pre-commit run --all-files
```

## GitHub Actions

Key workflows:
- `test-frontend.yml` - Frontend tests
- `test-backend.yml` - Backend tests
- `docker.yml` - Docker image builds
- `codeql.yml` - Security analysis
- `release.yml` - Release automation

## CI Environment Drift Memory

Known patterns where tests pass locally but fail in CI.

### Pattern: Conditional import creates environment-dependent constructor signatures

**Symptoms:**
- Test passes locally but fails in CI
- Error indicates missing required argument or unexpected class behavior
- A `try/except ImportError` block assigns a fallback class

**Root cause:** Fallback class (e.g., `Exception`) has a different constructor signature than the real class (e.g., `playwright.sync_api.TimeoutError`). Locally the fallback is used; in CI the real class is imported.

**Preferred fixes:**
- Always use the most restrictive calling convention (provide all required args for the real class)
- Mock imports explicitly rather than relying on package absence
- Add explicit test setup that does not depend on environment state

**Example (Issue #7):**
```python
# BAD: Works only when PlaywrightTimeout = Exception
timeout = PlaywrightTimeout()

# GOOD: Works in all environments
timeout = PlaywrightTimeout("timeout exceeded")
```

### Pattern: Local pass, CI fail due to leaked test state

**Symptoms:**
- Test passes alone but fails when run with other tests
- Error suggests missing config or polluted shared state

**Preferred fixes:**
- Make test setup explicit
- Reset mutated state in teardown
- Use monkeypatch/fixture scoping

---

*This documentation is under active development. Check back soon for updates!*
