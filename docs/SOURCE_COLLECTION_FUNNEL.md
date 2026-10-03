# Source → Collection 晋升漏斗（运营 SSOT）

> **Source lifecycle ≠ Collection production。**  
> 用户可见服务身份以 Collection `rule/_index.yaml` + `PUBLISH_STATUS.md` 为准。

## 周度配额（A）

- 每周从 **VERIFIED** 晋升 ≥ **8** 个到 Source **canary**
- **禁止跳级**到 production
- 本周批次（2026-10-03）：appledev appstore icloud applemusic applemedia azure openai claude → canary

## 阻塞看板（B）

```bash
python scripts/source_blocked_board.py
```

见 `docs/BLOCKED_BOARD.md`。
