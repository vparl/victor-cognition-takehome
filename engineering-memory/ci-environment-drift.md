# CI Environment Drift Log

Records incidents where CI and local environments diverge, causing tests to pass locally but fail in CI (or vice versa).

---

## 2026-06-07 — conditional-import-constructor-drift

**Pattern name:** conditional-import-constructor-drift

**Symptom:** Test passes locally, fails in CI with `TypeError` on class instantiation.

**Root cause:** `playwright` is an optional extra in `pyproject.toml`. Locally most developers skip it, so the conditional import falls back to `PlaywrightTimeout = Exception`. `Exception()` accepts zero args, but the real `playwright.sync_api.TimeoutError` requires a message string. CI installs `playwright` explicitly, so the real class is used and the bare `PlaywrightTimeout()` call raises a `TypeError`.

**Fix applied:** Added required `message` argument to the `PlaywrightTimeout()` call in `tests/unit_tests/utils/devin_demo/test_playwright_environment.py` (line 21).

**Prevention:**
- Always use the most restrictive constructor signature when instantiating conditionally-imported classes.
- Add optional dependencies to development requirements so local and CI environments match.

**Validation command:**
```bash
pytest tests/unit_tests/utils/devin_demo/ -v --noconftest
```
