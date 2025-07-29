import matplotlib.pyplot as plt
from matplotlib.patches import Patch

species_richness = {
    "ajax": 126,
    "burlington": 150,
    "calgary": 170,
    "edmonton": 125,
    "fredericton": 90,
    "guelph": 125,
    "halifax": 232,
    "kelowna": 105,
    "kingston": 161,
    "kitchener": 139,
    "lethbridge": 88,
    "longueuil": 113,
    "maple ridge": 163,
    "mississauga": 184,
    "moncton": 109,
    "montreal": 296,
    "new westminster": 272,
    "niagara falls": 131,
    "ottawa": 151,
    "peterborough": 123,
    "quebec city": 216,
    "regina": 29,
    "st. catharines": 147,
    "strathcona county": 89,
    "toronto": 216,
    "vancouver": 373,
    "victoria": 259,
    "waterloo": 100,
    "welland": 51,
    "whitby": 134,
    "windsor": 144,
    "winnipeg": 113
}

native_proportion = {
    "Vancouver": 4.78,
    "Victoria": 15.09,
    "New Westminster": 10.35,
    "Maple Ridge": 4.61,
    "Kelowna": 26.22,
    "Calgary": 31.86,
    "Lethbridge": 15.93,
    "Edmonton": 11.87,
    "Strathcona County": 23.58,
    "Regina": 89.17,
    "Winnipeg": 75.88,
    "St. Catharines": 27.89,
    "Niagara Falls": 31.87,
    "Ajax": 37.60,
    "Whitby": 36.36,
    "Kitchener": 32.17,
    "Burlington": 34.19,
    "Mississauga": 34.00,
    "Windsor": 38.47,
    "Toronto": 39.81,
    "Kingston": 45.26,
    "Waterloo": 44.38,
    "Peterborough": 54.86,
    "Welland": 47.73,
    "Guelph": 45.87,
    "Ottawa": 60.94,
    "Montreal": 35.32,
    "Quebec City": 47.35,
    "Longueuil": 58.17,
    "Moncton": 47.89,
    "Fredericton": 68.33,
    "Halifax": 42.01
}

# Custom ecozone color palette
ecozone_colors = {
    'Pacific Maritime': '#009DAE',    # Deep Forest Green
    'Montane Cordillera': '#A9A9A9', # Mountain Gray
    'Prairie': '#DFAF2C',            # Amber / Tawny Brown
    'Mixedwood Plain': '#D02E2E',    # Light Maple Red
    'Atlantic Maritime': '#0F52BA'   # Sapphire Blue
}

city_ecozones = {
    "Victoria": "Pacific Maritime",
    "Vancouver": "Pacific Maritime",
    "New Westminster": "Pacific Maritime",
    "Maple Ridge": "Pacific Maritime",

    "Kelowna": "Montane Cordillera",

    "Calgary": "Prairie",
    "Edmonton": "Prairie",
    "Strathcona County": "Prairie",
    "Lethbridge": "Prairie",
    "Regina": "Prairie",
    "Winnipeg": "Prairie",

    "Windsor": "Mixedwood Plain",
    "Waterloo": "Mixedwood Plain",
    "Kitchener": "Mixedwood Plain",
    "Guelph": "Mixedwood Plain",
    "Burlington": "Mixedwood Plain",
    "Mississauga": "Mixedwood Plain",
    "Toronto": "Mixedwood Plain",
    "Welland": "Mixedwood Plain",
    "St. Catharines": "Mixedwood Plain",
    "Niagara Falls": "Mixedwood Plain",
    "Ajax": "Mixedwood Plain",
    "Whitby": "Mixedwood Plain",
    "Peterborough": "Mixedwood Plain",
    "Kingston": "Mixedwood Plain",
    "Ottawa": "Mixedwood Plain",
    "Montreal": "Mixedwood Plain",
    "Quebec City": "Mixedwood Plain",
    "Longueuil": "Mixedwood Plain",

    "Fredericton": "Atlantic Maritime",
    "Moncton": "Atlantic Maritime",
    "Halifax": "Atlantic Maritime"
}

# Capitalize all input dictionaries
species_richness_cap = {k.title(): v for k, v in species_richness.items()}
native_proportion_cap = {k.title(): v for k, v in native_proportion.items()}
city_ecozones_cap = {k.title(): v for k, v in city_ecozones.items()}
ecozone_colors_cap = {k: v for k, v in ecozone_colors.items()}

# Use exact city order from your city_ecozones definition
ordered_cities = [k.title() for k in city_ecozones]
ordered_cities = [city for city in ordered_cities if city in species_richness_cap and city in native_proportion_cap]

# Extract data
richness_vals = [species_richness_cap[city] for city in ordered_cities]
native_vals = [native_proportion_cap[city] for city in ordered_cities]
colors = [ecozone_colors_cap[city_ecozones_cap[city]] for city in ordered_cities]

# Plot
fig, ax1 = plt.subplots(figsize=(16, 6))

# Bar plot (slightly faded)
ax1.bar(ordered_cities, richness_vals, color=colors, alpha=0.6)
ax1.set_ylabel('Species Richness', fontweight='bold', fontsize=13)
ax1.set_xticks(range(len(ordered_cities)))
ax1.set_xticklabels(ordered_cities, rotation=90, fontsize=12)
ax1.tick_params(axis='y', labelsize=12)
ax1.margins(x=0.01)

# Scatter plot for native proportion
ax2 = ax1.twinx()
ax2.scatter(range(len(ordered_cities)), native_vals, color='black', edgecolor='black', s=120, zorder=10)
ax2.set_ylabel('Proportion of Native Trees (%)', fontweight='bold', fontsize=13)
ax2.tick_params(axis='y', labelsize=12)

# Legend: 5 columns in a single row, inside figure
legend_handles = [Patch(color=color, label=eco) for eco, color in ecozone_colors_cap.items()]
ax1.legend(
    handles=legend_handles,
    loc='upper center',
    bbox_to_anchor=(0.5, 1.12),
    ncol=5,
    frameon=False,
    fontsize=11,
    title_fontsize=12
)

# Title and layout
fig.tight_layout()

plt.savefig("SoC Figure 2.png", dpi=600, bbox_inches='tight')

plt.show()
