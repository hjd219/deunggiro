/** Keep five practice-page article links crawlable without rewriting page content.
 *  Only the existing dg-blog-track children and its item count may change.
 *  The visual layout stays governed by the existing two-line CSS clamp.
 */
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const groups = [
  ['inheritance.html', ['상속등기', '상속재산분할']],
  ['renunciation.html', ['상속포기·한정승인']],
  ['corporate.html', ['법인등기']],
  ['realestate.html', ['부동산등기']],
  ['family.html', ['가사']],
];
const posts = JSON.parse(fs.readFileSync(path.join(root, 'data/posts.json'), 'utf8'));
if (!Array.isArray(posts)) throw Error('posts.json must be an array');
const esc = value => String(value ?? '').replace(/[&<>"']/g, ch =>
  ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[ch]));
// Keep substantive title text intact, excluding only leading category badges.
const displayTitle = value => {
  const raw = String(value ?? '').trim();
  return raw.replace(/^\s*(?:\[[^\]]{1,45}\]\s*)+/g, '')
    .replace(/^\s*\(처리사례\)\s*/, '').replace(/\s+/g, ' ').trim() || raw;
};
const card = p => {
  const title = esc(p.title), date = esc(p.date), slug = esc(p.slug);
  const thumbnail = esc(p.thumbnail || '/assets/posts/' + p.slug + '-thumbnail.png');
  return '<a class="dg-blog-card" href="/posts/' + slug + '.html" aria-label="' + title + '">'
    + '<img class="dg-blog-thumb" loading="lazy" decoding="async" src="' + thumbnail
    + '" alt="" onerror="this.onerror=null;this.src=\'/favicon.png\'">'
    + '<div class="dg-blog-card-content"><time datetime="' + date + '">' + date + '</time>'
    + '<h3 title="' + title + '">' + esc(displayTitle(p.title)) + '</h3></div></a>';
};
const trackRe = /(<div class="dg-blog-track"[^>]*>)([\s\S]*?)(<\/div><p class="dg-blog-note")/g;
const countRe = /(<span class="dg-blog-status" aria-live="polite">)\d+개 글(<\/span>)/g;
const protectedPart = s => s.replace(trackRe, '$1__ONLY_CARDS__$3')
  .replace(countRe, '$1__ONLY_COUNT__$2');
const seenSlugs = new Set();
for (const p of posts) {
  if (!p || !/^[\w-]+$/.test(p.slug || '') || !p.title || !p.date)
    throw Error('Invalid post metadata: ' + JSON.stringify(p).slice(0, 180));
  if (seenSlugs.has(p.slug)) throw Error('Duplicate slug: ' + p.slug);
  seenSlugs.add(p.slug);
}
let changed = 0;
for (const [filename, categories] of groups) {
  const filenameFull = path.join(root, filename);
  const original = fs.readFileSync(filenameFull, 'utf8');
  const items = posts.filter(p => categories.includes(p.category));
  if (!items.length) throw Error('No posts for ' + filename);
  for (const p of items) {
    if (!fs.existsSync(path.join(root, 'posts', p.slug + '.html')))
      throw Error('Missing post HTML: ' + p.slug);
  }
  const tracks = [...original.matchAll(trackRe)];
  const counts = [...original.matchAll(countRe)];
  if (tracks.length !== 1 || counts.length !== 1)
    throw Error('Unexpected card track or counter in ' + filename);
  let next = original.replace(trackRe, (_all, start, _old, end) =>
    start + items.map(card).join('') + end);
  next = next.replace(countRe, (_all, start, end) => start + items.length + '개 글' + end);
  if (protectedPart(original) !== protectedPart(next))
    throw Error('Attempt to edit outside cards/counter in ' + filename);
  if (next !== original) {
    fs.writeFileSync(filenameFull, next, 'utf8');
    changed += 1;
  }
  console.log('SERVICE_BLOG_SYNC', filename, 'cards=' + items.length,
    'changed=' + (next !== original));
}
console.log('SERVICE_BLOG_SYNC_DONE', changed);
