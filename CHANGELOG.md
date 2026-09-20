# Changelog

## 0.3.1 - 2026-09-20

### Taobao primary domain fix

- Added apex **taobao.com** and expanded hosts from official www.taobao.com
- 24 domains published including taobao.com / www.taobao.com

### Mode B official structured lists

- Fixture contracts for all 8 services under `tests/fixtures/*/mode_b/`
- `adapters/official_json/mode_b.py` + build integration
- Regression: `tests/test_mode_b.py`

### Publish path

- `python -m source_engine publish --service <id>`
- Promotion package + `publish.json` stamp + `generated/published/*.json`
- All 8 services marked **PUBLISHED**

## 0.3.0 - 2026-09-20

- Engineering 100%, quality uplift, conflict/health/quality/engineering
