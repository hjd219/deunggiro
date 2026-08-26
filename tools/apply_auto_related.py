from pathlib import Path
import re

pages = {
    'inheritance.html': ('상속등기', '상속'),
    'renunciation.html': ('상속포기·한정승인', '상속포기'),
    'corporate.html': ('법인등기', '법인'),
    'realestate.html': ('부동산등기', '부동산'),
    'family.html': ('가사', '가사'),
}

script_template = '''\n<script>\n(function(){\n  const box=document.getElementById("auto-related-posts");\n  if(!box) return;\n  const category=box.dataset.category;\n  const badge=box.dataset.badge || category;\n  const esc=s=>String(s||"").replace(/[&<>\\"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;","\\\"":"&quot;","'":"&#039;"}[m]));\n  fetch("/data/posts.json?v="+Date.now(),{cache:"no-store"})\n    .then(r=>{if(!r.ok) throw new Error("posts"); return r.json()})\n    .then(posts=>{\n      const list=posts.filter(p=>p.category===category).sort((a,b)=>String(b.date||"").localeCompare(String(a.date||""))).slice(0,4);\n      if(!list.length){\n        box.innerHTML='<a href="/posts.html"><span class="related-badge">'+esc(badge)+'</span><span class="related-title">관련 법률정보 전체보기</span><span class="related-arrow">→</span></a>';\n        return;\n      }\n      box.innerHTML=list.map(p=>'<a href="/posts/'+encodeURIComponent(p.slug)+'.html"><span class="related-badge">'+esc(badge)+'</span><span class="related-title">'+esc(p.title)+'</span><span class="related-arrow">→</span></a>').join("");\n    })\n    .catch(()=>{box.innerHTML='<a href="/posts.html"><span class="related-badge">'+esc(badge)+'</span><span class="related-title">관련 법률정보 전체보기</span><span class="related-arrow">→</span></a>';});\n})();\n</script>\n'''

for filename, (category, badge) in pages.items():
    p = Path(filename)
    t = p.read_text(encoding='utf-8')
    t = re.sub(r'\n?<script>\s*\(function\(\)\{\s*const box=document\.getElementById\(["\']auto-related-posts["\']\);.*?</script>\s*', '\n', t, flags=re.S)
    pattern = r'<div class="related-posts-list"(?:\s+id="auto-related-posts"[^>]*)?>.*?</div><div class="related-posts-actions">'
    repl = (f'<div class="related-posts-list" id="auto-related-posts" data-category="{category}" data-badge="{badge}">' 
            f'<a href="/posts.html"><span class="related-badge">{badge}</span><span class="related-title">최신 관련 법률정보를 불러오는 중입니다.</span><span class="related-arrow">→</span></a></div>'
            '<div class="related-posts-actions">')
    t2, n = re.subn(pattern, repl, t, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError(f'{filename}: related-posts-list not found')
    t = t2.replace('</body>', script_template + '\n</body>', 1)
    p.write_text(t, encoding='utf-8')
