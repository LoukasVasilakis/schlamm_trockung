import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from sqlalchemy import create_engine

plt.close("all")

print("Starting DB Error Analysis...")

# -----------------------------
# Einstellungen
# -----------------------------
DB_URL = "postgresql://postgres:postgres@localhost:5432/pro2d_db"
BLUE = "#2E5EAA"
TOP3_LINE_COLORS = ["#2E5EAA", "#F28E2B", "#59A14F"]
TOP3_STACK_COLORS = ["#2E5EAA", "#F28E2B", "#BDBDBD"]

de_months = {
    1: "Jan",
    2: "Feb",
    3: "Mär",
    4: "Apr",
    5: "Mai",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Okt",
    11: "Nov",
    12: "Dez",
}

weekday_mapping = {
    "Monday": "Montag",
    "Tuesday": "Dienstag",
    "Wednesday": "Mittwoch",
    "Thursday": "Donnerstag",
    "Friday": "Freitag",
    "Saturday": "Samstag",
    "Sunday": "Sonntag",
}

weekday_order = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]


# -----------------------------
# Hilfsfunktionen
# -----------------------------
def german_month_formatter(x, pos=None):
    dt = mdates.num2date(x)
    return de_months.get(dt.month, "")


def style_time_axis(ax, x_values):
    ax.set_xlim(x_values.min() - pd.Timedelta(days=5), x_values.max() + pd.Timedelta(days=5))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_minor_formatter(FuncFormatter(german_month_formatter))

    plt.setp(ax.xaxis.get_majorticklabels(), rotation=0, fontsize=11, fontweight="bold")
    plt.setp(ax.xaxis.get_minorticklabels(), rotation=0, fontsize=9)

    ax.tick_params(axis="x", which="major", pad=15)
    ax.tick_params(axis="x", which="minor", pad=3)

    for year in pd.Series(x_values).dt.year.unique():
        ax.axvline(pd.Timestamp(f"{year}-01-01"), color="gray", linestyle="--", alpha=0.3)


def show_and_close():
    plt.tight_layout()
    plt.show()
    plt.close()


# -----------------------------
# Daten laden
# -----------------------------
engine = create_engine(DB_URL)

query = """
SELECT "Datum", "Meldung", "evtTyp", "Prio"
FROM events
WHERE "evtTyp" = 'Störmeldungen'
"""

df = pd.read_sql(query, engine)

print("Data shape:", df.shape)
print("\nColumns:")
print(df.columns)
print("\nFirst 5 rows:")
print(df.head())

if df.empty:
    print("\nKeine Störmeldungen gefunden.")
    exit()

print("\nFehlende Werte (NA):")
print(df.isna().sum())

print("\nNA in Meldung:")
print(df["Meldung"].isna().sum())

# -----------------------------
# Datenbereinigung
# -----------------------------
df = df.dropna(subset=["Meldung"])
empty_strings = df["Meldung"].str.strip() == ""
print("\nLeere Meldungen (inkl. Leerzeichen):", empty_strings.sum())

df = df[~empty_strings].copy()

print("\nData shape nach Cleaning:", df.shape)

# -----------------------------
# Feature Engineering
# -----------------------------
df["Datum"] = pd.to_datetime(df["Datum"])
df["Monat_num"] = df["Datum"].dt.month
df["Monat_kurz"] = df["Monat_num"].map(de_months)
df["Jahr"] = df["Datum"].dt.year
df["Monat_Anzeige"] = df["Monat_kurz"] + " " + df["Jahr"].astype(str)
df["Monat"] = df["Datum"].dt.to_period("M")
df["Stunde"] = df["Datum"].dt.hour
df["Wochentag"] = df["Datum"].dt.day_name().map(weekday_mapping)

# -----------------------------
# Globaler NA / NaN Check
# -----------------------------
print("\n----- NA / NaN CHECK (GANZER DATENSATZ) -----")

missing = df.isna().sum()
missing_percent = df.isna().mean() * 100

na_check = pd.DataFrame({"Fehlende Werte": missing, "Anteil (%)": missing_percent.round(2)})

print(na_check)

print("\nDatentypen:")
print(df.dtypes)

# -----------------------------
# Grundauswertung
# -----------------------------
error_counts = df["Meldung"].value_counts()

print("\nTop 10 häufigste Störmeldungen:")
print(error_counts.head(10))

most_common_error = error_counts.idxmax()
most_common_count = error_counts.max()

print("\nHäufigste Störmeldung:")
print(most_common_error)

print("\nAnzahl:")
print(most_common_count)

# -----------------------------
# Plot 1: Top 10 Störmeldungen (absolut + relativ)
# -----------------------------
top_10_errors = error_counts.head(10)
top_10_sorted = top_10_errors.sort_values()

total_errors = len(df)
top_10_percent_sorted = ((top_10_errors / total_errors) * 100).sort_values()

fig, axes = plt.subplots(ncols=2, figsize=(16, 7))

ax1 = axes[0]
top_10_sorted.plot(kind="barh", color="darkred", ax=ax1)
offset1 = top_10_sorted.max() * 0.01
for i, v in enumerate(top_10_sorted):
    ax1.text(v + offset1, i, str(v), va="center", fontweight="bold")
ax1.set_xlim(0, top_10_sorted.max() * 1.2)
ax1.set_title("Häufigkeit")
ax1.set_xlabel("Anzahl")
ax1.set_ylabel("Störmeldung")
ax1.grid(axis="x", linestyle="--", alpha=0.6)

ax2 = axes[1]
top_10_percent_sorted.plot(kind="barh", color="darkorange", ax=ax2)
offset2 = top_10_percent_sorted.max() * 0.01
for i, v in enumerate(top_10_percent_sorted):
    ax2.text(v + offset2, i, f"{v:.1f}%", va="center", fontweight="bold")
ax2.set_xlim(0, top_10_percent_sorted.max() * 1.2)
ax2.set_title("Normalisierter Anteil (%)")
ax2.set_xlabel("Prozent (%)")
ax2.set_ylabel("")
ax2.grid(axis="x", linestyle="--", alpha=0.6)

plt.suptitle("Top 10 Störmeldungen (2024–2026)", fontsize=14)
show_and_close()

# -----------------------------
# Plot 2: Störmeldungen pro Monat nach Jahr
# -----------------------------
monthly_year = (
    df.assign(Monat=df["Datum"].dt.month)
    .groupby(["Jahr", "Monat"])
    .size()
    .reset_index(name="Anzahl")
)

pivot_month = monthly_year.pivot(index="Monat", columns="Jahr", values="Anzahl")

fig, ax = plt.subplots(figsize=(12, 6))

colors = {2024: "#2E5EAA", 2025: "#F28E2B", 2026: "#59A14F"}

for year in pivot_month.columns:
    ax.plot(
        pivot_month.index,
        pivot_month[year],
        marker="o",
        linewidth=2,
        label=year,
        color=colors[year],
    )

month_labels = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]

ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_labels)

ax.set_title("Störmeldungen pro Monat nach Jahr")
ax.set_xlabel("Monat")
ax.set_ylabel("Anzahl")
ax.grid(axis="y", linestyle="--", alpha=0.6)
ax.legend(title="Jahr")

show_and_close()

# -----------------------------
# Plot 3: Störmeldungen nach Uhrzeit pro Jahr
# -----------------------------
hour_year = df.groupby(["Jahr", "Stunde"]).size().reset_index(name="Anzahl")

pivot_hour = hour_year.pivot(index="Stunde", columns="Jahr", values="Anzahl").reindex(range(24))

fig, ax = plt.subplots(figsize=(12, 6))

colors = {2024: "#2E5EAA", 2025: "#F28E2B", 2026: "#59A14F"}

for year in pivot_hour.columns:
    ax.plot(
        pivot_hour.index,
        pivot_hour[year],
        label=year,
        color=colors[year],
        linewidth=2.5,
        marker="o",
        markersize=5,
    )

ax.set_title("Störmeldungen nach Uhrzeit pro Jahr")
ax.set_xlabel("Uhrzeit")
ax.set_ylabel("Anzahl")
ax.grid(axis="y", linestyle="--", alpha=0.6)

hours = range(0, 24, 2)
ax.set_xticks(hours)
ax.set_xticklabels([f"{h}:00" for h in hours])

ax.legend(title="Jahr")

show_and_close()

# -----------------------------
# Plot 4: Wochentag vs Jahr
# -----------------------------
heatmap_weekday = df.groupby(["Wochentag", "Jahr"]).size().reset_index(name="Anzahl")

pivot_heatmap = heatmap_weekday.pivot(index="Wochentag", columns="Jahr", values="Anzahl").reindex(
    weekday_order
)

fig, ax = plt.subplots(figsize=(8, 6))

sns.heatmap(pivot_heatmap, cmap="Blues", annot=True, fmt=".0f", ax=ax)

ax.set_title("Störmeldungen: Wochentag vs Jahr")
ax.set_xlabel("Jahr")
ax.set_ylabel("Wochentag")

show_and_close()

# -----------------------------
# Plot 5: Anteil der Prioritäten (%)
# -----------------------------
prio_percent = df["Prio"].value_counts(normalize=True).sort_index() * 100

fig, ax = plt.subplots()

prio_percent.plot(kind="bar", color=["red", "orange", "gray"], ax=ax)

ax.set_title("Anteil der Prioritäten (%)")
ax.set_xlabel("Priorität")
ax.set_ylabel("Prozent")

ax.tick_params(axis="x", rotation=0)

for i, v in enumerate(prio_percent):
    ax.text(i, v + 1, f"{v:.1f}%", ha="center")

show_and_close()

# -----------------------------
# Plot 6: Top Störmeldungen nach Priorität (prozentual)
# -----------------------------
pivot_prio = df.groupby(["Meldung", "Prio"]).size().unstack(fill_value=0)

pivot_prio = pivot_prio.reindex(columns=[0, 1, 2], fill_value=0)

top_errors = pivot_prio.sum(axis=1).sort_values(ascending=False).head(10).index
pivot_prio = pivot_prio.loc[top_errors]

pivot_prio_percent = pivot_prio.div(pivot_prio.sum(axis=1), axis=0) * 100
pivot_prio_percent = pivot_prio_percent.iloc[::-1]

fig, ax = plt.subplots(figsize=(12, 7))

pivot_prio_percent.plot(kind="barh", stacked=True, ax=ax, color=["#D62728", "#F28E2B", "#59A14F"])

ax.set_title("Top 10 Störmeldungen nach Priorität (prozentuale Verteilung)")
ax.set_xlabel("Anteil (%)")
ax.set_ylabel("Störmeldung")
ax.legend(title="Priorität")
ax.grid(axis="x", linestyle="--", alpha=0.6)
ax.set_xlim(0, 100)
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))

for i, (_, row) in enumerate(pivot_prio_percent.iterrows()):
    cumulative = 0
    for value in row:
        if value >= 5:
            ax.text(
                cumulative + value / 2,
                i,
                f"{value:.1f}%",
                ha="center",
                va="center",
                color="white",
                fontsize=9,
                fontweight="bold",
            )
        cumulative += value

show_and_close()

# -----------------------------
# Zusatzanalyse: Peak Oktober 2024
# -----------------------------
oct_2024 = df[(df["Datum"].dt.year == 2024) & (df["Datum"].dt.month == 10)]

print("\nTop 10 Störmeldungen im Oktober 2024:")
print(oct_2024["Meldung"].value_counts().head(10))

print("\nAnzahl aller Störmeldungen im Oktober 2024:")
print(len(oct_2024))
