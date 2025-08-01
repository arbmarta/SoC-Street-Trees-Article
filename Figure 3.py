import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from matplotlib.patches import Patch

df = pd.read_csv('Processing File.csv')

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

# Define metrics and exclusions
metrics = ['Tree Count', 'Basal Area']
exclude_for_basal = ["Halifax", "Maple Ridge", "New Westminster", "Peterborough", "Waterloo"]
cities_all = df['City'].unique()
cities_basal = [c for c in cities_all if c not in exclude_for_basal]

for i, metric in enumerate(metrics):
    plt.figure(figsize=(8, 6))

    city_list = cities_basal if metric == 'Basal Area' else cities_all

    # Group cities by ecozone
    ecozone_city_map = {}
    for city in city_list:
        ecozone = city_ecozones.get(city)
        if ecozone:
            ecozone_city_map.setdefault(ecozone, []).append(city)

    x_vals = np.linspace(0.0, 1.0, 1000)

    for ecozone, cities in ecozone_city_map.items():
        curves = {}
        for city in cities:
            city_df = df[df['City'] == city]
            dauid_values = city_df.groupby('DAUID')[metric].sum().sort_values()
            if dauid_values.sum() == 0:
                continue  # skip cities with no data

            cum_vals = np.cumsum(dauid_values.values)
            lorenz = np.insert(cum_vals / cum_vals[-1], 0, 0)
            x_lorenz = np.linspace(0.0, 1.0, len(lorenz))
            interpolated = np.interp(x_vals, x_lorenz, lorenz)
            curves[city] = interpolated

        if not curves:
            continue

        # Identify min and max curves
        all_curves = np.array(list(curves.values()))
        min_curve = np.min(all_curves, axis=0)
        max_curve = np.max(all_curves, axis=0)

        # Find corresponding cities
        min_city = min(curves, key=lambda city: np.sum(curves[city]))
        max_city = max(curves, key=lambda city: np.sum(curves[city]))
        min_curve = curves[min_city]
        max_curve = curves[max_city]

        # Plot filled area between them
        plt.fill_between(x_vals, min_curve, max_curve,
                         color=ecozone_colors[ecozone], alpha=0.2)

        # Plot min and max curves
        plt.plot(x_vals, min_curve, color=ecozone_colors[ecozone], alpha=0.8, linewidth=1.5)
        plt.plot(x_vals, max_curve, color=ecozone_colors[ecozone], alpha=0.8, linewidth=1.5)

    # Line of equality
    plt.plot([0, 1], [0, 1], color='black', linestyle='--')
    plt.text(0.40, 0.42, "Line of Perfect Equality", rotation=37.5, fontsize=10,
             color='black', ha='left', va='bottom')

    plt.xlabel("Cumulative Population", fontweight='bold')
    plt.ylabel(f"Cumulative {metric}", fontweight='bold')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.grid(False)

    # Figure label
    #label = "A" if i == 0 else "B"
    #plt.text(0.04, 0.95, label, transform=plt.gca().transAxes, fontsize=24, va='top', ha='left')

    # Add ecozone color legend
    from matplotlib.patches import Patch
    legend_handles = [Patch(color=color, label=ecozone) for ecozone, color in ecozone_colors.items()]
    plt.legend(handles=legend_handles, loc='upper left', frameon=False)

    plt.tight_layout()
    plt.show()
