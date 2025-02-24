import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

// Define rank names
export const standardsNames = [
    "God",
    "Myth A", "Myth B", "Myth C",
    "Titan A", "Titan B", "Titan C",
    "Hero A", "Hero B", "Hero C",
    "Exp A", "Exp B", "Exp C",
    "Adv A", "Adv B", "Adv C",
    "Int A", "Int B", "Int C",
    "Beg A", "Beg B", "Beg C"
];

export const WRColor = "rgb(251, 192, 45)";

// Generate color mapping
export const rankColormap = new Map();
standardsNames.forEach((rank, i) => {
    let index = 0.05;
    let color = tintColor(d3.interpolateTurbo(index), 30);
    if (i > 0) {
        index += Math.floor((i + 2) / 3) * 0.9 / 7;
        color = d3.interpolateTurbo(index);
        if ((i - 1) % 3 === 0) color = tintColor(color, 10, true);
        if ((i - 1) % 3 === 1) color = tintColor(color, 30);
        if ((i - 1) % 3 === 2) color = tintColor(color, 50);
    }
    rankColormap.set(rank, color);
});

// WR Diff Color Scaling
const DIFF_MAX = 10;
const DIFF_STEP = 1.0;

export function getWRDiffColor(diff) {
    if (isNaN(diff)) return "white";

    let index = Math.max(0, Math.min(Math.floor(diff / DIFF_STEP) / (DIFF_MAX / DIFF_STEP), 1));
    return d3.interpolateSpectral(1 - index);
}

// Function to lighten or darken a color
export function tintColor(color, percent, darken = false) {
    let rgb = d3.color(color);
    if (!rgb) return color;

    let bw = darken ? "#000000" : "#FFFFFF";
    return d3.interpolateRgb(color, bw)(percent / 100);
}
