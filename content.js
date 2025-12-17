(() => {
  const BUTTON_ID = "reddit-random-btn";

  function createButton() {
    const span = document.createElement("span");
    span.className = "hidden m:block contents";

    span.innerHTML = `
      <rpl-tooltip placement="bottom" appearance="inverted" trigger="hover focus-visible">
        <button
          id="${BUTTON_ID}"
          class="button-medium px-[var(--rem8)] button-plain icon items-center justify-center button inline-flex"
          aria-label="Random"
          title="Random"
        >
          <svg fill="currentColor" width="20" height="20" viewBox="0 0 20 20">
            <path d="M4 2h12a2 2 0 012 2v12a2 2 0 01-2 2H4a2 2 0 01-2-2V4a2 2 0 012-2z"/>
          </svg>
        </button>
        <span slot="content">Random</span>
      </rpl-tooltip>
    `;

    span.querySelector("button").onclick = () => {
      window.location.href = "/r/random";
    };

    return span;
  }

  function inject() {
    if (document.getElementById(BUTTON_ID)) return;

    // This selector IS stable (confirmed by your logs)
    const actionRow = document.querySelector(
      "div.ps-lg.gap-xs.flex.items-center.justify-end"
    );
    if (!actionRow) return;

    actionRow.prepend(createButton());
  }

  // Retry loop — cheap and reliable
  let tries = 0;
  const timer = setInterval(() => {
    inject();
    if (++tries > 20 || document.getElementById(BUTTON_ID)) {
      clearInterval(timer);
    }
  }, 300);
})();
