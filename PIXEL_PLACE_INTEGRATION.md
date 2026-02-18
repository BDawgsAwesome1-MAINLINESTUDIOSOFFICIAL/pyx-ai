# Pixel Place + Pyx AI — Integration Guide & Studio Prompt

## For the studio: what to do and how it works

**Pyx** is our kid-friendly content filter. It learns fast (minutes, not hours) and runs inside Pixel Place so we can flag inappropriate text before it’s shown.

### How it works

1. **You have some text** — e.g. a chat message, a prompt for an AI game, or any user- or AI-generated string.
2. **Run it through Pyx** — call `pyx.score(text)`. Pyx returns a number from 0 (safe) to 1 (bad).
3. **If the score is “bad”** (at or above the threshold, `BAN_LINE` = 0.7):
   - **Censor it for display:** replace every **letter** (A–Z, a–z) with the symbol **`~`**, then show that censored string (e.g. in chat or in an AI game).
   - Optionally you can also block the message entirely or show a warning; the minimum we ask is: **when you do show it, show the censored version** (letters → `~`).
4. **If the score is “safe”** — show the text as-is.

So: **bad content is not shown in plain text; it’s shown with letters replaced by `~`** (and you can add blocking on top of that if you want).

### Where to use it

Use Pyx (and the “if bad → censor letters with `~`” rule) everywhere text can be seen by players:

- **Chat** — filter and censor messages before they’re displayed.
- **AI games / AI-generated content** — before showing any AI-generated text (names, descriptions, prompts, etc.), run it through Pyx and censor if bad.
- **Any other user- or AI-generated text** — usernames, custom game text, etc., when you want them to be kid-safe.

**Please implement this in the studio when you build AI games and any feature that displays user or AI text.** One shared flow: “get text → Pyx score → if bad, show `censor_letters(text)` instead of `text`.”

---

## Implementation (Python)

If Pixel Place (or a backend/service) uses Python and the `pyx_ai` package:

```python
from pyx_ai import PyxAI, BAN_LINE, censor_letters

# Once at startup (or reuse one instance)
pyx = PyxAI()

def filter_for_display(text: str) -> str:
    """If content is bad, return censored version (letters → ~); otherwise return as-is."""
    score = pyx.score(text)
    if score >= BAN_LINE:
        return censor_letters(text)
    return text
```

- **`pyx.score(text)`** — returns 0.0–1.0; **≥ BAN_LINE** means inappropriate.
- **`censor_letters(text)`** — returns the same string with every letter (A–Z, a–z) replaced by `~`.

Use `filter_for_display(message)` before showing a chat message or any AI-generated text. If you prefer to **block** bad messages instead of showing them censored, you can do:

```python
if pyx.score(text) >= BAN_LINE:
    # Don’t send / don’t show; optionally tell user “Message blocked.”
    return None  # or show censored: return censor_letters(text)
return text
```

---

## No server 24/7: run as serverless

You don’t need a server running Pyx 24/7. Deploy Pyx as a **serverless function** so it runs only when a request comes in.

- **Same API:** `POST` with `{"text": "..."}` → `{"score", "bad", "censored"}`.

**Firebase Hosting + Cloud Functions (recommended if you already use Firebase):**

- Deploy to your Hosting URL so Pyx is at `https://YOUR_PROJECT.web.app/api/score`.
- **Steps:** See [DEPLOY_FIREBASE.md](DEPLOY_FIREBASE.md) — copy `pyx_ai.py` into `functions/`, then `firebase deploy --only functions,hosting`.
- No server 24/7; the function runs only when called.

**AWS Lambda or other serverless:**

- **Handler:** Use `pyx_serverless.handler` (see `pyx_serverless.py`).
- **Details:** See [DEPLOY_SERVERLESS.md](DEPLOY_SERVERLESS.md).

After deployment, call your API URL from Pixel Place. No 24/7 server to maintain.

---

## HTTP service (call from any language)

If you prefer a normal server (e.g. on your own machine or a VPS), Pyx can run as an HTTP service so Pixel Place (or any client) can call it without using Python.

**Start the service:**

```bash
cd /path/to/pyx-ai
source .venv/bin/activate   # if using venv
python3 pyx_server.py --port 8765 --host 0.0.0.0
```

Default: `http://0.0.0.0:8765`. Use `--port` and `--host` to change.

**Endpoints:**

| Method | Path    | Body / Response |
|--------|---------|-----------------|
| POST   | `/score` | Body: `{"text": "..."}` → `{"score": float, "bad": bool, "censored": "..."}` |
| GET    | `/health` | → `{"status": "ok", "service": "pyx"}` |

**Example: score text**

```bash
curl -X POST http://localhost:8765/score -H "Content-Type: application/json" -d '{"text": "hello world"}'
```

Response:

```json
{"score": 0.1234, "bad": false, "censored": "hello world"}
```

If the content is bad, `bad` is `true` and `censored` has letters replaced with `~`:

```json
{"score": 0.85, "bad": true, "censored": "~~~~ ~~~ ~~~~"}
```

**From your game/client:** POST JSON `{"text": "user message"}` to `http://your-server:8765/score`. If the response has `bad: true`, show `censored` (or block). If `bad: false`, show the original text. CORS is enabled so browsers can call the service.

---

## If Pixel Place is not in Python

- **Same rules:** run the text through Pyx (or the HTTP service above). If the result is “bad”, show the `censored` value from the response (letters → `~`) or block.
- **Censor rule:** any character in `A–Z` or `a–z` → `~`; leave spaces, numbers, and symbols as-is.
- Run `python3 pyx_server.py` on a machine your game can reach, then call `POST /score` from chat, AI games, or any feature that displays text.

---

## Summary

| Step | Action |
|------|--------|
| 1 | Get text (chat, AI game, etc.). |
| 2 | Call Pyx: `score = pyx.score(text)`. |
| 3 | If `score >= BAN_LINE`: show (or send) **`censor_letters(text)`** (letters → `~`); optionally also block. |
| 4 | If `score < BAN_LINE`: show text as-is. |
| 5 | Use this flow for **all** AI games and any place user/AI text is shown. |

Pyx learns from the training list and from overrides (and supports `...` prefix rules). Keep using it everywhere we display text so one policy applies across chat and AI games.
