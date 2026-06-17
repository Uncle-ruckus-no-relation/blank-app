import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy.interpolate import PchipInterpolator
from io import BytesIO


st.set_page_config(page_title="Electronics Lab Plotter", layout="wide")

# ====================== LANGUAGE SUPPORT ======================
LANGUAGES = {
    "Slovak": {
        "title": "📊 Vykresľovanie grafických charakteristík",
        "subtitle": "**Nástroj na vykresľovanie priebehov pre elektrotechnické merania**",
        "plot_settings": "Nastavenia grafu",
        "plot_title": "Názov grafu",
        "x_label": "Označenie osi X",
        "plot_width": "Šírka grafu (palce)",
        "plot_height": "Výška grafu (palce)",
        "x_scale": "Stupnica X",
        "markers": "Zobraziť dátové markery",
        "grid": "Mriežka",
        "legend_placement": "Umiestnenie legendy",
        "legend_font_size": "Veľkosť písma legendy",
        "legend_font_family": "Rodina písma legendy",
        "legend_frame": "Zobraziť rámec legendy",
        "csv_import": "Importovať CSV",
        "data_series": "Dátové série a hodnoty",
        "add_series": "Pridať novú sériu",
        "remove_series": "Odstrániť poslednú",
        "x_values": "Hodnoty X (čiarkami oddelené)",
        "series_customization": "Prispôsobenie série",
        "plot_header": "Graf",
        "export_header": "Export / Uložiť",
        "download_csv": "Stiahnuť CSV",
        "download_png": "Stiahnuť PNG",
        "color": "Farba",
        "line_width": "Šírka čiary",
        "axis": "Os",
        "show_markers_series": "Zobraziť markery pre túto sériu",
        "x_axis": "X os",
        "y_axis": "Y os",
        "x_axes": "Počet X osí",
        "y_axes": "Počet pravých Y osí",
        "y_min": "Min Y",
        "y_max": "Max Y",
        "right_axes": "Počet pravých osí",
    },
    "English": {
        "title": "📊 Plotting Graphics Characteristics",
        "subtitle": "**Curve plotting tool for electrical measurements**",
        "plot_settings": "Plot Settings",
        "plot_title": "Plot Title",
        "x_label": "X-axis Label",
        "plot_width": "Plot Width (inches)",
        "plot_height": "Plot Height (inches)",
        "x_scale": "X Scale",
        "markers": "Show data markers",
        "grid": "Grid",
        "legend_placement": "Legend placement",
        "legend_font_size": "Legend font size",
        "legend_font_family": "Legend font family",
        "legend_frame": "Show legend frame",
        "csv_import": "Import CSV",
        "data_series": "Data Series & Values",
        "add_series": "Add New Series",
        "remove_series": "Remove Last",
        "x_values": "X values (comma separated)",
        "series_customization": "Series Customization",
        "plot_header": "Plot",
        "export_header": "Export / Save",
        "download_csv": "Download CSV",
        "download_png": "Download PNG",
        "color": "Color",
        "line_width": "Line width",
        "axis": "Axis",
        "show_markers_series": "Show markers for this series",
        "x_axis": "X axis",
        "y_axis": "Y axis",
        "x_axes": "Number of X axes",
        "y_axes": "Number of right Y axes",
        "y_min": "Min Y",
        "y_max": "Max Y",
        "right_axes": "Number of right axes",
    },
    "Russian": {
        "title": "📊 Построение графических характеристик",
        "subtitle": "**Инструмент для построения графиков для электротехнических измерений**",
        "plot_settings": "Параметры графика",
        "plot_title": "Название графика",
        "x_label": "Метка оси X",
        "plot_width": "Ширина графика (дюймы)",
        "plot_height": "Высота графика (дюймы)",
        "x_scale": "Масштаб X",
        "markers": "Показывать маркеры данных",
        "grid": "Сетка",
        "legend_placement": "Размещение легенды",
        "legend_font_size": "Размер шрифта легенды",
        "legend_font_family": "Семейство шрифтов легенды",
        "legend_frame": "Показать кадр легенды",
        "csv_import": "Импорт CSV",
        "data_series": "Серии данных и значения",
        "add_series": "Добавить новую серию",
        "remove_series": "Удалить последнюю",
        "x_values": "Значения X (через запятую)",
        "series_customization": "Настройка серии",
        "plot_header": "График",
        "export_header": "Экспорт / Сохранить",
        "download_csv": "Загрузить CSV",
        "download_png": "Загрузить PNG",
        "color": "Цвет",
        "line_width": "Ширина линии",
        "axis": "Ось",
        "show_markers_series": "Показать маркеры для этой серии",
        "x_axis": "Ось X",
        "y_axis": "Ось Y",
        "x_axes": "Количество осей X",
        "y_axes": "Количество правых осей Y",
        "y_min": "Мин Y",
        "y_max": "Макс Y",
    },
    "Serbian": {
        "title": "📊 Crtanje grafičkih karakteristika",
        "subtitle": "**Alat za crtanje grafika za elektrotehnička mjerenja**",
        "plot_settings": "Postavke grafikona",
        "plot_title": "Naslov grafikona",
        "x_label": "Oznaka X ose",
        "plot_width": "Širina grafikona (inči)",
        "plot_height": "Visina grafikona (inči)",
        "x_scale": "X skala",
        "markers": "Prikaži markere podataka",
        "grid": "Mreža",
        "legend_placement": "Položaj legende",
        "legend_font_size": "Veličina fonta legende",
        "legend_font_family": "Porodica fontova legende",
        "legend_frame": "Prikaži okvir legende",
        "csv_import": "Uvezi CSV",
        "data_series": "Serije podataka i vrednosti",
        "add_series": "Dodaj novu seriju",
        "remove_series": "Ukloni poslednju",
        "x_values": "X vrednosti (odvojene zarezom)",
        "series_customization": "Prilagođavanje serije",
        "plot_header": "Grafikon",
        "export_header": "Izvoz / Sačuvaj",
        "download_csv": "Preuzmi CSV",
        "download_png": "Preuzmi PNG",
        "color": "Boja",
        "line_width": "Debljina linije",
        "axis": "Osa",
        "show_markers_series": "Prikaži markere za ovu seriju",
        "x_axis": "X osa",
        "y_axis": "Y osa",
        "x_axes": "Broj X osa",
        "y_axes": "Broj desnih Y osa",
        "y_min": "Min Y",
        "y_max": "Maks Y",
    },
}

# Language selector
lang = st.sidebar.selectbox("Language / Jezik / Язык / Језик", list(LANGUAGES.keys()), index=0)
tx = LANGUAGES[lang]  # Translation function

st.title(tx["title"])
st.markdown(tx["subtitle"])

# Initialize series in session state (must happen before sidebar controls access it)
if 'series' not in st.session_state:
    st.session_state.series = [
        {"name": "P_k", "color": "#000000", "lw": 1, "x_axis": "X1", "y_axis": "Left", "show_markers": False},
        {"name": "U_k", "color": "#ff1472", "lw": 1, "x_axis": "X1", "y_axis": "Right 1", "show_markers": False},
        {"name": "cos φ_k", "color": "#00b4f0", "lw": 1, "x_axis": "X1", "y_axis": "Right 2", "show_markers": False},
    ]

if 'x_input' not in st.session_state:
    st.session_state.x_input = "1, 2, 2.91, 3.46, 4.13"

if 'num_x_axes' not in st.session_state:
    st.session_state.num_x_axes = 2


def parse_number_list(value_str):
    if not isinstance(value_str, str):
        return []
    normalized = value_str.replace(';', ',').replace('−', '-')
    values = []
    for token in normalized.split(','):
        token = token.strip()
        if not token:
            continue
        try:
            values.append(float(token))
        except ValueError:
            try:
                values.append(float(token.replace(',', '.')))
            except ValueError:
                continue
    return values


# ====================== SIDEBAR ======================
st.sidebar.header(tx["plot_settings"])

title = st.sidebar.text_input(tx["plot_title"], "Charakteristiky transformátora nakrátko")
x_label = st.sidebar.text_input(tx["x_label"], "Prúd nakrátko [A]")

col_size1, col_size2 = st.sidebar.columns(2)
plot_width = col_size1.number_input(tx["plot_width"], value=12.0, min_value=6.0, max_value=20.0, step=0.5)
plot_height = col_size2.number_input(tx["plot_height"], value=7.0, min_value=4.0, max_value=15.0, step=0.5)

x_scale = st.sidebar.selectbox(tx["x_scale"], ["linear", "log"], index=0)
show_markers = st.sidebar.checkbox(tx["markers"], False)  # Default unchecked
grid_style = st.sidebar.selectbox(tx["grid"], ["Both", "Major only", "None"], index=0)

# Legend customization
legend_location = st.sidebar.selectbox(
    tx["legend_placement"],
    ["best", "upper right", "upper left", "lower right", "lower left", "center right", "center left", "upper center", "lower center", "center", "Below (figure)"],
    index=0,
)
legend_font_size = st.sidebar.number_input(tx["legend_font_size"], value=10, min_value=6, max_value=30, step=1)
legend_font_family = st.sidebar.selectbox(tx["legend_font_family"], ["sans", "serif", "monospace", "cursive", "fantasy", "dejavusans", "times"], index=0)
legend_frame = st.sidebar.checkbox(tx["legend_frame"], False)
num_x_axes = st.sidebar.number_input(tx["x_axes"], min_value=1, max_value=4, value=st.session_state.num_x_axes, step=1, key="num_x_axes")
num_right_axes = st.sidebar.number_input(tx["y_axes"], min_value=1, max_value=8, value=st.session_state.get("num_right_axes", 3), step=1, key="num_right_axes")

# CSV import
uploaded = st.sidebar.file_uploader(tx["csv_import"] + " (first column X, other columns series)", type=["csv"])


# ====================== SERIES & DATA ======================
st.header(tx["data_series"])

# Add / Remove
col1, col2 = st.columns([1,1])
with col1:
    if st.button("➕ " + tx["add_series"]):
        st.session_state.series.append({"name": f"Series {len(st.session_state.series)+1}", 
                                      "color": "#000000", "lw": 1.5, "x_axis": "X1", "y_axis": "Right 1", "show_markers": False})

# X values input (or from CSV) for the first axis (X1)
col_x_buttons, col_x_info = st.columns([1, 6])
with col_x_buttons:
    if st.button("➕ Add X vector"):
        st.session_state.num_x_axes = min(4, st.session_state.num_x_axes + 1)
        st.experimental_rerun()
    if st.button("➖ Remove X vector") and st.session_state.num_x_axes > 1:
        st.session_state.num_x_axes -= 1
        st.experimental_rerun()
with col_x_info:
    st.markdown("**X vectors:** create multiple X value columns and assign them per series.")

x_input = st.text_input(tx["x_values"] + " (X1)", value=st.session_state.x_input, key="x_input")
x_list = parse_number_list(x_input)
if not x_list:
    x_list = [1, 2, 3, 4, 5]
    st.session_state.x_input = "1, 2, 3, 4, 5"

# If CSV uploaded, read and populate
if uploaded is not None:
    try:
        csv_df = pd.read_csv(uploaded)
        if csv_df.shape[1] >= 2:
            # first column -> X
            x_list = csv_df.iloc[:,0].astype(float).tolist()
            # populate series from other columns
            st.session_state.series = []
            for col in csv_df.columns[1:]:
                st.session_state.series.append({"name": str(col), "color": "#000000", "lw": 1.5, "x_axis": "X1", "y_axis": "Right 1", "show_markers": False})
            data_df = csv_df.copy()
        else:
            data_df = None
    except Exception:
        data_df = None
else:
    data_df = None

# Data table construction
x_column_names = [f"X{i+1}" for i in range(st.session_state.num_x_axes)]

x_axis_values = {x_column_names[0]: x_list}
for name in x_column_names[1:]:
    x_axis_values[name] = [None] * len(x_list)

data = {name: x_axis_values[name] for name in x_column_names}
for s in st.session_state.series:
    if data_df is not None and s["name"] in data_df.columns:
        data[s["name"]] = pd.to_numeric(data_df[s["name"]]).tolist()
    else:
        data[s["name"]] = [None] * len(x_list)

df = st.data_editor(pd.DataFrame(data), num_rows="dynamic", use_container_width=True, key="series_table")

# If the user edits the X values in the table, use those values for plotting.
x_axis_values = {}
for name in x_column_names:
    if name in df.columns:
        x_axis_values[name] = pd.to_numeric(df[name], errors='coerce').values
    else:
        x_axis_values[name] = np.array([np.nan] * len(x_list))

if np.any(np.isfinite(x_axis_values[x_column_names[0]])):
    # Don't assign to session_state during build (can raise StreamlitAPIException).
    # Keep a local preview variable instead; user can edit X1 in the text input above.
    x_input_preview = ", ".join([str(v) for v in x_axis_values[x_column_names[0]] if np.isfinite(v)])
st.caption("Edit values directly in the table or import a CSV" if lang == "English" else "Upravte hodnoty priamo v tabuľke alebo importujte CSV" if lang == "Slovak" else "Редактируйте значения в таблице или импортируйте CSV" if lang == "Russian" else "Uređujte vrednosti direktno u tabeli ili uvezite CSV")


# ====================== SERIES CUSTOMIZATION ======================
st.subheader(tx["series_customization"])
existing_right_axes = [int(s["y_axis"].split()[-1]) for s in st.session_state.series if isinstance(s.get("y_axis"), str) and s["y_axis"].startswith("Right ") and s["y_axis"].split()[-1].isdigit()]
axis_count = max(num_right_axes, max(existing_right_axes) if existing_right_axes else 1)
y_axis_options = ["Left"] + [f"Right {i+1}" for i in range(axis_count)]
x_axis_options = [f"X{i+1}" for i in range(st.session_state.num_x_axes)]
for i, s in enumerate(st.session_state.series):
    with st.expander(f"Series {i+1}: {s['name']}", expanded=(i==0)):
        col_exp1, col_exp2 = st.columns([4, 1])
        with col_exp1:
            new_name = st.text_input(f"Name (series {i+1})", value=s["name"], key=f"name_{i}")
        with col_exp2:
            if st.button("🗑️", key=f"remove_{i}"):
                st.session_state.series.pop(i)
                st.rerun()
        
        new_color = st.color_picker(tx["color"], value=s.get("color", "#000000"), key=f"color_{i}")
        new_lw = st.number_input(tx["line_width"], value=float(s.get("lw",1.5)), min_value=0.5, max_value=10.0, step=0.1, key=f"lw_{i}")
        if s.get("x_axis") not in x_axis_options:
            s["x_axis"] = x_axis_options[0]
        new_x_axis = st.selectbox(tx["x_axis"], x_axis_options, index=x_axis_options.index(s.get("x_axis","X1")), key=f"x_axis_{i}")
        if s.get("y_axis") not in y_axis_options:
            s["y_axis"] = y_axis_options[0]
        new_y_axis = st.selectbox(tx["y_axis"], y_axis_options, index=y_axis_options.index(s.get("y_axis","Right 1")) if s.get("y_axis","Right 1") in y_axis_options else 1, key=f"y_axis_{i}")
        new_show = st.checkbox(tx["show_markers_series"], value=s.get("show_markers", False), key=f"show_markers_{i}")
        
        # Y-axis scaling for this series
        st.divider()
        st.write("**Y-Axis Scaling**")
        auto_scale = st.checkbox(f"Auto scale Y", value=s.get("auto_scale_y", True), key=f"auto_scale_y_{i}")
        if not auto_scale:
            col_y1, col_y2 = st.columns(2)
            y_min = col_y1.number_input(f"Min Y", value=float(s.get("y_min", 0.0)), key=f"y_min_{i}")
            y_max = col_y2.number_input(f"Max Y", value=float(s.get("y_max", 1.0)), key=f"y_max_{i}")
            s["y_min"] = y_min
            s["y_max"] = y_max
            s["auto_scale_y"] = False
        else:
            s["auto_scale_y"] = True
        
        # apply changes back to session_state
        s["name"] = new_name
        s["color"] = new_color
        s["lw"] = float(new_lw)
        s["x_axis"] = new_x_axis
        s["y_axis"] = new_y_axis
        s["show_markers"] = bool(new_show)


# ====================== PLOTTING ======================
st.header(tx["plot_header"])
fig = plt.figure(figsize=(plot_width, plot_height))
ax = fig.add_subplot(111)
if x_scale == 'log':
    ax.set_xscale('log')

handles = []
labels = []

# Build axes so every series can plot against a chosen X axis and a chosen Y axis.
axes_map = {}
y_axes = {"Left": ax}
for idx in range(1, len(y_axis_options)):
    y_name = y_axis_options[idx]
    new_ax = ax.twinx()
    new_ax.spines['right'].set_position(('axes', 1.08 + 0.12 * (idx - 1)))
    new_ax.set_frame_on(True)
    new_ax.patch.set_visible(False)
    y_axes[y_name] = new_ax

for y_name, y_ax in y_axes.items():
    for x_idx, x_name in enumerate(x_axis_options):
        if x_idx == 0:
            axes_map[(x_name, y_name)] = y_ax
        else:
            new_x = y_ax.twiny()
            new_x.spines['top'].set_position(('axes', 1.0 + 0.12 * (x_idx - 1)))
            new_x.xaxis.set_label_position('top')
            new_x.xaxis.set_ticks_position('top')
            new_x.spines['top'].set_visible(True)
            new_x.set_frame_on(True)
            new_x.patch.set_visible(False)
            new_x.set_xlabel(x_name)
            axes_map[(x_name, y_name)] = new_x

for s in st.session_state.series:
    if s["name"] not in df.columns:
        continue
    y = pd.to_numeric(df[s["name"]], errors='coerce').values.astype(float)
    x_axis_name = s.get("x_axis", "X1")
    x_vals = x_axis_values.get(x_axis_name, np.array([np.nan] * len(y), dtype=float))
    mask = ~np.isnan(y) & np.isfinite(x_vals)
    if mask.sum() < 2:
        continue

    y_axis_name = s.get("y_axis", "Left")
    current_ax = axes_map.get((x_axis_name, y_axis_name), ax)

    # prepare data: aggregate duplicate X values and sort
    x_masked = x_vals[mask]
    y_masked = y[mask]
    df_xy = pd.DataFrame({"x": x_masked, "y": y_masked})
    df_xy = df_xy.groupby('x', as_index=False).mean()
    x_u = df_xy['x'].values
    y_u = df_xy['y'].values
    if x_u.size < 2:
        continue
    sort_idx = np.argsort(x_u)
    x_u = x_u[sort_idx]
    y_u = y_u[sort_idx]

    # determine whether to show markers for this series (per-series overrides global)
    series_show = s.get('show_markers', None)
    if series_show is None:
        plot_markers = bool(show_markers)
    else:
        plot_markers = bool(series_show)

    try:
        # For log scale, ensure positive x
        if x_scale == 'log' and np.any(x_u <= 0):
            x_smooth = np.linspace(x_u.min(), x_u.max(), 1000)
        elif x_scale == 'log':
            x_smooth = np.logspace(np.log10(x_u.min()), np.log10(x_u.max()), 1000)
        else:
            x_smooth = np.linspace(x_u.min(), x_u.max(), 1000)

        pchip = PchipInterpolator(x_u, y_u)
        y_smooth = pchip(x_smooth)
        p, = current_ax.plot(x_smooth, y_smooth, color=s["color"], lw=s["lw"], label=s["name"])
        if plot_markers:
            current_ax.plot(x_u, y_u, 'o', color=s["color"], ms=6, alpha=0.8)
        handles.append(p)
        labels.append(s["name"])
    except Exception:
        # fallback: plot raw (unique) points
        p, = current_ax.plot(x_u, y_u, color=s["color"], lw=s["lw"], label=s["name"])
        if plot_markers:
            current_ax.plot(x_u, y_u, 'o', color=s["color"], ms=6, alpha=0.8)
        handles.append(p)
        labels.append(s["name"])

# Styling
# Apply fonts and sizes based on legend controls (title slightly larger)
title_fs = max(legend_font_size + 6, 12)
label_fs = max(legend_font_size + 2, 10)
tick_fs = max(legend_font_size, 8)
font_props = FontProperties(family=legend_font_family)

# Title and X label
ax.set_title(title, fontsize=title_fs, pad=20, fontfamily=legend_font_family)
ax.set_xlabel(x_label, fontsize=label_fs, fontfamily=legend_font_family)

# Left axis label and ticks
if st.session_state.series:
    first = st.session_state.series[0]
    ax.set_ylabel(first["name"], color=first["color"], fontsize=label_fs, fontfamily=legend_font_family)
    ax.tick_params(axis='y', colors=first["color"], labelsize=tick_fs)
    ax.tick_params(axis='x', labelsize=tick_fs)
    try:
        ax.spines['left'].set_color(first["color"])
    except Exception:
        pass
    # apply font family to tick labels
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        try:
            lbl.set_fontproperties(font_props)
        except Exception:
            pass

# Right axis labels color sync and font (optional)
for y_name, rax in y_axes.items():
    if y_name == "Left":
        continue
    series_on_axis = [s for s in st.session_state.series if s.get("y_axis") == y_name]
    if series_on_axis:
        first_series = series_on_axis[0]
        rax.set_ylabel(first_series["name"], color=first_series["color"], fontsize=label_fs, fontfamily=legend_font_family)
        try:
            rax.spines['right'].set_color(first_series["color"])
        except Exception:
            pass
        rax.tick_params(axis='y', colors=first_series["color"], labelsize=tick_fs)
    try:
        rax.spines['right'].set_visible(True)
    except Exception:
        pass
    try:
        for lbl in rax.get_yticklabels():
            try:
                lbl.set_fontproperties(font_props)
            except Exception:
                pass
    except Exception:
        pass

# Grid styling: strong major lines and dotted minor lines (matching provided script)
if grid_style == "Both":
    ax.grid(which='major', linestyle='-', linewidth=1.2, alpha=0.8)
    ax.grid(which='minor', linestyle=':', linewidth=0.9, alpha=0.6)
    ax.minorticks_on()
elif grid_style == "Major only":
    ax.grid(which='major', linestyle='-', linewidth=1.2, alpha=0.8)
    ax.minorticks_on()
# ensure right axes also show minor ticks and similar grid lines if requested
if grid_style != "None":
    for y_name, rax in y_axes.items():
        try:
            rax.minorticks_on()
        except Exception:
            pass

# Stabilize x-limits so resizing doesn't create odd autoscaling shapes
valid_x = x_axis_values[x_column_names[0]][np.isfinite(x_axis_values[x_column_names[0]])]
if valid_x.size > 0:
    if x_scale == 'log':
        pos = valid_x[valid_x > 0]
        if pos.size > 0:
            ax.set_xlim(pos.min(), pos.max())
    else:
        ax.set_xlim(valid_x.min(), valid_x.max())

# Apply per-series Y scaling (collect all series on each axis and apply their scaling)
axis_scaling = {y_name: None for y_name in y_axis_options}
for s in st.session_state.series:
    axis_name = s.get("y_axis", "Left")
    if not s.get("auto_scale_y", True):
        y_min = s.get("y_min", 0.0)
        y_max = s.get("y_max", 1.0)
        axis_scaling[axis_name] = (y_min, y_max)

for y_name, rax in y_axes.items():
    if axis_scaling.get(y_name) is not None:
        rax.set_ylim(axis_scaling[y_name][0], axis_scaling[y_name][1])

# Legend
if handles:
    # Create FontProperties for consistent font styling
    legend_props = FontProperties(family=legend_font_family, size=legend_font_size)
    
    # If user wants the legend below the figure, place it as a figure legend
    if legend_location == "Below (figure)":
        fig.legend(
            handles=handles,
            labels=labels,
            loc='lower center',
            bbox_to_anchor=(0.5, -0.12),
            ncol=max(1, len(handles)),
            frameon=legend_frame,
            prop=legend_props,
        )
        # leave space for the legend below
        try:
            fig.subplots_adjust(bottom=0.20)
        except Exception:
            pass
    else:
        ax.legend(handles=handles, labels=labels, loc=legend_location, frameon=legend_frame, prop=legend_props)

st.pyplot(fig)


# ====================== EXPORTS ======================
st.header(tx["export_header"])
col_a, col_b = st.columns(2)
with col_a:
    # CSV download
    to_csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(tx["download_csv"], data=to_csv, file_name="series_data.csv", mime='text/csv')
    # PNG download
with col_b:
    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png', dpi=200)
    buf.seek(0)
    st.download_button(tx["download_png"], data=buf, file_name="plot.png", mime='image/png')

st.caption("Tip: Edit the data table or import a CSV. Add/remove series in the top controls." if lang == "English" else "Tip: Upravte tabuľku alebo importujte CSV. Pridajte/odstráňte série vyššie." if lang == "Slovak" else "Совет: отредактируйте таблицу или импортируйте CSV. Добавляйте/удаляйте серии выше." if lang == "Russian" else "Savet: Uređujte tabelu ili uvezite CSV. Dodajte/uklonite serije gore.")
