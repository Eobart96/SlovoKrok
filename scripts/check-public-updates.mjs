import { readFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import assert from 'node:assert/strict';

export function validatePublicUpdates(data) {
  assert.equal(data?.schemaVersion, 1, 'Unknown public news format');
  assert.ok(Array.isArray(data.entries) && data.entries.length > 0 && data.entries.length <= 100, 'Expected 1–100 entries');
  const ids = new Set();
  let previousDate = '9999-99-99';
  const technical = /\b(?:backend|frontend|API|SQLite|Pydantic|TypeScript|CourseState|pytest|SQL|CI|JSON)\b/i;
  for (const entry of data.entries) {
    assert.match(entry.id, /^[a-z0-9-]{1,80}$/);
    assert.ok(!ids.has(entry.id), 'Duplicate news id');
    ids.add(entry.id);
    if (entry.version !== undefined) assert.match(entry.version, /^\d+\.\d+\.\d+$/, 'Invalid version');
    assert.match(entry.date, /^\d{4}-\d{2}-\d{2}$/);
    assert.equal(new Date(entry.date).toISOString().slice(0, 10), entry.date, 'Invalid calendar date');
    assert.ok(entry.date <= previousDate, 'Newest news must come first');
    previousDate = entry.date;
    assert.ok(Array.isArray(entry.changes) && entry.changes.length > 0 && entry.changes.length <= 8, 'Expected 1–8 changes');
    for (const value of [entry.title, ...entry.changes]) {
      assert.ok(typeof value === 'string' && value.trim() === value && value.length > 0 && value.length <= 400, 'Invalid public text');
      assert.ok(!technical.test(value), 'Keep technical details in CHANGELOG.md');
    }
  }
  return data;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const news = validatePublicUpdates(JSON.parse(await readFile(new URL('../updates/public.json', import.meta.url), 'utf8')));
  const pkg = JSON.parse(await readFile(new URL('../frontend/package.json', import.meta.url), 'utf8'));
  assert.equal(news.entries[0].version, pkg.version, 'Latest public version must match the application');
  console.log('PUBLIC_UPDATES_OK');
}
