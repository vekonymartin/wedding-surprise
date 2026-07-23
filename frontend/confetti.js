/* ─────────────────────────────────────────────
   confetti.js — canvas-based confetti engine
   Pure vanilla JS, no dependencies
   ───────────────────────────────────────────── */

(function (global) {
  "use strict";

  const COLORS = [
    "#3fb950", "#58a6ff", "#d2a8ff",
    "#ffa657", "#ff7b72", "#f0e040",
    "#79c0ff", "#56d364",
  ];

  class Particle {
    constructor(canvas) {
      this.canvas = canvas;
      this.reset(true);
    }

    reset(initial = false) {
      const w = this.canvas.width;
      const h = this.canvas.height;
      this.x = Math.random() * w;
      this.y = initial ? Math.random() * h - h : -20;
      this.size = Math.random() * 8 + 4;
      this.color = COLORS[Math.floor(Math.random() * COLORS.length)];
      this.speedX = (Math.random() - .5) * 3.5;
      this.speedY = Math.random() * 3 + 1.5;
      this.rotation = Math.random() * Math.PI * 2;
      this.rotSpeed = (Math.random() - .5) * .12;
      this.opacity = 1;
      this.shape = Math.random() < .5 ? "rect" : "circle";
    }

    update() {
      this.x += this.speedX;
      this.y += this.speedY;
      this.rotation += this.rotSpeed;
      if (this.y > this.canvas.height + 20) this.reset();
    }

    draw(ctx) {
      ctx.save();
      ctx.globalAlpha = this.opacity;
      ctx.fillStyle = this.color;
      ctx.translate(this.x, this.y);
      ctx.rotate(this.rotation);
      if (this.shape === "rect") {
        ctx.fillRect(-this.size / 2, -this.size / 4, this.size, this.size / 2);
      } else {
        ctx.beginPath();
        ctx.arc(0, 0, this.size / 2, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.restore();
    }
  }

  class ConfettiEngine {
    constructor(canvasId) {
      this.canvas = document.getElementById(canvasId);
      this.ctx = this.canvas.getContext("2d");
      this.particles = [];
      this.running = false;
      this.raf = null;
      this._resize = this._resize.bind(this);
      window.addEventListener("resize", this._resize);
    }

    _resize() {
      this.canvas.width  = window.innerWidth;
      this.canvas.height = window.innerHeight;
    }

    burst(count = 200) {
      this._resize();
      // add fresh particles originating from top
      for (let i = 0; i < count; i++) {
        const p = new Particle(this.canvas);
        p.y = Math.random() * this.canvas.height * .4 - 40;
        p.speedY = Math.random() * 4 + 2;
        this.particles.push(p);
      }
      if (!this.running) this._loop();
    }

    _loop() {
      this.running = true;
      const ctx = this.ctx;
      const tick = () => {
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.particles.forEach(p => { p.update(); p.draw(ctx); });
        // remove finished particles after a while
        if (this.particles.length > 500) {
          this.particles.splice(0, this.particles.length - 500);
        }
        this.raf = requestAnimationFrame(tick);
      };
      tick();
    }

    stop() {
      this.running = false;
      if (this.raf) cancelAnimationFrame(this.raf);
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.particles = [];
    }
  }

  global.ConfettiEngine = ConfettiEngine;
})(window);
