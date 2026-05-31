#!/usr/bin/env python3
"""
Memory Daemon — central cross-project team memory.
Persistent process on 127.0.0.1. Embedding model loaded once at startup.

  POST /save    — save a lesson (kind=lesson) or fact (kind=fact)
  POST /recall  — semantic search; scope=project|all
  GET  /health  — health check

POST authorization: X-Daemon-Secret header.

Dependencies: psycopg[binary], fastembed
Install: pip install "psycopg[binary]" fastembed
"""
import json, sys, signal, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import psycopg
from fastembed import TextEmbedding

ENV = {}
_env = Path(__file__).with_name(".env")
if _env.exists():
    for ln in _env.read_text().splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#") and "=" in ln:
            k, v = ln.split("=", 1)
            ENV[k.strip()] = v.strip()

DB = dict(
    host="127.0.0.1",
    port=int(ENV.get("POSTGRES_PORT", "5400")),
    dbname=ENV.get("POSTGRES_DB", "team_memory"),
    user=ENV.get("POSTGRES_USER", "devteam"),
    password=ENV.get("POSTGRES_PASSWORD", ""),
)
PORT = int(ENV.get("DAEMON_PORT", "5401"))
SECRET = ENV.get("DAEMON_SECRET", "")

print("[daemon] loading nomic-embed-text-v1.5 ...", flush=True)
_model = TextEmbedding(model_name="nomic-ai/nomic-embed-text-v1.5")
_emb_lock = threading.Lock()
print("[daemon] model ready (768 dim)", flush=True)


def embed(text, mode="document"):
    prefix = "search_query: " if mode == "query" else "search_document: "
    with _emb_lock:
        v = list(_model.embed([prefix + (text or "")]))[0]
    return "[" + ",".join(f"{x:.6f}" for x in v.tolist()) + "]"


def db():
    return psycopg.connect(**DB)


def ensure_project(cur, name):
    cur.execute(
        "INSERT INTO projects(name) VALUES(%s) "
        "ON CONFLICT(name) DO UPDATE SET name=EXCLUDED.name RETURNING id",
        (name,),
    )
    return cur.fetchone()[0]


def handle_save(d):
    kind = d.get("kind", "fact")
    project = (d.get("project") or "default").strip()
    with db() as conn, conn.cursor() as cur:
        pid = ensure_project(cur, project)
        if kind == "lesson":
            text = " ".join(x for x in (d.get("symptom"), d.get("lesson")) if x) \
                or d.get("title", "")
            cur.execute(
                "INSERT INTO lessons(project_id,bug_id,title,status,found_by,caused_by,"
                "fixed_by,symptom,zone,root_cause,lesson,regression_test,embedding) "
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::vector) RETURNING id",
                (pid, d.get("bug_id"), d.get("title", "(untitled)"),
                 d.get("status", "open"), d.get("found_by"), d.get("caused_by"),
                 d.get("fixed_by"), d.get("symptom"), d.get("zone"), d.get("root_cause"),
                 d.get("lesson"), d.get("regression_test"), embed(text)),
            )
        else:
            content = d.get("content", "")
            cur.execute(
                "INSERT INTO facts(project_id,kind,content,importance,embedding) "
                "VALUES(%s,%s,%s,%s,%s::vector) RETURNING id",
                (pid, d.get("fact_kind", "fact"), content,
                 int(d.get("importance", 3)), embed(content)),
            )
        new_id = cur.fetchone()[0]
        conn.commit()
    return {"ok": True, "kind": kind, "id": new_id}


def handle_recall(d):
    query = (d.get("query") or "").strip()
    if not query:
        return {"ok": False, "error": "empty query"}
    project = (d.get("project") or "").strip()
    scoped = d.get("scope", "all") == "project" and bool(project)
    limit = int(d.get("limit", 5))
    qv = embed(query, mode="query")
    with db() as conn, conn.cursor() as cur:
        if scoped:
            cur.execute(
                "SELECT p.name,l.title,l.status,l.zone,l.lesson,l.regression_test,"
                "1-(l.embedding<=>%s::vector) FROM lessons l JOIN projects p ON p.id=l.project_id "
                "WHERE p.name=%s ORDER BY l.embedding<=>%s::vector LIMIT %s",
                (qv, project, qv, limit),
            )
        else:
            cur.execute(
                "SELECT p.name,l.title,l.status,l.zone,l.lesson,l.regression_test,"
                "1-(l.embedding<=>%s::vector) FROM lessons l JOIN projects p ON p.id=l.project_id "
                "ORDER BY l.embedding<=>%s::vector LIMIT %s",
                (qv, qv, limit),
            )
        lcols = ["project", "title", "status", "zone", "lesson", "regression_test", "sim"]
        lessons = [dict(zip(lcols, r)) for r in cur.fetchall()]

        if scoped:
            cur.execute(
                "SELECT p.name,f.kind,f.content,f.importance,1-(f.embedding<=>%s::vector) "
                "FROM facts f JOIN projects p ON p.id=f.project_id "
                "WHERE f.superseded_by IS NULL AND p.name=%s "
                "ORDER BY f.embedding<=>%s::vector LIMIT %s",
                (qv, project, qv, limit),
            )
        else:
            cur.execute(
                "SELECT p.name,f.kind,f.content,f.importance,1-(f.embedding<=>%s::vector) "
                "FROM facts f JOIN projects p ON p.id=f.project_id "
                "WHERE f.superseded_by IS NULL "
                "ORDER BY f.embedding<=>%s::vector LIMIT %s",
                (qv, qv, limit),
            )
        fcols = ["project", "kind", "content", "importance", "sim"]
        facts = [dict(zip(fcols, r)) for r in cur.fetchall()]
    return {"ok": True, "scope": "project" if scoped else "all",
            "lessons": lessons, "facts": facts}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"ok": True})
        else:
            self._send(404, {"ok": False, "error": "not found"})

    def do_POST(self):
        if SECRET and self.headers.get("X-Daemon-Secret") != SECRET:
            return self._send(403, {"ok": False, "error": "forbidden"})
        try:
            n = int(self.headers.get("Content-Length", 0))
            d = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._send(400, {"ok": False, "error": "bad json"})
        try:
            if self.path == "/save":
                self._send(200, handle_save(d))
            elif self.path == "/recall":
                self._send(200, handle_recall(d))
            else:
                self._send(404, {"ok": False, "error": "not found"})
        except Exception as e:
            print(f"[daemon] error {self.path}: {type(e).__name__}: {e}", flush=True)
            self._send(500, {"ok": False, "error": type(e).__name__})


def main():
    def _stop(*_):
        print("[daemon] stopping", flush=True)
        sys.exit(0)

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"[daemon] listening 127.0.0.1:{PORT} (auth: {'on' if SECRET else 'OFF'})", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
