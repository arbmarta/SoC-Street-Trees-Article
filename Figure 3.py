import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

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

    # Choose cities depending on metric
    city_list = cities_basal if metric == 'Basal Area' else cities_all

    for city in city_list:
        city_df = df[df['City'] == city]
        dauid_values = city_df.groupby('DAUID')[metric].sum().sort_values()

        # Compute Lorenz curve
        cum_values = np.cumsum(dauid_values.values)
        lorenz = np.insert(cum_values / cum_values[-1], 0, 0)

        plt.plot(np.linspace(0.0, 1.0, len(lorenz)), lorenz)

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

    # Add figure label: A for first, B for second
    label = "A" if i == 0 else "B"
    plt.text(0.04, 0.95, label, transform=plt.gca().transAxes,
             fontsize=24, va='top', ha='left')

    plt.tight_layout()
    plt.show()

print(df['City'].unique())
