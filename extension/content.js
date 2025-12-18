(() => {
  const BUTTON_ID = "reddit-random-btn";
  const API_URL = "https://randeddit-api.iyed.space/get_sub?count=10";

  let cache = [];
  let isFetching = false;

  /* ---------------- PREFETCH ---------------- */

  async function prefetch() {
    if (isFetching || cache.length >= 3) return;

    isFetching = true;
    try {
      const res = await fetch(API_URL);
      const data = await res.json();

      if (Array.isArray(data)) {
        cache.push(...data.map((x) => x.subreddit));
      }
    } catch (e) {
      console.warn("Randomdit fetch failed", e);
    } finally {
      isFetching = false;
    }
  }

  // Fetch immediately — no waiting
  prefetch();

  /* ---------------- BUTTON ---------------- */

  function createButton() {
    const span = document.createElement("span");
    span.className = "hidden m:block contents";

    span.innerHTML = `
      <rpl-tooltip placement="bottom" appearance="inverted" trigger="hover focus-visible">
        <button
          id="${BUTTON_ID}"
          class="button-medium px-[var(--rem8)] button-plain icon items-center justify-center button inline-flex"
          aria-label="Random subreddit"
        >
          <svg fill="currentColor" width="20" height="20" viewBox="0 0 20 20">
            <rect x="2" y="2" width="16" height="16" rx="3" stroke="currentColor" fill="none" stroke-width="2"/>
            <circle cx="6" cy="6" r="1.5"/>
            <circle cx="10" cy="10" r="1.5"/>
            <circle cx="14" cy="14" r="1.5"/>
          </svg>
        </button>
        <span slot="content">Random</span>
      </rpl-tooltip>
    `;

    span.querySelector("button").onclick = () => {
      // Instant navigation
      const sub = cache.shift();

      if (sub) {
        window.location.href = `/r/${sub}`;
        prefetch(); // refill silently
      } else {
        // Absolute fallback
        window.location.href = "/r/random";
      }
    };

    return span;
  }

  /* ---------------- INJECT ---------------- */

  function inject() {
    if (document.getElementById(BUTTON_ID)) return;

    const actionRow = document.querySelector(
      "div.ps-lg.gap-xs.flex.items-center.justify-end"
    );
    if (!actionRow) return;

    actionRow.prepend(createButton());
  }

  let tries = 0;
  const timer = setInterval(() => {
    inject();
    if (++tries > 25 || document.getElementById(BUTTON_ID)) {
      clearInterval(timer);
    }
  }, 250);
})();
