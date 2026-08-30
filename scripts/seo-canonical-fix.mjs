import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const BASE = 'https://www.deunggiro.kr';
const postsPath = path.join(root, 'data', 'posts.json');
const reportPath = path.join(root, 'data', 'seo-report.json');

const posts = JSON.parse(fs.readFileSync(postsPath, 'utf8'));

function hasCanonical(html) {
  return /<link\b(?=[^>]*\brel=["'][^"']*\bcanonical\b[^"']*["'])(?=[^>]*\bhref=["'][^"']+["'])[^>]*>/i.test(html);
}

function ensureCanonical(html, url) {
  const tag = `<link rel="canonical" href="${url}">`;
  const canonicalAnyOrder = /<link\b(?=[^>]*\brel=["'][^"']*\bcanonical\b[^"']*["'])[^>]*>/i;
  if (canonicalAnyOrder.test(html)) return html.replace(canonicalAnyOrder, tag);
  return html.replace(/<\/head>/i, `${tag}\n</head>`);
}

let fixed = 0;
let missingFiles = 0;
for (const p of posts) {
  const slug = String(p?.slug || '').replace(/\.html$/i, '');
  if (!slug) continue;
  const file = path.join(root, 'posts', `${slug}.html`);
  if (!fs.existsSync(file)) {
    missingFiles++;
    continue;
  }
  const url = `${BASE}/posts/${slug}.html`;
  const before = fs.readFileSync(file, 'utf8');
  const after = ensureCanonical(before, url);
  if (after !== before) {
    fs.writeFileSync(file, after);
    fixed++;
  }
}

let ok = 0;
let warnings = 0;
const items = [];
for (const p of posts) {
  const slug = String(p?.slug || '').replace(/\.html$/i, '');
  if (!slug) continue;
  const file = path.join(root, 'posts', `${slug}.html`);
  const issues = [];
  if (!fs.existsSync(file)) {
    issues.push('HTML 파일 없음');
  } else {
    const html = fs.readFileSync(file, 'utf8');
    if (!hasCanonical(html)) issues.push('canonical 누락');
    if (!/<meta\b(?=[^>]*\bname=["']description["'])(?=[^>]*\bcontent=["'][^"']+["'])[^>]*>/i.test(html)) issues.push('description 누락');
    if (/<meta\b(?=[^>]*\bname=["']robots["'])[^>]*\bcontent=["'][^"']*noindex/i.test(html)) issues.push('noindex 발견');
    if (!/"@type"\s*:\s*"Article"/.test(html)) issues.push('Article 구조화데이터 누락');
    if (!/"@type"\s*:\s*"BreadcrumbList"/.test(html)) issues.push('Breadcrumb 구조화데이터 누락');
  }
  if (issues.length) warnings++; else ok++;
  items.push({ slug, status: issues.length ? 'warning' : 'ok', issues });
}

const report = {
  generatedAt: new Date().toISOString(),
  totalPosts: items.length,
  ok,
  warnings,
  canonicalFixed: fixed,
  missingFiles,
  items
};
fs.writeFileSync(reportPath, JSON.stringify(report, null, 2) + '\n');
console.log(`canonical 점검 완료: ${items.length}개 / 정상 ${ok} / 경고 ${warnings} / 보정 ${fixed}`);
