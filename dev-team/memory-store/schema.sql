-- Central cross-project memory. Postgres 16 + pgvector.
-- Embeddings: local nomic-embed-text-v1.5 (768 dim).
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS projects (
  id         SERIAL PRIMARY KEY,
  name       TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS lessons (
  id              SERIAL PRIMARY KEY,
  project_id      INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  bug_id          TEXT,
  title           TEXT NOT NULL,
  status          TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','fixed')),
  found_by        TEXT,
  caused_by       TEXT,
  fixed_by        TEXT,
  symptom         TEXT,
  zone            TEXT,
  root_cause      TEXT,
  lesson          TEXT,
  regression_test TEXT,
  embedding       vector(768),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS facts (
  id            SERIAL PRIMARY KEY,
  project_id    INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  kind          TEXT NOT NULL DEFAULT 'fact'
                CHECK (kind IN ('fact','decision','contract','pattern','preference')),
  content       TEXT NOT NULL,
  importance    INTEGER NOT NULL DEFAULT 3 CHECK (importance BETWEEN 1 AND 5),
  embedding     vector(768),
  valid_from    TIMESTAMPTZ NOT NULL DEFAULT now(),
  superseded_by INTEGER REFERENCES facts(id),
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_lessons_project ON lessons(project_id);
CREATE INDEX IF NOT EXISTS idx_lessons_zone    ON lessons(zone);
CREATE INDEX IF NOT EXISTS idx_lessons_emb     ON lessons USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_facts_project   ON facts(project_id);
CREATE INDEX IF NOT EXISTS idx_facts_active    ON facts(project_id) WHERE superseded_by IS NULL;
CREATE INDEX IF NOT EXISTS idx_facts_emb       ON facts USING hnsw (embedding vector_cosine_ops);
