const isDarkMode = () => {
  return window.matchMedia('(prefers-color-scheme: dark)').matches;
}

/* ===========================
   Notes Page Builder (STATIC)
   =========================== */

/** Manually list your notes here. */
const NOTES = [
  {
    course: "CS2420",
    date: "2024-09-05",
    topic: "First Lecture",
    file: "doc/notes/9-5-24.md"
  },
];

async function buildNotesPage() {
  const root = document.getElementById('notes-root');
  if (!root) return;

  const byCourse = new Map();
  for (const n of NOTES) {
    if (!byCourse.has(n.course)) byCourse.set(n.course, []);
    byCourse.get(n.course).push(n);
  }

  for (const [course, arr] of byCourse) {
    arr.sort((a, b) => b.date.localeCompare(a.date));
  }

  const frag = document.createDocumentFragment();
  for (const [course, arr] of byCourse) {
    const section = document.createElement('section');
    section.className = 'course-block';

    const h = document.createElement('div');
    h.className = 'course-title';
    h.textContent = course + " Notes";
    section.appendChild(h);

    const wrap = document.createElement('div');
    wrap.className = 'accordion';

    for (const note of arr) {
      const details = document.createElement('details');
      const summary = document.createElement('summary');
      summary.textContent = `${note.date} — ${note.topic}`;
      details.appendChild(summary);

      const body = document.createElement('div');
      body.className = 'note-body';
      details.appendChild(body);

      const links = document.createElement('div');
      links.className = 'note-links';
      links.innerHTML = `<a href="${note.file}" target="_blank">Open raw Markdown ↗</a>`;
      details.appendChild(links);

      details.addEventListener('toggle', async () => {
        if (!details.open || body.dataset.loaded) return;
        try {
          const res = await fetch(note.file, { cache: 'no-store' });
          const md = await res.text();
          body.innerHTML = window.marked ? marked.parse(md) : `<pre>${escapeHtml(md)}</pre>`;
          body.dataset.loaded = '1';
        } catch (e) {
          body.innerHTML = `<div class="bad-link">Could not load: ${note.file}</div>`;
          body.dataset.loaded = '1';
        }
      });

      wrap.appendChild(details);
    }

    section.appendChild(wrap);
    frag.appendChild(section);
  }

  root.innerHTML = '';
  root.appendChild(frag);
}

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
}
