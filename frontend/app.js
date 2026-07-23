/* ─────────────────────────────────────────────
   app.js — WeddingOS v2.0 main application
   Typewriter boot sequence → confetti → card
   ───────────────────────────────────────────── */

"use strict";

// ── Configuration ────────────────────────────────────────────────────────────
const CONFIG = {
  names:      "Kriszti & Gabor",
  commitDate: "2026-07-25",
  author:     "Your Friends",
  typeDelay:  28,          // ms per character in typewriter
  lineGap:    220,         // ms between lines appearing
  barDuration: 1600,       // ms to fill a progress bar
};

// ── Helpers ───────────────────────────────────────────────────────────────────
const sleep = ms => new Promise(r => setTimeout(r, ms));

function qs(sel) { return document.querySelector(sel); }

/** Append a new div.line to #content and return it */
function addLine(html = "", cssClass = "") {
  const div = document.createElement("div");
  div.className = "line" + (cssClass ? " " + cssClass : "");
  div.innerHTML = html;
  qs("#content").appendChild(div);
  return div;
}

/** Make a line visible (fade + slide) */
function show(el) {
  // force reflow so transition fires
  el.offsetHeight; // eslint-disable-line no-unused-expressions
  el.classList.add("visible");
  qs("#content").scrollTop = qs("#content").scrollHeight;
}

/** Animate a progress bar from 0 → 100% in barDuration ms */
function animateBar(fillEl, labelEl, duration = CONFIG.barDuration) {
  return new Promise(resolve => {
    const start = performance.now();
    function tick(now) {
      const pct = Math.min(100, ((now - start) / duration) * 100);
      fillEl.style.width = pct + "%";
      if (labelEl) labelEl.textContent = Math.floor(pct) + "%";
      if (pct < 100) {
        requestAnimationFrame(tick);
      } else {
        resolve();
      }
    }
    requestAnimationFrame(tick);
  });
}

/** Typewriter effect: resolve when text fully printed */
function typewriter(el, text, delay = CONFIG.typeDelay) {
  return new Promise(resolve => {
    let i = 0;
    const cursor = document.createElement("span");
    cursor.className = "cursor";
    el.appendChild(cursor);

    function next() {
      if (i < text.length) {
        cursor.insertAdjacentText("beforebegin", text[i++]);
        setTimeout(next, delay + (Math.random() * delay * .4 - delay * .2));
      } else {
        cursor.remove();
        resolve();
      }
    }
    next();
  });
}

// ── Matrix background ─────────────────────────────────────────────────────────
(function initMatrix() {
  const canvas = qs("#matrix");
  const ctx    = canvas.getContext("2d");
  let cols, drops;

  function resize() {
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
    cols  = Math.floor(canvas.width / 20);
    drops = Array.from({ length: cols }, () => Math.random() * -50);
  }

  window.addEventListener("resize", resize);
  resize();

  setInterval(() => {
    ctx.fillStyle = "rgba(13,17,23,.18)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#3fb950";
    ctx.font = "14px monospace";
    drops.forEach((y, i) => {
      const ch = Math.random() < .5 ? "0" : "1";
      ctx.fillText(ch, i * 20, y * 20);
      if (y * 20 > canvas.height && Math.random() > .975) drops[i] = 0;
      else drops[i] += .45;
    });
  }, 55);
})();

// ── Sound toggle ──────────────────────────────────────────────────────────────
let soundEnabled = false;
qs("#soundtoggle").addEventListener("click", () => {
  soundEnabled = !soundEnabled;
  qs("#soundtoggle").textContent = soundEnabled ? "🔊" : "🔇";
  if (soundEnabled) {
    const audio = qs("#bootsound");
    audio.volume = .15;
    audio.play().catch(() => {}); // autoplay policy — silently ignore
  }
});

// ── Easter-egg commands ───────────────────────────────────────────────────────
const EASTER_COMMANDS = [
  ["help",              "Show available commands"],
  ["brew coffee",       "Brew a fresh pot of coffee ☕"],
  ["git hug",           "Hug the nearest person unconditionally"],
  ["deploy vacation",   "Schedule honeymoon deployment pipeline"],
  ["restart honeymoon", "Restart happily_ever_after() process"],
  ["git blame love",    "Author: <You two> — every commit"],
  ["sudo kiss",         "Permission granted — always"],
  ["ping happiness",    "PING happiness — 0% packet loss"],
];

function showHelp() {
  const box   = qs("#helpbox");
  const table = qs("#helptable");
  table.innerHTML = EASTER_COMMANDS.map(([cmd, desc]) =>
    `<span class="hcmd">${cmd}</span><span class="hdesc"># ${desc}</span>`
  ).join("");
  box.hidden = false;
}

qs("#helpclose").addEventListener("click", () => { qs("#helpbox").hidden = true; });
qs("#helpclose").addEventListener("keydown", e => {
  if (e.key === "Enter" || e.key === " ") qs("#helpbox").hidden = true;
});

function handleCommand(raw) {
  const cmd = raw.trim().toLowerCase();
  const contentEl = qs("#content");

  if (cmd === "help") {
    showHelp();
    addLine("", "");
    const l = addLine('<span class="ok">Available commands loaded. See help panel above.</span>');
    show(l);
    return;
  }

  const found = EASTER_COMMANDS.find(([c]) => c === cmd);
  if (found) {
    const l = addLine(`<span class="ok">✔ ${found[1]}</span>`);
    show(l);
    contentEl.scrollTop = contentEl.scrollHeight;
    return;
  }

  const l = addLine(`<span class="error">command not found: ${raw} — try 'help'</span>`);
  show(l);
  contentEl.scrollTop = contentEl.scrollHeight;
}

qs("#cmdinput").addEventListener("keydown", e => {
  if (e.key === "Enter") {
    const val = qs("#cmdinput").value;
    if (!val.trim()) return;
    const prompt = addLine(`<span class="prompt-text">$ ${val}</span>`);
    show(prompt);
    handleCommand(val);
    qs("#cmdinput").value = "";
  }
});

// ── Card reveal helpers ───────────────────────────────────────────────────────
async function revealCard() {
  const message = qs("#message");
  message.removeAttribute("aria-hidden");
  message.classList.add("show");

  await sleep(600);

  // Title
  const title = qs("#cardTitle");
  title.textContent = "❤️ Congratulations ❤️";
  title.classList.add("visible");

  await sleep(700);

  // Letter paragraphs
  const letterEl = qs("#letter");
  const paragraphs = [
    `Dear ${CONFIG.names},`,
    "Today you successfully merged two beautiful branches into one shared future.",
    "May your life always compile without errors,\nyour coffee never run out,\nand every challenge become just another solved bug.",
    "We wish you endless happiness, countless adventures,\nand a lifetime full of successful commits.",
  ];

  for (const text of paragraphs) {
    const p = document.createElement("p");
    p.style.whiteSpace = "pre-line";
    letterEl.appendChild(p);
    await sleep(100);
    p.classList.add("visible");
    await typewriter(p, text, 22);
    await sleep(280);
  }

  await sleep(400);

  // Commit block
  const commitEl = qs("#commit");
  commitEl.innerHTML = `
<span class="commit-hash">commit <span style="color:#d2a8ff">a2026b${CONFIG.commitDate.replace(/-/g,"")}</span></span>
<span class="commit-merged">MERGED</span>
<br>
<span class="dim">Author:</span> ${CONFIG.author}
<br>
<span class="commit-feat">feat: happily ever after</span>
<br>
<span class="dim">Date:</span> ${CONFIG.commitDate}`;
  commitEl.classList.add("visible");

  await sleep(700);

  // git status footer
  const gsEl = qs("#gitstatus");
  gsEl.innerHTML = `<span class="prompt-text">$ git status</span>
<span class="ok">On branch forever</span>

<span class="ok">nothing to commit,</span>
<span class="ok">working tree clean ❤️</span>`;
  gsEl.classList.add("visible");
}

// ── Main boot sequence ────────────────────────────────────────────────────────
async function boot() {
  const content = qs("#content");

  /** Helper: create line, show it, wait lineGap */
  async function line(html, cls, extraDelay = 0) {
    const el = addLine(html, cls);
    await sleep(80);
    show(el);
    await sleep(CONFIG.lineGap + extraDelay);
    return el;
  }

  /** Progress bar line */
  async function progressLine(labelText) {
    const wrapper = addLine("", "");
    wrapper.innerHTML = `
      <span>${labelText}</span>
      <div class="progress-wrap">
        <div class="progress-fill" id="pf_${Date.now()}"></div>
      </div>
      <span class="progress-label dim" id="pl_${Date.now()}">0%</span>`;
    show(wrapper);
    await sleep(120);
    const fill  = wrapper.querySelector(".progress-fill");
    const label = wrapper.querySelector(".progress-label");
    await animateBar(fill, label);
    content.scrollTop = content.scrollHeight;
    return wrapper;
  }

  // ── Sequence ────────────────────────────────────
  await sleep(400);
  await line('<span class="prompt-text">$ ./deploy_marriage.sh</span>', "", 50);
  await line("Initializing WeddingOS...", "", 50);
  await line("Loading crypto engine...", "", 50);
  await line("Loading relationship modules...", "", 100);
  await line('<span class="ok">✔ Love module loaded</span>',    "", 40);
  await line('<span class="ok">✔ Trust module loaded</span>',   "", 40);
  await line('<span class="ok">✔ Respect module loaded</span>', "", 40);
  await line('<span class="ok">✔ Humor module loaded</span>',   "", 40);
  await line('<span class="ok">✔ Coffee dependency satisfied</span>', "", 100);
  await line("", "");
  await line("Searching encrypted payload...", "", 60);
  await line('<span class="ok">Payload found.</span>', "", 80);
  await line("", "");

  await progressLine("Decrypting payload...");
  await sleep(200);
  await line('<span class="ok">Payload decrypted.</span>', "", 80);
  await line("", "");

  await progressLine("Checking compatibility...");
  await sleep(200);
  await line('<span class="ok">Compatibility: 99.9999998%</span>', "", 80);
  await line('<span class="ok">No merge conflicts detected.</span>', "", 100);
  await line("", "");

  await progressLine("Deploying marriage...");
  await sleep(200);
  await line('<span class="ok">Deployment successful.</span>', "", 80);
  await line("", "");
  await line("Launching happily_ever_after()", "", 200);
  await line("", "");

  // SUCCESS headline with typewriter
  const successEl = addLine("", "");
  show(successEl);
  await typewriter(successEl, "SUCCESS", 80);
  successEl.className = "line visible success-text";
  await sleep(600);

  // ── Confetti bursts ──
  const confetti = new ConfettiEngine("confetti-canvas");
  confetti.burst(220);
  await sleep(400);
  confetti.burst(180);
  await sleep(400);
  confetti.burst(150);

  await sleep(1000);

  // ── Shrink & fade terminal ──
  qs("#terminal").classList.add("shrink");

  await sleep(900);

  // ── Reveal card ──
  await revealCard();

  // ── Activate command input ──
  const cmdRow = qs("#cmdrow");
  cmdRow.hidden = false;
  qs("#cmdinput").focus();
}

// Kick off
boot();
