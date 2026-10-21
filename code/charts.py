"""Data charts for the affordable housing brief. Brand palette: dark charcoal, amber, teal."""
import json, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PKG = pathlib.Path(__file__).resolve().parent.parent
S = json.loads((PKG / "stats.json").read_text())
BG, AMBER, TEAL, FG = "#1a1a1a", "#f2a900", "#2a9d8f", "#e8e8e8"
plt.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG, "text.color": FG,
                     "axes.labelcolor": FG, "xtick.color": FG, "ytick.color": FG,
                     "axes.edgecolor": "#555555"})

def save(fig, name):
    fig.savefig(PKG / "charts" / name, dpi=200, facecolor=BG)
    plt.close(fig); print(name)

# 1. Top neighborhoods by restricted units
top = S["top_neighborhoods_by_units"][:8][::-1]
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.barh([t[0] for t in top], [t[1] for t in top], color=AMBER)
for i, t in enumerate(top):
    ax.text(t[1] + 40, i, f"{t[1]:,} units, {t[2]} projects", va="center", fontsize=9)
ax.set_xlabel("Income-restricted units (HOST inventory, pulled Oct 21, 2026)")
ax.set_title("Restricted units concentrate in a few neighborhoods", color=FG, loc="left")
ax.set_xlim(0, 3300)
save(fig, "chart_top_neighborhoods.png")

# 2. Units opened by decade
dec = S["by_decade_opened"]
labels = [f"{k}s" for k in dec]; vals = [dec[k]["restricted_units"] for k in dec]
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.bar(labels, vals, color=TEAL)
for i, v in enumerate(vals):
    ax.text(i, v + 180, f"{v:,}", ha="center", fontsize=9)
ax.set_ylabel("Restricted units")
ax.set_title("Restricted units by decade the project opened (BUILT_OPEN_DATE as filed)", color=FG, loc="left")
ax.tick_params(axis="x", labelsize=8, rotation=30)
save(fig, "chart_decades.png")

# 3. Rate per 1,000 housing units, top neighborhoods excluding Sun Valley (denominator caveat printed)
rates = sorted(((k, v["restricted_per_1000_units"], v["restricted_units"]) for k, v in S["neighborhoods"].items()
                if k != "Sun Valley"), key=lambda x: -x[1])[:8][::-1]
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.barh([r[0] for r in rates], [r[1] for r in rates], color=AMBER)
for i, r in enumerate(rates):
    ax.text(r[1] + 8, i, f"{r[1]:.1f} per 1,000 ({r[2]:,} units)", va="center", fontsize=9)
ax.axvline(82.0, color=TEAL, linestyle="--", label="Citywide: 82.0 per 1,000")
ax.legend(facecolor=BG, edgecolor="#555555", labelcolor=FG, fontsize=8)
ax.set_xlabel("Restricted units per 1,000 housing units (ACS units, neighborhood panel)")
ax.set_title("Restricted-unit rates: Sun Valley excluded - its 1,196 units exceed\nits ACS housing-unit base (502.9), see brief Finding 3", color=FG, loc="left", fontsize=10)
ax.set_xlim(0, 520)
save(fig, "chart_neighborhood_rates.png")
