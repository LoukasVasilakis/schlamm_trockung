import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

plt.close("all")

print("Starte Analyse der Top-3-Störmeldungen...")

# --------------------------------------------------
# Einstellungen
# --------------------------------------------------
DB_URL = "postgresql://postgres:postgres@localhost:5432/pro2d_db"

BLUE = "#2E5EAA"
GRAY = "#B0B0B0"


def shorten_label(text, max_len=45):
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rstrip() + "..."


# --------------------------------------------------
# Daten laden
# --------------------------------------------------
engine = create_engine(DB_URL)

query = """
SELECT "Datum", "Meldung"
FROM events
WHERE "evtTyp" = 'Störmeldungen'
"""

df = pd.read_sql(query, engine)

if df.empty:
    raise SystemExit("Keine Störmeldungen gefunden.")

# --------------------------------------------------
# Daten bereinigen
# --------------------------------------------------
df = df.dropna(subset=["Meldung"]).copy()
df = df[df["Meldung"].str.strip() != ""].copy()

df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")
df = df.dropna(subset=["Datum"]).copy()

if df.empty:
    raise SystemExit("Keine gültigen Daten vorhanden.")

df["Minute"] = df["Datum"].dt.floor("min")

# --------------------------------------------------
# Top 3 Störmeldungen bestimmen
# --------------------------------------------------
error_counts = df["Meldung"].value_counts()
top3_errors = error_counts.head(3).index.tolist()

if len(top3_errors) < 3:
    raise SystemExit("Weniger als 3 unterschiedliche Meldungen vorhanden.")

print("\nTop 3 Störmeldungen:")
for i, err in enumerate(top3_errors, 1):
    print(f"{i}. {err} ({error_counts[err]})")

df_top3 = df[df["Meldung"].isin(top3_errors)].copy()

# --------------------------------------------------
# Kürzere Labels für den Plot
# --------------------------------------------------
label_map = {}
for err in top3_errors:
    if "Drahtbruch" in err:
        label_map[err] = "Drahtbruch - 10% unterschritten"
    elif "Überlauf" in err:
        label_map[err] = "Überlauf - 10% überschritten"
    elif "Signal hat angesprochen" in err:
        label_map[err] = "Signal hat angesprochen"
    else:
        label_map[err] = shorten_label(err)

# --------------------------------------------------
# Pro Minute prüfen, welche Top-3-Meldungen aktiv sind
# --------------------------------------------------
minute_counts = (
    df_top3.groupby(["Minute", "Meldung"])
    .size()
    .unstack(fill_value=0)
)

for err in top3_errors:
    if err not in minute_counts.columns:
        minute_counts[err] = 0

minute_counts = minute_counts[top3_errors]

presence = (minute_counts > 0).astype(int)
presence["anzahl_aktive"] = presence.sum(axis=1)

# --------------------------------------------------
# Reihenfolge im Plot:
# Drahtbruch -> Überlauf -> Signal
# --------------------------------------------------
ordered_errors = []
ordered_errors += [e for e in top3_errors if "Drahtbruch" in e]
ordered_errors += [e for e in top3_errors if "Überlauf" in e]
ordered_errors += [e for e in top3_errors if "Signal hat angesprochen" in e]
ordered_errors += [e for e in top3_errors if e not in ordered_errors]

# --------------------------------------------------
# Daten für Plot aufbauen
# --------------------------------------------------
rows = []

for err in ordered_errors:
    temp = presence[presence[err] == 1]

    allein = (temp["anzahl_aktive"] == 1).sum()
    gemeinsam = (temp["anzahl_aktive"] > 1).sum()
    total = allein + gemeinsam

    allein_pct = 0 if total == 0 else allein / total * 100
    gemeinsam_pct = 0 if total == 0 else gemeinsam / total * 100

    rows.append(
        {
            "Meldung": label_map[err],
            "Gemeinsam": gemeinsam_pct,
            "Allein": allein_pct,
        }
    )

plot_df = pd.DataFrame(rows)

print("\n===== DATEN FÜR PLOT =====")
print(plot_df)

# --------------------------------------------------
# Plot
# --------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))

x = range(len(plot_df))

bars_gemeinsam = ax.bar(x, plot_df["Gemeinsam"], color=BLUE, label="Gemeinsam")
bars_allein = ax.bar(
    x,
    plot_df["Allein"],
    bottom=plot_df["Gemeinsam"],
    color=GRAY,
    label="Allein"
)

# Prozentwerte in die Balken schreiben
for i in range(len(plot_df)):
    gemeinsam = plot_df.iloc[i]["Gemeinsam"]
    allein = plot_df.iloc[i]["Allein"]

    if gemeinsam > 0:
        ax.text(
            i,
            gemeinsam / 2,
            f"{gemeinsam:.1f}%",
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
            fontsize=11
        )

    if allein > 0:
        ax.text(
            i,
            gemeinsam + allein / 2,
            f"{allein:.1f}%",
            ha="center",
            va="center",
            color="black",
            fontweight="bold",
            fontsize=11
        )

ax.set_xticks(list(x))
ax.set_xticklabels(plot_df["Meldung"], rotation=0)
ax.set_ylim(0, 100)

ax.set_ylabel("Anteil (%)", labelpad=15)
ax.set_xlabel("Störmeldung", labelpad=15)
ax.set_title(
    "Analyse des Auftretens der Top-3-Störmeldungen (einzeln vs. gemeinsam)",
    fontsize=15,
    pad=14
)

ax.grid(axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Legende: zuerst Allein, dann Gemeinsam
handles, labels = ax.get_legend_handles_labels()
ax.legend(
    [handles[1], handles[0]],
    ["Allein", "Gemeinsam"],
    loc="upper left",
    bbox_to_anchor=(1.01, 1.0),
    frameon=True
)

plt.tight_layout()
plt.show()
plt.close()

print("\nAnalyse abgeschlossen.")