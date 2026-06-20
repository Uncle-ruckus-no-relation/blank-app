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
        "title": "📊 PVykresľovanie grafických charakteristík",
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
        "x_auto_scale": "Automatické X škálovanie",
        "x_min": "Min X",
        "x_max": "Max X",
        "y_min": "Min Y",
        "y_max": "Max Y",
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
        "x_auto_scale": "Auto X scale",
        "x_min": "Min X",
        "x_max": "Max X",
        "y_min": "Min Y",
        "y_max": "Max Y",
    }
}

# Language selector
lang = st.sidebar.selectbox("Language / Jazyk ", ["Slovak", "English"], index=0)
tx = LANGUAGES.get(lang, LANGUAGES["Slovak"]) 

st.title(tx["title"])
st.markdown(tx["subtitle"])

# ====================== SESSION STATE INIT ======================
if 'series' not in st.session_state:
    st.session_state.series = [
        {"name": "P_k", "color": "#000000", "lw": 1.5, "x_axis": "X1", "y_axis": "Left", "show_markers": False},
        {"name": "U_k", "color": "#ff1472", "lw": 1.5, "x_axis": "X1", "y_axis": "Right 1", "show_markers": False},
        {"name": "cos φ_k", "color": "#00b4f0", "lw": 1.5, "x_axis": "X1", "y_axis": "Right 2", "show_markers": False},
    ]

if 'num_x_axes' not in st.session_state:
    st.session_state.num_x_axes = 1

if 'table_data' not in st.session_state:
    st.session_state.table_data = pd.DataFrame({
        "X1": [1.0, 2.0, 2.91, 3.46, 4.13],
        "P_k": [np.nan]*5,
        "U_k": [np.nan]*5,
        "cos φ_k": [np.nan]*5
    })

# Sync renamed series headers smoothly safely before rendering editor
for i, s in enumerate(st.session_state.series):
    widget_key = f"name_{i}"
    if widget_key in st.session_state and st.session_state[widget_key] != s["name"]:
        old_name = s["name"]
        new_name = st.session_state[widget_key]
        if old_name in st.session_state.table_data.columns:
            st.session_state.table_data.rename(columns={old_name: new_name}, inplace=True)
        s["name"] = new_name


# ====================== SIDEBAR ======================
st.sidebar.header(tx["plot_settings"])
title = st.sidebar.text_input(tx["plot_title"], "Charakteristiky transformátora nakrátko")
x_label = st.sidebar.text_input(tx["x_label"], "Prúd nakrátko [A]")

col_size1, col_size2 = st.sidebar.columns(2)
plot_width = col_size1.number_input(tx["plot_width"], value=12.0, min_value=6.0, max_value=20.0, step=0.5)
plot_height = col_size2.number_input(tx["plot_height"], value=7.0, min_value=4.0, max_value=15.0, step=0.5)

x_scale = st.sidebar.selectbox(tx["x_scale"], ["linear", "log"], index=0)
show_markers = st.sidebar.checkbox(tx["markers"], False)
grid_style = st.sidebar.selectbox(tx["grid"], ["Both", "Major only", "None"], index=0)

legend_location = st.sidebar.selectbox(
    tx["legend_placement"],
    ["best", "upper right", "upper left", "lower right", "lower left", "center right", "center left", "upper center", "lower center", "center", "Below (figure)"],
    index=0,
)
legend_font_size = st.sidebar.number_input(tx["legend_font_size"], value=10, min_value=6, max_value=30, step=1)
legend_font_family = st.sidebar.selectbox(tx["legend_font_family"], ["sans", "serif", "monospace", "cursive", "fantasy", "dejavusans", "times"], index=0)
legend_frame = st.sidebar.checkbox(tx["legend_frame"], False)

auto_x_scale = st.sidebar.checkbox(tx["x_auto_scale"], value=True, key="auto_x_scale")
if not auto_x_scale:
    col_x_min, col_x_max = st.sidebar.columns(2)
    x_min = col_x_min.number_input(tx["x_min"], value=0.0, key="x_min")
    x_max = col_x_max.number_input(tx["x_max"], value=1.0, key="x_max")
else:
    x_min = None
    x_max = None

num_x_axes = st.sidebar.number_input(tx["x_axes"], min_value=1, max_value=4, step=1, key="num_x_axes")
num_right_axes = st.sidebar.number_input(tx["y_axes"], min_value=0, max_value=8, step=1, key="num_right_axes")

uploaded = st.sidebar.file_uploader(tx["csv_import"], type=["csv"])


# ====================== SERIES & DATA ======================
st.header(tx["data_series"])

if uploaded is not None and st.session_state.get('last_uploaded') != uploaded.name:
    try:
        csv_df = pd.read_csv(uploaded)
        if csv_df.shape[1] >= 2:
            st.session_state.table_data = csv_df
            st.session_state.last_uploaded = uploaded.name
            st.session_state.series = []
            for i, col in enumerate(csv_df.columns[1:]):
                st.session_state.series.append({
                    "name": str(col), "color": "#000000", "lw": 1.5, 
                    "x_axis": "X1", "y_axis": "Left" if i == 0 else "Right 1", 
                    "show_markers": False
                })
    except Exception:
        pass

if st.button("➕ " + tx["add_series"]):
    new_idx = len(st.session_state.series) + 1
    st.session_state.series.append({"name": f"Series {new_idx}", "color": "#000000", "lw": 1.5, "x_axis": "X1", "y_axis": "Left", "show_markers": False})


# ====================== DATAFRAME SYNC (OPTIMIZED) ======================
target_x_cols = [f"X{i+1}" for i in range(st.session_state.num_x_axes)]
target_y_cols = [s["name"] for s in st.session_state.series]
target_cols = target_x_cols + target_y_cols

# CRITICAL FIX: Only touch data structure if configuration actually mismatched
if list(st.session_state.table_data.columns) != target_cols:
    synchronized_df = pd.DataFrame(columns=target_cols)
    for c in target_cols:
        if c in st.session_state.table_data.columns:
            synchronized_df[c] = st.session_state.table_data[c]
        else:
            synchronized_df[c] = [np.nan] * len(st.session_state.table_data)
            
    if len(synchronized_df) == 0:
        synchronized_df = pd.DataFrame(np.nan, index=range(5), columns=target_cols)
        
    st.session_state.table_data = synchronized_df

col_config = {}
for c in st.session_state.table_data.columns:
    if c.startswith("X"):
        col_config[c] = st.column_config.NumberColumn(f"🔴 {c}")
    else:
        col_config[c] = st.column_config.NumberColumn(f"🔵 {c}")

st.caption("Hodnoty zadávaj a upravuj priamo v tabuľke (podporuje šípky na klávesnici).")

# CRITICAL FIX: Added explicit 'key' parameter to preserve keyboard focus state entirely
edited_df = st.data_editor(
    st.session_state.table_data, 
    num_rows="dynamic", 
    use_container_width=True, 
    column_config=col_config,
    key="lab_data_editor"
)
st.session_state.table_data = edited_df

x_axis_values = {}
for x_col in target_x_cols:
    x_axis_values[x_col] = pd.to_numeric(edited_df[x_col], errors='coerce').values


# ====================== SERIES CUSTOMIZATION ======================
st.subheader(tx["series_customization"])
existing_right_axes = [int(s["y_axis"].split()[-1]) for s in st.session_state.series if isinstance(s.get("y_axis"), str) and s["y_axis"].startswith("Right ") and s["y_axis"].split()[-1].isdigit()]
axis_count = max(num_right_axes, max(existing_right_axes) if existing_right_axes else 0)

y_axis_options = ["Left"]
if axis_count > 0:
    y_axis_options += [f"Right {i+1}" for i in range(axis_count)]

x_axis_options = target_x_cols

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
            s["x_axis"] = x_axis_options[0] if x_axis_options else "X1"
            
        new_x_axis = st.selectbox(tx["x_axis"], x_axis_options, index=x_axis_options.index(s.get("x_axis","X1")) if s.get("x_axis","X1") in x_axis_options else 0, key=f"x_axis_{i}")
        
        if s.get("y_axis") not in y_axis_options:
            s["y_axis"] = y_axis_options[0]
            
        new_y_axis = st.selectbox(tx["y_axis"], y_axis_options, index=y_axis_options.index(s.get("y_axis")) if s.get("y_axis") in y_axis_options else 0, key=f"y_axis_{i}")
        new_show = st.checkbox(tx["show_markers_series"], value=s.get("show_markers", False), key=f"show_markers_{i}")
        
        st.divider()
        st.write("**Y-Axis Scaling**")
        auto_scale_y = st.checkbox(f"Auto scale Y", value=s.get("auto_scale_y", True), key=f"auto_scale_y_{i}")
        if not auto_scale_y:
            col_y1, col_y2 = st.columns(2)
            y_min = col_y1.number_input(f"Min Y", value=float(s.get("y_min", 0.0)), key=f"y_min_{i}")
            y_max = col_y2.number_input(f"Max Y", value=float(s.get("y_max", 1.0)), key=f"y_max_{i}")
            s["y_min"] = y_min
            s["y_max"] = y_max
            s["auto_scale_y"] = False
        else:
            s["auto_scale_y"] = True
        
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
axes_map = {}
y_axes = {"Left": ax}

for idx in range(1, len(y_axis_options)):
    y_name = y_axis_options[idx]
    new_ax = ax.twinx()
    new_ax.spines['right'].set_position(('axes', 1.0 + 0.12 * (idx - 1)))
    new_ax.set_frame_on(True)
    new_ax.patch.set_visible(False)
    y_axes[y_name] = new_ax

for y_name, y_ax in y_axes.items():
    for x_name in x_axis_options:
        axes_map[(x_name, y_name)] = y_ax

for s in st.session_state.series:
    if s["name"] not in edited_df.columns:
        continue
    y = pd.to_numeric(edited_df[s["name"]], errors='coerce').values.astype(float)
    x_axis_name = s.get("x_axis", "X1")
    x_vals = x_axis_values.get(x_axis_name, None)
    
    if x_vals is None:
        x_vals = np.array([np.nan] * len(y), dtype=float)
    else:
        x_vals = np.asarray(x_vals, dtype=float)
        if x_vals.shape[0] < y.shape[0]:
            x_vals = np.pad(x_vals, (0, y.shape[0] - x_vals.shape[0]), constant_values=np.nan)
        elif x_vals.shape[0] > y.shape[0]:
            x_vals = x_vals[: y.shape[0]]
            
    mask = ~np.isnan(y) & np.isfinite(x_vals)
    if mask.sum() < 2:
        continue

    y_axis_name = s.get("y_axis", "Left")
    current_ax = axes_map.get((x_axis_name, y_axis_name), ax)

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

    series_show = s.get('show_markers', None)
    plot_markers = bool(show_markers) if series_show is None else bool(series_show)

    try:
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
        p, = current_ax.plot(x_u, y_u, color=s["color"], lw=s["lw"], label=s["name"])
        if plot_markers:
            current_ax.plot(x_u, y_u, 'o', color=s["color"], ms=6, alpha=0.8)
        handles.append(p)
        labels.append(s["name"])

# Styling
title_fs = max(legend_font_size + 6, 12)
label_fs = max(legend_font_size + 2, 10)
tick_fs = max(legend_font_size, 8)
font_props = FontProperties(family=legend_font_family)

ax.set_title(title, fontsize=title_fs, pad=20, fontfamily=legend_font_family)
ax.set_xlabel(x_label, fontsize=label_fs, fontfamily=legend_font_family)

if st.session_state.series:
    first = st.session_state.series[0]
    ax.set_ylabel(first["name"], color=first["color"], fontsize=label_fs, fontfamily=legend_font_family)
    ax.tick_params(axis='y', colors=first["color"], labelsize=tick_fs)
    ax.tick_params(axis='x', labelsize=tick_fs)
    try:
        ax.spines['left'].set_color(first["color"])
    except Exception:
        pass
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        try:
            lbl.set_fontproperties(font_props)
        except Exception:
            pass

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

if grid_style == "Both":
    ax.grid(which='major', linestyle='-', linewidth=1.2, alpha=0.8)
    ax.grid(which='minor', linestyle=':', linewidth=0.9, alpha=0.6)
    ax.minorticks_on()
elif grid_style == "Major only":
    ax.grid(which='major', linestyle='-', linewidth=1.2, alpha=0.8)
    ax.minorticks_on()

if grid_style != "None":
    for y_name, rax in y_axes.items():
        try:
            rax.minorticks_on()
        except Exception:
            pass

if auto_x_scale:
    all_valid_x = []
    for arr in x_axis_values.values():
        valid = arr[np.isfinite(arr)]
        if valid.size > 0:
            all_valid_x.extend(valid.tolist())
            
    if all_valid_x:
        all_valid_x = np.array(all_valid_x)
        if x_scale == 'log':
            pos = all_valid_x[all_valid_x > 0]
            if pos.size > 0:
                ax.set_xlim(pos.min(), pos.max())
        else:
            ax.set_xlim(all_valid_x.min(), all_valid_x.max())
else:
    if x_min is not None and x_max is not None and x_max > x_min:
        if x_scale == 'log':
            pos_min, pos_max = max(x_min, 1e-9), max(x_max, 1e-9)
            if pos_max > pos_min:
                ax.set_xlim(pos_min, pos_max)
        else:
            ax.set_xlim(x_min, x_max)

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

if handles:
    legend_props = FontProperties(family=legend_font_family, size=legend_font_size)
    if legend_location == "Below (figure)":
        fig.legend(
            handles=handles, labels=labels, loc='lower center',
            bbox_to_anchor=(0.5, -0.12), ncol=max(1, len(handles)),
            frameon=legend_frame, prop=legend_props,
        )
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
    to_csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button(tx["download_csv"], data=to_csv, file_name="series_data.csv", mime='text/csv')
with col_b:
    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png', dpi=200)
    buf.seek(0)
    st.download_button(tx["download_png"], data=buf, file_name="plot.png", mime='image/png')
