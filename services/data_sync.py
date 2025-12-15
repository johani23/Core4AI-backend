/**
 * 💎 Core4.AI – MVP-24.9 DataSync (Final Stable Version)
 * ------------------------------------------------------------
 * Unified logic for:
 *  - Market & Wallet Sync
 *  - Emotion Cluster Analysis (Feed)
 *  - Leaderboard Color Mapping
 *  - Unified Stats (Profile / Leaderboard)
 * ------------------------------------------------------------
 */

import {
  getWallet,
  getMarketMood,
  getMarketTrades,
  getMarketMessages,
} from "@services/api";

/* ------------------------------------------------------------
 * 🧠 Unified Market Sync
 * ------------------------------------------------------------ */
export async function syncMarketData(userId = 1) {
  try {
    const [wallet, mood, trades, message] = await Promise.all([
      getWallet(userId),
      getMarketMood(),
      getMarketTrades(),
      getMarketMessages(),
    ]);

    const snapshot = {
      wallet,
      mood,
      trades,
      message,
      timestamp: new Date().toISOString(),
    };

    cacheMarketData(snapshot);
    return snapshot;
  } catch (err) {
    console.warn("⚠️ DataSync fallback (mock mode):", err.message);

    const fallback = {
      wallet: { balance: 30, symbol: "C4T", dopamine: 50 },
      mood: { mood: "neutral", emoji: "🌤", label: "Calm", emi: 50 },
      trades: [
        { price: 3.42, qty: 15, t: new Date().toISOString() },
        { price: 3.39, qty: 22, t: new Date(Date.now() - 60000).toISOString() },
      ],
      message: {
        message: "🌤 Calm day — keep posting meaningful content!",
        timestamp: new Date().toISOString(),
      },
      timestamp: new Date().toISOString(),
    };

    cacheMarketData(fallback);
    return fallback;
  }
}

/* ------------------------------------------------------------
 * 🎨 Market / Momentum Color Helpers
 * ------------------------------------------------------------ */
export function getMoodColor(mood) {
  if (!mood) return "#facc15"; // neutral yellow
  const tone = mood.toLowerCase();
  if (tone.includes("euphoric") || tone.includes("bullish")) return "#22c55e"; // green
  if (tone.includes("bearish") || tone.includes("cooling") || tone.includes("flat"))
    return "#ef4444"; // red
  return "#facc15"; // yellow (neutral)
}

/* 🔗 Alias for Leaderboard compatibility */
export function getMomentumColor(mood) {
  return getMoodColor(mood);
}

/* ------------------------------------------------------------
 * ⚙️ Local Cache
 * ------------------------------------------------------------ */
export function cacheMarketData(data) {
  try {
    localStorage.setItem("core4_market_cache", JSON.stringify(data));
  } catch (err) {
    console.warn("Cache write error:", err.message);
  }
}

export function loadCachedMarketData() {
  try {
    const cache = localStorage.getItem("core4_market_cache");
    return cache ? JSON.parse(cache) : null;
  } catch (err) {
    console.warn("Cache read error:", err.message);
    return null;
  }
}

/* ------------------------------------------------------------
 * 🔁 Auto-Refresh Utility
 * ------------------------------------------------------------ */
export function startAutoSync(callback, interval = 60000, userId = 1) {
  async function refresh() {
    const data = await syncMarketData(userId);
    callback?.(data);
  }
  refresh();
  return setInterval(refresh, interval);
}

/* ------------------------------------------------------------
 * 🧠 Emotion Cluster Analysis (Feed.jsx)
 * ------------------------------------------------------------ */
export async function analyzeEmotionCluster(text) {
  try {
    const res = await fetch("http://127.0.0.1:8000/ai/emotion-cluster", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn("⚠️ Emotion Cluster fallback:", err.message);
    const tones = ["joy", "focus", "curiosity", "neutral", "tension"];
    const tone = tones[Math.floor(Math.random() * tones.length)];
    return {
      text,
      cluster: `${tone.charAt(0).toUpperCase() + tone.slice(1)} Cluster`,
      dominant_tone: tone,
      value_density: Math.random().toFixed(2),
      insight: `Offline mode — simulated ${tone} tone.`,
    };
  }
}

/* ------------------------------------------------------------
 * 🧬 Unified Stats (Profile / Leaderboard)
 * ------------------------------------------------------------ */
export function getUnifiedStats() {
  const mockClusters = [
    { id: 1, name: "Visionary Squad", momentum: "Rising 🚀", description: "High creative synergy." },
    { id: 2, name: "Neural Nomads", momentum: "Climbing 📈", description: "Strong adaptation and growth." },
    { id: 3, name: "Data Dreamers", momentum: "Stable 🌕", description: "Consistent teamwork and results." },
  ];

  return {
    groups: mockClusters.map((c) => ({
      ...c,
      ai: {
        momentum: c.momentum,
        forecast: c.description,
        insight:
          c.momentum.includes("Rising") || c.momentum.includes("Climbing")
            ? "High synergy and creativity boost expected."
            : "Steady performance and consistent engagement.",
      },
    })),
  };
}
