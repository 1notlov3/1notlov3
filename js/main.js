/* kcalm — The Listening Pool
   Only what speech touches is allowed to glow. */
(() => {
  'use strict';

  const init = () => {
    const $ = (s, c) => (c || document).querySelector(s);
    const $$ = (s, c) => [...(c || document).querySelectorAll(s)];
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const easeOut = t => 1 - Math.pow(1 - t, 3);
    const fmt = n => Math.round(n).toLocaleString('en-US');

    /* ---------- nav scrim ---------- */
    const nav = $('#nav');
    const onScroll = () => nav.classList.toggle('scrimmed', scrollY > 24);
    addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    /* ---------- the pool (hero canvas) ---------- */
    const hero = $('#hero');
    const canvas = $('#pool');
    const ctx = canvas.getContext('2d');
    const pearl = $('#pearl');

    let W = 0, H = 0, DPR = 0, cx = 0, cy = 0;
    let baseGrad = null;
    let ripples = [];
    let glowBoost = 0;
    let running = false, heroVisible = false, rafId = 0;
    let lastFrame = 0;
    const t0 = performance.now();

    function resize() {
      const r = hero.getBoundingClientRect();
      const dpr = Math.min(devicePixelRatio || 1, 2);
      const dimsChanged = r.width !== W || r.height !== H || dpr !== DPR;
      W = r.width; H = r.height; DPR = dpr;
      if (dimsChanged) {
        canvas.width = W * DPR; canvas.height = H * DPR;
        ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      }
      const p = pearl.getBoundingClientRect();
      cx = p.left - r.left + p.width / 2;
      cy = p.top - r.top + p.height / 2;
      const R = Math.max(W, H) * 0.75;
      baseGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, R);
      baseGrad.addColorStop(0, 'rgba(246,184,75,0.34)');
      baseGrad.addColorStop(0.25, 'rgba(255,142,79,0.16)');
      baseGrad.addColorStop(0.6, 'rgba(255,142,79,0.04)');
      baseGrad.addColorStop(1, 'rgba(0,0,0,0)');
      if (reduced) drawFrame(t0, 0);
    }

    function ripple(x, y, strength = 1) {
      if (reduced) return;
      if (ripples.length > 42) ripples.shift();
      ripples.push({ x, y, r: 6, v: 1.4 + strength * 0.9, a: 0.28 * strength, w: 1.25 + strength });
    }

    function drawFrame(now, dt) {
      ctx.clearRect(0, 0, W, H);
      const breathe = 0.5 + 0.5 * Math.sin((now - t0) / 4000 * Math.PI * 2);
      const base = Math.min(0.10 + breathe * 0.05 + glowBoost, 1);

      // the pool's resting glow — warm light under dark water
      ctx.globalAlpha = base;
      ctx.fillStyle = baseGrad;
      ctx.fillRect(0, 0, W, H);
      ctx.globalAlpha = 1;

      // ripples — light radiating from speech
      ctx.globalCompositeOperation = 'lighter';
      for (const p of ripples) {
        p.r += p.v * dt; p.a *= Math.pow(0.972, dt);
        const grad = ctx.createRadialGradient(p.x, p.y, Math.max(p.r - 14, 0), p.x, p.y, p.r + 14);
        grad.addColorStop(0, 'rgba(246,184,75,0)');
        grad.addColorStop(0.5, `rgba(246,184,75,${p.a})`);
        grad.addColorStop(1, 'rgba(255,142,79,0)');
        ctx.strokeStyle = grad;
        ctx.lineWidth = p.w;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.stroke();
      }
      ctx.globalCompositeOperation = 'source-over';
      ripples = ripples.filter(p => p.a > 0.004);
      glowBoost *= Math.pow(0.94, dt);
    }

    let lastAuto = 0;
    function loop(now) {
      if (!running) return;
      const dt = lastFrame ? Math.min((now - lastFrame) / 16.67, 3) : 1;
      lastFrame = now;
      if (now - lastAuto > 3400) {           // the pool is alive, faintly
        lastAuto = now;
        ripple(cx + (Math.sin(now / 700) * W) / 6, cy + (Math.cos(now / 900) * H) / 14, 0.35);
      }
      drawFrame(now, dt);
      rafId = requestAnimationFrame(loop);
    }
    function setRunning(on) {
      if (reduced) { drawFrame(t0, 0); return; }
      if (on && !running) { running = true; lastFrame = 0; rafId = requestAnimationFrame(loop); }
      if (!on && running) { running = false; cancelAnimationFrame(rafId); }
    }

    addEventListener('resize', resize);
    new IntersectionObserver(([e]) => {
      heroVisible = e.isIntersecting;
      setRunning(heroVisible && !document.hidden);
    }, { threshold: 0.02 }).observe(hero);
    document.addEventListener('visibilitychange', () => setRunning(!document.hidden && heroVisible));

    // pointer stirs the water, gently
    let lastMove = 0;
    hero.addEventListener('pointermove', e => {
      const now = performance.now();
      if (now - lastMove < 110) return;
      lastMove = now;
      const r = hero.getBoundingClientRect();
      ripple(e.clientX - r.left, e.clientY - r.top, 0.3);
    }, { passive: true });

    /* ---------- count-up (cancellable per element) ---------- */
    function countTo(el, to, dur = 700, from = 0) {
      const suffix = el.dataset.suffix || '';
      const id = el._countId = (el._countId || 0) + 1;
      if (reduced) { el.textContent = fmt(to) + suffix; return; }
      const start = performance.now();
      const tick = now => {
        if (el._countId !== id) return;
        const t = Math.min((now - start) / dur, 1);
        el.textContent = fmt(from + (to - from) * easeOut(t)) + suffix;
        if (t < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }

    /* ---------- animated numbers: keep truth in the a11y tree ---------- */
    $$('.kcal-num[data-to], .stat-num[data-to]').forEach(el => {
      const sr = document.createElement('span');
      sr.className = 'sr-only';
      sr.textContent = el.textContent;
      el.setAttribute('aria-hidden', 'true');
      el.after(sr);
      if (!reduced) el.textContent = '0' + (el.dataset.suffix ? el.dataset.suffix : '');
    });

    /* ---------- hero title: words resolve like live captions ---------- */
    const title = $('#heroTitle');
    const words = title.textContent.split(' ');
    title.textContent = '';
    words.forEach((w, i) => {
      const s = document.createElement('span');
      s.className = 'w';
      s.textContent = w;
      title.appendChild(s);
      if (i < words.length - 1) title.appendChild(document.createTextNode(' '));
    });
    let titleShown = false;
    const showTitle = () => {
      if (titleShown) return;
      titleShown = true;
      $$('.w', title).forEach((s, i) =>
        setTimeout(() => s.classList.add('in'), reduced ? 0 : 250 + i * 90));
    };
    (document.fonts?.ready || Promise.resolve()).then(showTitle).catch(showTitle);
    setTimeout(showTitle, 1400); // fallback if fonts hang

    /* ---------- the pearl: scripted voice log ---------- */
    const spokenLine = $('#spokenLine');
    const demoStatus = $('#demoStatus');
    const heroCard = $('#heroCard');
    const heroKcal = $('#heroKcal');
    const pearlLabel = $('.pearl-label', pearl);
    const LINE = ['“One', 'chicken', 'burrito,', 'extra', 'guac.”'];
    let playing = false, played = false;

    function playDemo() {
      if (playing) return;
      playing = true;
      spokenLine.textContent = '';
      demoStatus.textContent = '';
      heroCard.classList.remove('in');
      heroCard.hidden = true;
      pearl.classList.add('listening');

      const wordGap = reduced ? 0 : 320;
      LINE.forEach((w, i) => {
        setTimeout(() => {
          const s = document.createElement('span');
          s.className = 'w';
          s.textContent = (i ? ' ' : '') + w;
          spokenLine.appendChild(s);
          requestAnimationFrame(() => requestAnimationFrame(() => s.classList.add('in')));
          ripple(cx, cy, 1.6);
        }, 350 + i * wordGap);
      });

      const settle = 350 + LINE.length * wordGap + (reduced ? 50 : 500);
      setTimeout(() => {
        pearl.classList.remove('listening');
        if (!reduced) glowBoost = 0.9;       // the light condenses…
        ripple(cx, cy, 2.4);
      }, settle);
      setTimeout(() => {
        heroCard.hidden = false;             // …and becomes the meal
        requestAnimationFrame(() => requestAnimationFrame(() => heroCard.classList.add('in')));
        countTo(heroKcal, +heroKcal.dataset.to, 750);
        demoStatus.textContent = 'Heard: “One chicken burrito, extra guac.” Logged — 812 kcal: protein 42 grams, carbs 71 grams, fat 40 grams.';
        playing = false;
        if (!played) {
          played = true;
          pearlLabel.innerHTML = 'Tap to<br>replay';
        }
        resize();                            // card changed layout → recentre glow
      }, settle + (reduced ? 60 : 420));
    }
    pearl.addEventListener('click', playDemo);

    // the closing pearl replays the magic, upstairs
    $('#pearlEnd').addEventListener('click', () => {
      let done = false;
      const go = () => {
        if (done) return;
        done = true;
        pearl.focus({ preventScroll: true });
        playDemo();
      };
      if (!reduced && 'onscrollend' in window) addEventListener('scrollend', go, { once: true });
      hero.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' });
      setTimeout(go, reduced ? 100 : 1100);
    });

    /* ---------- scroll reveals ---------- */
    $$('.section').forEach(sec =>
      $$('.reveal', sec).forEach((el, i) => el.style.setProperty('--d', Math.min(i, 6) * 70 + 'ms')));

    const revealIO = new IntersectionObserver(entries => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        e.target.classList.add('in');
        revealIO.unobserve(e.target);
        const num = e.target.querySelector('.kcal-num[data-to], .stat-num[data-to]');
        if (num && !num.dataset.done) {
          num.dataset.done = '1';
          countTo(num, +num.dataset.to, 900);
        }
      }
    }, { threshold: 0.25, rootMargin: '0px 0px -5% 0px' });
    $$('.reveal').forEach(el => revealIO.observe(el));

    /* ---------- the correction ---------- */
    const correction = $('#correction');
    const fixKcal = $('#fixKcal');
    const fixSr = fixKcal.nextElementSibling;   // the sr-only 510
    let fixTimer = 0;
    fixKcal.textContent = '550';                // pre-correction state (JS path only)

    function playFix() {
      clearTimeout(fixTimer);
      fixKcal._countId = (fixKcal._countId || 0) + 1;  // cancel any in-flight count
      correction.classList.remove('played');
      fixKcal.textContent = '550';
      fixSr.textContent = '510';
      void correction.offsetWidth;             // restart the CSS strikethrough
      fixTimer = setTimeout(() => {
        correction.classList.add('played');
        fixTimer = setTimeout(() => countTo(fixKcal, 510, 650, 550), reduced ? 0 : 450);
      }, reduced ? 0 : 500);
    }
    new IntersectionObserver(([e], io) => {
      if (e.isIntersecting) { playFix(); io.disconnect(); }
    }, { threshold: 0.45 }).observe(correction);
    $('#replayFix').addEventListener('click', playFix);

    resize();
    (document.fonts?.ready || Promise.resolve()).then(resize).catch(resize);
  };

  try {
    init();
  } catch (err) {
    // fail open: without JS enhancements the document is complete on its own
    document.documentElement.classList.remove('js');
    console.error(err);
  }
})();
