/* DG_FEEDBACK_V1: per-post and tool helpfulness ratings stored in Firestore.
   Stores aggregated yes/no votes only; no document fields, form data, or personal details. */
(function () {
  'use strict';
  if (window.__DGFeedbackLoaded) return;
  window.__DGFeedbackLoaded = true;
  var PROJECT = 'project-b08e5f3c-fa49-4ae6-933';
  var DATABASE = 'default';
  var API_KEY = 'AIzaSyAlXYOrj7V-XtDrK13Cbxw6hWzbfhGf_do';
  var ENDPOINT = 'https://firestore.googleapis.com/v1/projects/' +
    encodeURIComponent(PROJECT) + '/databases/' + encodeURIComponent(DATABASE) +
    '/documents:commit?key=' + encodeURIComponent(API_KEY);

  function makeStyle() {
    if (document.querySelector('link[data-dg-feedback-style]')) return;
    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/assets/feedback-v1.css?v=20261025-2';
    link.setAttribute('data-dg-feedback-style', '1');
    document.head.appendChild(link);
  }
  function voteId(kind, value) {
    var clean = String(value || '').toLowerCase().replace(/[^a-z0-9_-]/g, '-')
      .replace(/-+/g, '-').replace(/^-|-$/g, '').slice(0, 130);
    if (!clean) return null;
    return kind + '-' + clean;
  }
  function choiceSaved(key) {
    try { return localStorage.getItem('dg_feedback_v1:' + key) || ''; }
    catch (_) { return ''; }
  }
  function remember(key, choice) {
    try { localStorage.setItem('dg_feedback_v1:' + key, choice); } catch (_) {}
  }
  async function sendVote(key, choice) {
    var name = 'projects/' + PROJECT + '/databases/' + DATABASE + '/documents/feedback/' + key;
    var field = choice === 'yes' ? 'helpful' : 'unhelpful';
    var body = { writes: [{
      transform: {
        document: name,
        fieldTransforms: [{ fieldPath: field, increment: { integerValue: '1' } }]
      }
    }] };
    var controller = new AbortController();
    var timer = setTimeout(function () { controller.abort(); }, 12000);
    try {
      var response = await fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: controller.signal,
        cache: 'no-store'
      });
      if (!response.ok) throw new Error('Firestore write HTTP ' + response.status);
      var payload = await response.json();
      if (!payload || !Array.isArray(payload.writeResults) || !payload.writeResults.length) {
        throw new Error('Unexpected Firestore write response');
      }
    } finally {
      clearTimeout(timer);
    }
  }
  function widget(kind, id, label) {
    var existing = choiceSaved(id);
    var box = document.createElement('section');
    box.className = 'dg-feedback';
    box.setAttribute('data-dg-feedback-kind', kind);
    box.setAttribute('data-dg-feedback-id', id);
    box.setAttribute('aria-label', '이용자 평가');
    var title = document.createElement('p');
    title.className = 'dg-feedback-title';
    title.textContent = label;
    var choices = document.createElement('div');
    choices.className = 'dg-feedback-choices';
    var status = document.createElement('p');
    status.className = 'dg-feedback-note';
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    var buttons = {};
    // Small outlined icons instead of emoji; match the rest of the site's clean blue design.
    var icons = {
      yes: '<path d="M7 10v12"/><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H5a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 3a3.13 3.13 0 0 1 3 2.88Z"/>',
      no: '<path d="M17 14V2"/><path d="M9 18.12 10 14H4.17a2 2 0 0 1-1.92-2.56l2.33-8A2 2 0 0 1 6.5 2H19a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.76a2 2 0 0 0-1.79 1.11L12 21a3.13 3.13 0 0 1-3-2.88Z"/>'
    };
    [['yes', '도움됐어요'], ['no', '아쉬워요']].forEach(function (item) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'dg-feedback-btn';
      btn.innerHTML = '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="display:block;flex:none">' + icons[item[0]] + '</svg><span>' + item[1] + '</span>';
      btn.setAttribute('aria-pressed', 'false');
      btn.setAttribute('aria-label', item[1]);
      buttons[item[0]] = btn;
      choices.appendChild(btn);
    });
    var busy = false;
    function paint(value) {
      Object.keys(buttons).forEach(function (choice) {
        buttons[choice].disabled = busy || Boolean(value);
        buttons[choice].setAttribute('aria-pressed', String(value === choice));
      });
      if (value) status.textContent = '평가해 주셔서 감사합니다.';
    }
    Object.keys(buttons).forEach(function (choice) {
      buttons[choice].addEventListener('click', async function () {
        if (busy || existing || choiceSaved(id)) return;
        busy = true;
        status.textContent = '평가를 저장하는 중입니다.';
        paint('');
        try {
          await sendVote(id, choice);
          remember(id, choice);
          existing = choice;
          busy = false;
          paint(existing);
        } catch (error) {
          busy = false;
          status.textContent = '평가를 저장하지 못했습니다. 다시 시도해 주세요.';
          paint('');
          console.warn('[DGFeedback] Firestore write failed:', error && error.message);
        }
      });
    });
    box.appendChild(title);
    box.appendChild(choices);
    box.appendChild(status);
    paint(existing);
    if (!existing) status.textContent = '서비스 개선을 위한 간단한 평가입니다.';
    return box;
  }
  function onArticle() {
    var match = location.pathname.match(/^\/posts\/([^/]+)\.html$/i);
    if (!match) return false;
    var article = document.querySelector('main article, article.article, .post-article, article');
    if (!article) return false;
    if (article.querySelector('.dg-feedback')) return true;
    var slug = '';
    try { slug = decodeURIComponent(match[1]); } catch (_) { slug = match[1]; }
    var id = voteId('post', slug);
    if (!id) return false;
    var box = widget('post', id, '이 글이 도움이 되셨나요?');
    // Place directly after the legal article text, before core links, related posts or consultation CTAs.
    var articleBody = article.querySelector('.article-body');
    if (articleBody && articleBody.parentNode) articleBody.insertAdjacentElement('afterend', box);
    else {
      var related = article.querySelector('.seo-core-link,.dg-topic-cta,.seo-related-posts,.related');
      if (related && related.parentNode) related.parentNode.insertBefore(box, related);
      else article.appendChild(box);
    }
    return true;
  }
  function onCalculator() {
    var path = location.pathname;
    var type = {
      '/acquisition-calculator.html': 'acquisition',
      '/corporate-calculator.html': 'corporate',
      '/renunciation-calculator.html': 'renunciation'
    }[path];
    if (!type) return false;
    var root = document.querySelector('#resultPanel, .calculator-flow aside.result');
    if (!root) return false;
    if (root.querySelector('.dg-feedback')) return true;
    var box = widget('calculator', voteId('calc', type), '이 계산기가 도움이 되셨나요?');
    var actions = root.querySelector('.actions');
    if (actions) actions.insertAdjacentElement('afterend', box);
    else root.appendChild(box);
    return true;
  }
  function onWriter() {
    var inheritance = location.pathname === '/inheritance.html';
    var divorce = location.pathname === '/family.html';
    if (!inheritance && !divorce) return false;
    var root = document.querySelector(inheritance ? '#dg-inherit-agreement .dg-agr-panel' : '#dg-divorce-chapter .dg-tool');
    if (!root) return false;
    if (root.querySelector('.dg-feedback')) return true;
    var box = widget('writer', voteId('writer', inheritance ? 'inheritance' : 'divorce'),
      '이 자동작성기가 도움이 되셨나요?');
    var lastAction = root.querySelector(inheritance ? '.dg-agr-actions' : '.dg-actions');
    if (lastAction) lastAction.insertAdjacentElement('afterend', box);
    else root.appendChild(box);
    box.hidden = true;
    var watch = document.querySelector(inheritance ? '#dg-agr-step' : '#dg-wiz-title');
    if (!watch) return true;
    var update = function () {
      box.hidden = inheritance ? !/4단계/.test(watch.textContent || '')
        : !/출력 및 저장 안내/.test(watch.textContent || '');
    };
    var observer = new MutationObserver(update);
    observer.observe(watch, { childList: true, characterData: true, subtree: true });
    update();
    return true;
  }
  function init() {
    if (document.querySelector('[data-dg-feedback-id]')) return;
    var path = location.pathname;
    if (!/^\/posts\/[^/]+\.html$/i.test(path) &&
        !/^(\/(acquisition|corporate|renunciation)-calculator\.html|\/(inheritance|family)\.html)$/.test(path)) return;
    makeStyle();
    if (!onArticle() && !onCalculator()) onWriter();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();