const isDarkMode = () => {
  return window.matchMedia('(prefers-color-scheme: dark)').matches;
};

/* ===========================
   Notes Page Builder (STATIC)
   =========================== */

const NOTES = [
  {
    course: "CS2420",
    date: "2024-09-05",
    topic: "First Lecture - Big O, and Complexity",
    file: "doc/Notes/9-5-24.md"
  },
  {
    course: "CS2420",
    date: "2024-09-10",
    topic: "Binary Search Tree",
    file: "doc/Notes/9-10-24.md"
  },
  {
    course: "CS2420",
    date: "2024-09-12",
    topic: "Binary Search Trees and AVL Trees",
    file: "doc/Notes/9-12-24.md"
  },
  {
    course: "CS2420",
    date: "2024-09-17",
    topic: "AVL Trees Continued... and Splay Trees",
    file: "doc/Notes/9-17-24.md"
  },
  {
    course: "CS2420",
    date: "2024-09-24",
    topic: "Hashing/Hash Tables",
    file: "doc/Notes/9-24-24.md"
  },
  {
    course: "CS2420",
    date: "2024-10-08",
    topic: "Priority Queues and Heaps",
    file: "doc/Notes/10-8-24.md"
  },
    {
    course: "CS2420",
    date: "2024-10-10",
    topic: "More Heaps",
    file: "doc/Notes/10-10-24.md"
  },
    {
    course: "CS2420",
    date: "2024-10-22",
    topic: "Up-Tree",
    file: "doc/Notes/10-22-24.md"
  },
    {
    course: "CS2420",
    date: "2024-10-29",
    topic: "Graphs",
    file: "doc/Notes/10-29-24.md"
  },
      {
    course: "CS2420",
    date: "2024-11-05",
    topic: "Graph Algorithms",
    file: "doc/Notes/11-5-24.md"
  },

  {
    course: "CS2420",
    date: "2024-11-21",
    topic: "Greedy Algorithms",
    file: "doc/Notes/11-21-24.md"
  },

    {
    course: "CS2610",
    date: "2025-08-25",
    topic: "First Lecture",
    file: "CS2610/Notes/8-27-25.md"
  },
    {
    course: "CS2810",
    date: "2025-08-25",
    topic: "First Lecture",
    file: "CS2810/Notes/8-25-25.md"
  },
      {
    course: "CS2810",
    date: "2025-08-27",
    topic: "Boolean Algebra",
    file: "CS2810/Notes/8-27-25.md"
  },
        {
    course: "CS2810",
    date: "2025-08-29",
    topic: "Logic Gates",
    file: "CS2810/Notes/8-29-25.md"
  },

          {
    course: "CS2810",
    date: "2025-09-03",
    topic: "Logic Gates",
    file: "CS2810/Notes/9-3-25.md"
  },

      {
    course: "CS2610",
    date: "2025-09-04",
    topic: "Ports, Sockets, Protocols, Advanced Python",
    file: "CS2610/Notes/9-4-25.md"
  },
            {
    course: "CS2810",
    date: "2025-09-05",
    topic: "Boolean Arithmetic",
    file: "CS2810/Notes/9-5-25.md"
  },
              {
    course: "CS2610",
    date: "2025-09-06",
    topic: "Advanced Python",
    file: "CS2610/Notes/9-6-25.md"
  },
  
  // Add more notes here...
];

// Format YYYY-MM-DD → "Month DD, YYYY"
// Format YYYY-MM-DD → "Month DD, YYYY"
function formatDate(dateString) {
  // Expect input like "2024-09-05" (YYYY-MM-DD)
  const [year, month, day] = dateString.split('-').map(Number);

  // Subtract 1 from month because JS Date months are 0-based
  const dateObj = new Date(year, month - 1, day);

  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return dateObj.toLocaleDateString('en-US', options);
}



// Entry point called by notes.html
async function buildNotesPage() {
  const root = document.getElementById('notes-root');
  if (!root) return;

  // Group by course
  const byCourse = new Map();
  for (const n of NOTES) {
    if (!byCourse.has(n.course)) byCourse.set(n.course, []);
    byCourse.get(n.course).push(n);
  }

  // Sort newest → oldest
  for (const [, arr] of byCourse) {
    arr.sort((a, b) => b.date.localeCompare(a.date));
  }

  const frag = document.createDocumentFragment();

  for (const [course, arr] of byCourse) {
    const section = document.createElement('section');

    // Brown title bar
    const titleEl = document.createElement('h2');
    titleEl.className = 'titles';
    titleEl.textContent = `${course} Notes`;
    section.appendChild(titleEl);

    // Each note gets its own white box
    for (const note of arr) {
      const box = document.createElement('div');
      box.className = 'contact-info note-box';  // adds note-box class


      const details = document.createElement('details');

      const summary = document.createElement('summary');
      summary.textContent = `${formatDate(note.date)} — ${note.topic}`;
      details.appendChild(summary);

      const body = document.createElement('div');
      body.className = 'note-body';
      details.appendChild(body);

      const links = document.createElement('div');
      links.className = 'note-links';
      links.innerHTML = `<a href="${note.file}" target="_blank">Open raw Markdown ↗</a>`;
      details.appendChild(links);

      // Lazy-load & render Markdown on first open
      details.addEventListener('toggle', async () => {
        if (!details.open || body.dataset.loaded) return;
        try {
          const url = new URL(note.file, document.baseURI).toString();
          const res = await fetch(url, { cache: 'no-store' });
          if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
          const md = await res.text();
          body.innerHTML = (window.marked ? marked.parse(md) : `<pre>${escapeHtml(md)}</pre>`);
          body.dataset.loaded = '1';
        } catch (e) {
          console.error('Markdown fetch failed:', e);
          body.innerHTML = `<div class="bad-link">Could not load: ${note.file}</div>`;
          body.dataset.loaded = '1';
        }
      });

      box.appendChild(details);
      section.appendChild(box);
    }

    frag.appendChild(section);
  }

  root.innerHTML = '';
  root.appendChild(frag);
}

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
}
