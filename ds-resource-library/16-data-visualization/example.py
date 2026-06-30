"""
Example — Data Visualization (chart with a takeaway, saved to PNG)
==================================================================
Runnable (headless). Deps: matplotlib, numpy

Demonstrates the senior habits: title states the TAKEAWAY (not just axes),
uncertainty is shown (error bars), and chart junk is removed. Saves a PNG so it
works without a display.

Run: python example.py   ->   writes bills_by_group.png
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # headless backend (no display needed)
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

rng = np.random.default_rng(0)
groups = ["Mon", "Tue", "Wed", "Thu", "Fri"]
means = np.array([18, 19, 21, 24, 31], dtype=float)
# Standard error for error bars (uncertainty -> honest charts).
errs = rng.uniform(1.0, 2.5, size=len(groups))

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(groups, means, yerr=errs, capsize=4, color="#4C72B0")
bars[-1].set_color("#DD8452")  # highlight the point that drives the message

# Title = the message; minimal chrome.
ax.set_title("Friday bills run ~70% higher than Monday", fontsize=13, fontweight="bold")
ax.set_ylabel("Avg bill ($)")
ax.spines[["top", "right"]].set_visible(False)   # remove chart junk
for spine_val, x in zip(means, range(len(groups))):
    ax.text(x, spine_val + 3, f"${spine_val:.0f}", ha="center", fontsize=9)

plt.tight_layout()
out = "bills_by_group.png"
plt.savefig(out, dpi=130)
print(f"Saved {out}")
print("Lesson: label charts with the TAKEAWAY, show uncertainty (error bars),")
print("highlight the one element that carries the message, and strip chart junk.")
