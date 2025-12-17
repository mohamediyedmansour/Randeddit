(function () {
  const INTERVAL = setInterval(() => {
    // Main navbar button container
    const navGroup = document.querySelector(
      "div.ps-lg.gap-xs.flex.items-center.justify-end > div.flex.h-\\[40px\\]"
    );

    if (!navGroup) return;

    // Prevent duplicates
    if (document.getElementById("reddit-random-btn")) {
      clearInterval(INTERVAL);
      return;
    }

    // Create wrapper span (matches Reddit structure)
    const wrapper = document.createElement("span");
    wrapper.className = "contents";

    // Create button
    const button = document.createElement("button");
    button.id = "reddit-random-btn";
    button.className = `
      button-medium px-[var(--rem8)]
      button-plain
      icon
      items-center justify-center
      button inline-flex
    `;

    button.setAttribute("aria-label", "Random");
    button.title = "Random";

    // SVG icon (dice-style)
    button.innerHTML = `
      <span class="flex items-center justify-center">
        <svg fill="currentColor" width="20" height="20" viewBox="0 0 20 20">
          <path d="M4 2h12a2 2 0 012 2v12a2 2 0 01-2 2H4a2 2 0 01-2-2V4a2 2 0 012-2zm2.5 3a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm5 0a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm5 0a1.5 1.5 0 100 3 1.5 1.5 0 000-3zM6.5 10a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm5 0a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm2.5 3a1.5 1.5 0 100 3 1.5 1.5 0 000-3z"/>
        </svg>
      </span>
    `;

    // Click action
    button.addEventListener("click", (e) => {
      e.preventDefault();
      window.location.href = "https://google.com";
    });

    wrapper.appendChild(button);

    // Insert before chat button (native placement)
    const chatButton = navGroup.querySelector('[data-part="chat"]');
    navGroup.insertBefore(wrapper, chatButton);

    clearInterval(INTERVAL);
  }, 500);
})();
