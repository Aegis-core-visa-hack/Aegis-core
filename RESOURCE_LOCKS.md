# Resource Locks
## Self-Check Before Using Shared Resources

> **PROTOCOL:** Before using a resource, check this file. Update when you start/stop using.

---

## 🖥️ SERVERS

| Resource | Port | Status | Locked By | Since |
|----------|------|--------|-----------|-------|
| Frontend | 3000 | 🟢 RUNNING | System | 05:19 IST |
| Backend | 8000 | 🟢 RUNNING | System | 05:34 IST |

**Note:** Servers auto-reload on file changes. No need to restart.

---

## 🌐 BROWSER

| Browser Session | Status | Locked By | Purpose | Since |
|-----------------|--------|-----------|---------|-------|
| Chrome Tab 1 | 🟢 FREE | - | - | - |
| Chrome Tab 2 | 🟢 FREE | - | - | - |

---

## 📁 FILE LOCKS

| File/Directory | Status | Locked By | Since |
|----------------|--------|-----------|-------|
| `routes/__init__.py` | 🟢 FREE | - | - |
| `agents/__init__.py` | 🟢 FREE | - | - |
| `main.py` | 🟢 FREE | - | - |

---

## HOW TO USE

### Before Using a Resource:
```markdown
1. Check this file
2. If 🟢 FREE - Update status to 🔴 LOCKED with your agent name
3. Do your work
4. Update status back to 🟢 FREE when done
```

### Example Lock:
```markdown
| Chrome Tab 1 | 🔴 LOCKED | Agent-1-Regulatory | Testing /api/regulations | 05:45 IST |
```

### If Resource is LOCKED:
- Wait 2 minutes
- Check again
- If still locked after 5 min, assume stale lock and take over

---

## CURRENT ACTIVITY LOG

| Time | Agent | Action |
|------|-------|--------|
| 05:42 | Coordinator | Created lock file |

---

*Auto-check command:* `cat RESOURCE_LOCKS.md | head -30`
