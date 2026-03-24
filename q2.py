import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import argparse
import sys
import os

# ─────────────────────────────────────────
# Valid options
# ─────────────────────────────────────────
VALID_INDUSTRIES = {
    "1": "Construction [23]",
    "2": "Manufacturing [31-33]",
    "3": "Retail trade [44-45]",
    "4": "Health care and social assistance [62]",
    "5": "all"
}

VALID_PROVINCES = [
    "Newfoundland and Labrador",
    "Prince Edward Island",
    "Nova Scotia",
    "New Brunswick",
    "Quebec",
    "Ontario",
    "Manitoba",
    "Saskatchewan",
    "Alberta",
    "British Columbia",
    "Yukon",
    "Northwest Territories",
    "Nunavut"
]

# ─────────────────────────────────────────
# Argument Parsing
# ─────────────────────────────────────────
parser = argparse.ArgumentParser(
    description="Analyze relationship between wage growth and voter turnout across Canadian provinces."
)
parser.add_argument(
    "--industry",
    type=str,
    default=None,
    help=(
        "Industry to analyze. Provide a number (1-5) or exact name:\n"
        "  1 = Construction [23]\n"
        "  2 = Manufacturing [31-33]\n"
        "  3 = Retail trade [44-45]\n"
        "  4 = Health care and social assistance [62]\n"
        "  5 = all (average across all industries)\n"
        "If not provided, you will be prompted to choose."
    )
)
parser.add_argument(
    "--province",
    type=str,
    default="all",
    help=(
        "Province to highlight in the chart. Use 'all' to show all equally, "
        "or enter a specific province name (e.g. 'Ontario')."
    )
)
parser.add_argument(
    "--wages",
    type=str,
    default="wages_processed.csv",
    help="Path to the wages CSV file (default: wages_processed.csv)"
)
parser.add_argument(
    "--turnout",
    type=str,
    default="turnout44and43.csv",
    help="Path to the turnout CSV file (default: turnout44and43.csv)"
)

args = parser.parse_args()

# ─────────────────────────────────────────
# Industry Selection — prompt if not given
# ─────────────────────────────────────────
def prompt_industry():
    print("\n" + "─" * 50)
    print("  Select an industry to analyze:")
    print("─" * 50)
    print("  1. Construction")
    print("  2. Manufacturing")
    print("  3. Retail trade")
    print("  4. Health care and social assistance")
    print("  5. All industries (average)")
    print("─" * 50)
    while True:
        choice = input("  Enter a number (1-5): ").strip()
        if choice in VALID_INDUSTRIES:
            return VALID_INDUSTRIES[choice]
        else:
            print("  Invalid choice. Please enter a number between 1 and 5.")

# Resolve industry from argument or prompt
if args.industry is None:
    selected_industry = prompt_industry()
elif args.industry in VALID_INDUSTRIES:
    selected_industry = VALID_INDUSTRIES[args.industry]
elif args.industry in VALID_INDUSTRIES.values():
    selected_industry = args.industry
else:
    print(f"\nERROR: '{args.industry}' is not a valid industry.")
    print("You can pass a number (1-5) or one of these exact names:")
    for k, v in VALID_INDUSTRIES.items():
        print(f"  {k} = {v}")
    sys.exit(1)

# Validate province
if args.province != "all" and args.province not in VALID_PROVINCES:
    print(f"\nERROR: '{args.province}' is not a valid province.")
    print("Valid options are:")
    for p in VALID_PROVINCES:
        print(f"  {p}")
    sys.exit(1)

# ─────────────────────────────────────────
# Load data
# ─────────────────────────────────────────
print("\nLoading data...")

if not os.path.exists(args.wages):
    print(f"ERROR: Wages file not found at '{args.wages}'")
    sys.exit(1)

if not os.path.exists(args.turnout):
    print(f"ERROR: Turnout file not found at '{args.turnout}'")
    sys.exit(1)

wages_df = pd.read_csv(args.wages)
turnout_df = pd.read_csv(args.turnout)

# ─────────────────────────────────────────
# Process wages
# ─────────────────────────────────────────
wages_df["YEAR"] = wages_df["REF_DATE"].str[:4].astype(int)

if selected_industry != "all":
    wages_df = wages_df[wages_df["NAICS"] == selected_industry]
    industry_label = selected_industry
else:
    industry_label = "All Industries (Average)"

wages_avg = (
    wages_df.groupby(["GEO", "YEAR"])["VALUE"]
    .mean()
    .reset_index()
    .rename(columns={"GEO": "province", "VALUE": "avg_wage"})
)

wages_2019 = wages_avg[wages_avg["YEAR"] == 2019][["province", "avg_wage"]].rename(columns={"avg_wage": "wage_2019"})
wages_2021 = wages_avg[wages_avg["YEAR"] == 2021][["province", "avg_wage"]].rename(columns={"avg_wage": "wage_2021"})

wages_merged = pd.merge(wages_2019, wages_2021, on="province")
wages_merged["wage_change"] = wages_merged["wage_2021"] - wages_merged["wage_2019"]

# ─────────────────────────────────────────
# Merge wages with turnout
# ─────────────────────────────────────────
merged = pd.merge(wages_merged, turnout_df, on="province")

if merged.empty:
    print("ERROR: No matching data found after merging. Check that province names match between files.")
    sys.exit(1)

# ─────────────────────────────────────────
# Print summary table
# ─────────────────────────────────────────
print(f"\n{'─'*75}")
print(f"  Industry: {industry_label}")
print(f"{'─'*75}")
print(f"  {'Province':<33} {'Wage Change':>12} {'Turnout 2019':>13} {'Turnout 2021':>13} {'Turnout Change':>15}")
print(f"{'─'*75}")
for _, row in merged.sort_values("wage_change", ascending=False).iterrows():
    print(
        f"  {row['province']:<33}"
        f" {'${:+.2f}/hr'.format(row['wage_change']):>12}"
        f" {'{:.1f}%'.format(row['turnout_2019']):>13}"
        f" {'{:.1f}%'.format(row['turnout_2021']):>13}"
        f" {'{:+.1f}%'.format(row['turnout_change']):>15}"
    )
print(f"{'─'*75}\n")

# ─────────────────────────────────────────
# Visualization
# ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 7))

colors = []
sizes = []
for prov in merged["province"]:
    if args.province != "all" and prov == args.province:
        colors.append("#e63946")
        sizes.append(160)
    else:
        colors.append("#457b9d")
        sizes.append(90)

ax.scatter(
    merged["wage_change"],
    merged["turnout_change"],
    c=colors,
    s=sizes,
    alpha=0.85,
    edgecolors="white",
    linewidths=0.8,
    zorder=3
)

# Label each province
for _, row in merged.iterrows():
    ax.annotate(
        row["province"],
        (row["wage_change"], row["turnout_change"]),
        textcoords="offset points",
        xytext=(7, 4),
        fontsize=8,
        color="#333333"
    )

# Trend line
z = np.polyfit(merged["wage_change"], merged["turnout_change"], 1)
p = np.poly1d(z)
x_line = np.linspace(merged["wage_change"].min() - 0.5, merged["wage_change"].max() + 0.5, 100)
ax.plot(x_line, p(x_line), color="#e63946", linewidth=1.4,
        linestyle="--", alpha=0.6, label="Trend line", zorder=2)

# Reference lines at zero
ax.axhline(0, color="gray", linewidth=0.7, linestyle="--", alpha=0.4)
ax.axvline(0, color="gray", linewidth=0.7, linestyle="--", alpha=0.4)

# Axis labels and title
ax.set_xlabel("Average Wage Change 2019 → 2021 (CAD/hr)", fontsize=11)
ax.set_ylabel("Voter Turnout Change 2019 → 2021 (%)", fontsize=11)
ax.set_title(
    f"Wage Growth vs. Voter Turnout Change by Province\nIndustry: {industry_label}",
    fontsize=13,
    fontweight="bold",
    pad=15
)

ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('$%.2f'))
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))
ax.grid(True, linestyle="--", alpha=0.3, zorder=0)

# Legend
legend_handles = [
    plt.Line2D([0], [0], linestyle="--", color="#e63946", linewidth=1.4, label="Trend line"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#457b9d", markersize=9, label="Province")
]
if args.province != "all":
    legend_handles.append(
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#e63946",
                   markersize=9, label=f"Highlighted: {args.province}")
    )
ax.legend(handles=legend_handles, fontsize=9)

plt.tight_layout()

# Save chart with industry name in filename
safe_name = industry_label.replace(" ", "_").replace("/", "-").replace("[", "").replace("]", "").replace(",", "")
output_filename = f"wage_vs_turnout_{safe_name}.png"
plt.savefig(output_filename, dpi=150, bbox_inches="tight")
plt.show()
print(f"Chart saved as {output_filename}")
