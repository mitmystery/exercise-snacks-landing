/* =========================================================
   Exercise Snacks Landing Page — script.js
   - Smooth scroll: "See the research" button
   - Scroll-triggered fade-up animations via Intersection Observer
   ========================================================= */

(function () {
  'use strict';

  /* ---------------------------------------------------------
     1. Smooth Scroll — "See the research" button
        Handles the anchor link to #research with an offset
        so the section header isn't hidden under anything.
  --------------------------------------------------------- */
  document.querySelectorAll('.js-scroll-research').forEach(function (link) {
    link.addEventListener('click', function (e) {
      var href = link.getAttribute('href');
      if (!href || href.charAt(0) !== '#') return;

      var target = document.querySelector(href);
      if (!target) return;

      e.preventDefault();

      var offset = 32; // px breathing room above section
      var targetY = target.getBoundingClientRect().top + window.pageYOffset - offset;

      window.scrollTo({
        top: targetY,
        behavior: 'smooth',
      });
    });
  });

  /* ---------------------------------------------------------
     2. Intersection Observer — fade-up entrance animations
        Watches every .animate-up element and adds .visible
        once it enters the viewport. Elements are marked
        observed after triggering so the Observer disconnects
        per-element (fire once).
  --------------------------------------------------------- */
  var animatedElements = document.querySelectorAll('.animate-up');

  if (!animatedElements.length) return;

  // Check if the browser supports IntersectionObserver
  if (!('IntersectionObserver' in window)) {
    // Fallback: just show everything immediately
    animatedElements.forEach(function (el) {
      el.classList.add('visible');
    });
    return;
  }

  var observerOptions = {
    root: null,           // viewport
    rootMargin: '0px 0px -60px 0px', // trigger 60px before fully in view
    threshold: 0.12,      // 12% of element visible before firing
  };

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target); // animate once
      }
    });
  }, observerOptions);

  animatedElements.forEach(function (el) {
    observer.observe(el);
  });

})();
