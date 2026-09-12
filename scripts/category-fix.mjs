import fs from 'node:fs';

const file = 'data/posts.json';
const posts = JSON.parse(fs.readFileSync(file, 'utf8'));

// 제목/URL/본문은 건드리지 않고, 검토가 끝난 명확한 오분류만 교정합니다.
const fixes = new Map([
  ['naver-224258681142', '부동산등기'],
]);

let changed = 0;
for (const post of posts) {
  const next = fixes.get(post.slug);
  if (next && post.category !== next) {
    console.log(`[category] ${post.slug}: ${post.category} -> ${next}`);
    post.category = next;
    changed++;
  }
}

if (changed) {
  fs.writeFileSync(file, JSON.stringify(posts, null, 2) + '\n', 'utf8');
}
console.log(`Category fixes: ${changed}`);
