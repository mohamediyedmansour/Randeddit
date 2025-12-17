chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (!tab.url) return;
  if (!tab.url.includes("reddit.com")) return;

  if (changeInfo.status === "complete" || changeInfo.url) {
    chrome.scripting
      .executeScript({
        target: { tabId },
        files: ["content.js"],
      })
      .catch(() => {});
  }
});
