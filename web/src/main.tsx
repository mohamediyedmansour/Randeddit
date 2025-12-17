// src/main.tsx
import React from "react";
import { createRoot } from "react-dom/client";
import App from "./app/App";

import "./styles/index.css"; // if you have global styles

const container = document.getElementById("app");
if (container) {
  const root = createRoot(container);
  root.render(<App />);
}

