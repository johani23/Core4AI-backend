// ============================================================
// 💎 Core4.AI – Dev Environment Reset Script
// ------------------------------------------------------------
// 🧰 Cleans cache, removes Vite temp files, reinstalls deps,
// and restarts the local dev server.
// Run with:  node reset-dev-env.js
// ============================================================

import { execSync } from "child_process";
import fs from "fs";
import path from "path";

const root = process.cwd();

const dirsToRemove = [
  "node_modules/.vite",
  "node_modules/.cache",
  "dist",
];

console.log("\n🧹  Cleaning development environment...\n");

for (const dir of dirsToRemove) {
  const target = path.join(root, dir);
  if (fs.existsSync(target)) {
    fs.rmSync(target, { recursive: true, force: true });
    console.log(`🗑️  Removed: ${dir}`);
  }
}

// clear npm cache
console.log("\n🧼  Cleaning npm cache...");
execSync("npm cache clean --force", { stdio: "inherit" });

// reinstall deps
console.log("\n📦  Reinstalling dependencies...");
execSync("npm install", { stdio: "inherit" });

// restart vite dev server
console.log("\n🚀  Restarting Vite dev server...\n");
execSync("npm run dev", { stdio: "inherit" });
