<div align="center">

# 🚦 UrbanFlow
**Adaptive Route Intelligence for Narwana, Haryana**

Interactive shortest-path routing with live traffic simulation and real GPS-based visualization for 13 locations in Narwana town, Jind District.

![Status](https://img.shields.io/badge/status-active-brightgreen) ![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B) ![Python](https://img.shields.io/badge/Python-3.10+-3776AB) ![License](https://img.shields.io/badge/license-Educational-blue)

</div>

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🗺️ **Geographic Visualization** | Real-world positioning using GPS coordinates (29.59°N, 76.11°E) with adaptive scaling |
| 🚀 **Route Planning** | Dijkstra's shortest path algorithm - O((V+E) log V) complexity |
| 🔄 **Dynamic Network** | Add/remove locations and roads at runtime (in-memory editing) |
| 🚦 **Traffic Simulation** | Adjust bidirectional edge weights (travel time in minutes) live |
| 🎨 **Multiple Layouts** | 5 visualization modes: Geographic, Spring, Kamada-Kawai, Circular, Shell |
| 🎯 **Styling Controls** | Edge colors, weight labels, width scaling, adjustable label sizes |
| ✨ **Path Highlighting** | Multi-layer glow effect on shortest path edges |
| 📊 **Progress Feedback** | Staged progress bar with simulated route computation steps |
| 📈 **Metrics Dashboard** | Route history, network statistics, modification tracking |
| 🌙 **Dark Theme** | Custom dark UI with enhanced typography (3.2rem title) |

---

## 🗂 Project Structure

```
📦 UrbanFlow/
├── 📄 app.py                 # Main Streamlit application (645 lines)
│                              ├─ UI layout with custom CSS
│                              ├─ Geographic coordinate system (NARWANA_COORDINATES)
│                              ├─ 5 layout algorithms with adaptive scaling
│                              ├─ Interactive network editor
│                              └─ Route computation with staged progress bar
│
├── 📄 data_loader.py         # Base road network data (181 lines)
│                              ├─ get_road_network() - 13 locations, 29 connections
│                              ├─ get_locations() - sorted location list
│                              ├─ get_edge_list() - deduplicated edges
│                              └─ update_traffic_weight() - bidirectional updates
│
├── 📄 utils.py               # Pathfinding algorithms (153 lines)
│                              ├─ dijkstra_shortest_path() - O((V+E) log V)
│                              ├─ get_path_edges() - path to edge conversion
│                              └─ format_path_display() - UI formatting
│
├── 📄 requirements.txt       # Python dependencies
├── 📄 README.md              # This documentation
└── 📁 .streamlit/            # Streamlit configuration
    └── config.toml           # Theme settings
```

**Core Technologies:**
- **Frontend:** Streamlit 1.32+ (reactive UI framework)
- **Graph Library:** NetworkX 3.2+ (visualization only, **not** used for pathfinding)
- **Plotting:** Matplotlib 3.8+ with custom colormaps
- **Scientific:** SciPy 1.10+ for advanced layout algorithms (Kamada-Kawai)
- **HTTP:** Requests 2.31+ (for future API integration)

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ayushmittal62/Urban-Flow.git
cd Urban-Flow

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The app will open in your browser at **http://localhost:8501** (or next available port).

**System Requirements:**
- Python 3.10+ (tested on 3.12)
- 4GB RAM minimum
- Modern web browser (Chrome, Firefox, Edge)

**First Run:**
1. Wait for Streamlit to compile (~5-10 seconds)
2. Default network with 13 Narwana locations loads automatically
3. Geographic layout is set as the default visualization mode

---

## 🧭 Using UrbanFlow

### Basic Route Planning

1. **Select Locations**  
   Choose source and destination from the dropdown menus

2. **Compute Route**  
   Click **"⚡ Step 1 · Compute Fastest Route"**
   - Watch the 5-stage progress bar (simulated UX feedback)
   - Stages: *Initializing → Building → Scanning → Exploring → Finalizing*

3. **View Results**  
   Route card displays:
   - Total travel time (minutes)
   - Complete path with arrows (A → B → C → D)
   - Number of intermediate stops
   - Route history log

### Visualization Controls

**Display Settings Panel:**

**Layout Algorithms** (5 modes):
- 🗺️ **Geographic** (default) - Real GPS positioning with adaptive scaling
- 🌸 **Spring** - Force-directed physics simulation
- 🎯 **Kamada-Kawai** - Graph-theoretic energy minimization
- ⭕ **Circular** - Nodes arranged in a circle
- 🐚 **Shell** - Concentric circles by connectivity

**Styling Toggles:**
- ✅ Show edge weight labels (travel time in minutes)
- 🎨 Enable gradient colors (Blues colormap scaled by weight)
- 📏 Scale edge width proportionally to travel time
- 🔤 Adjust node label font size (6-20pt slider)

### Network Editing

**Traffic & Network Editor** (expandable section):

#### 1. Modify Traffic
- Select a road from dropdown (e.g., "Railway Station ↔ Bus Stand")
- Adjust weight slider (1-15 minutes)
- Click **"Update Weight"** → updates both directions automatically

#### 2. Add Location
- Enter new location name in text input
- Click **"Add Location"** → node appears in all dropdowns instantly

#### 3. Add Road
- Select two existing locations (source & destination)
- Set travel time weight (slider)
- Click **"Add Road"** → creates bidirectional connection

#### 4. Remove Elements
- Select road or location from respective dropdowns
- Click remove button → graph updates in real-time

#### 5. Network Reset
- **"Clear All Roads"** - Removes all edges (keeps nodes) ⚠️ Danger Zone
- **"Restore Default Network"** - Reloads original 13 locations

⚠️ **Important:** All changes are **in-memory only** and lost on app restart.

---

## 🧱 Architecture Overview

### Data Representation

```python
# Weighted adjacency list (bidirectional graph)
road_network: Dict[str, Dict[str, int]]

# Example:
{
    'Railway Station': {
        'Bus Stand': 4,      # 4 minutes travel time
        'Patram Nagar': 3,
        'K M College': 5
    },
    'Bus Stand': {
        'Railway Station': 4,  # Bidirectional
        'Nehru Park': 4
    }
}
```

All weight updates maintain **bidirectional symmetry** automatically.

### Current Network

**Location:** Narwana, Haryana (Jind District)  
**GPS Center:** 29.5960°N, 76.1150°E  
**Network Size:** 13 locations, 29 bidirectional roads  
**Travel Times:** 2-6 minutes between connected locations

**Locations by Category:**

| Category | Locations |
|----------|-----------|
| 🚉 **Transportation** | Railway Station, Bus Stand |
| 🎓 **Education** | Arya Senior Secondary School, S.D. Model School, K M College, S D Kanya Mahavidhlya |
| 🏥 **Healthcare** | Mittal Eye Hospital |
| 🏘️ **Residential** | Patram Nagar, Kishan Chand Colony, Model Town, Birbal Nagar, Arya Up Nagar |
| 🌳 **Public Spaces** | Nehru Park |

### Core Functions

| File | Function | Responsibility |
|------|----------|----------------|
| `data_loader.py` | `get_road_network()` | Returns baseline graph (13 locations, 29 connections) |
| `data_loader.py` | `get_locations()` | Returns sorted list of all locations |
| `data_loader.py` | `get_edge_list()` | Returns deduplicated edge tuples |
| `data_loader.py` | `update_traffic_weight()` | Mutates weight in both directions (A→B and B→A) |
| `utils.py` | `dijkstra_shortest_path()` | Shortest path core algorithm |
| `utils.py` | `get_path_edges()` | Converts node path to edge list for highlighting |
| `utils.py` | `format_path_display()` | Formats path for UI display with arrows |
| `app.py` | `get_geographic_layout()` | Converts GPS coords to graph positions |
| `app.py` | `create_network_graph()` | Visualization with theming, layouts & effects |

### Algorithm: Dijkstra's Shortest Path

**Implementation:** Custom heapq-based priority queue (not NetworkX)

**Time Complexity:** O((V + E) log V)  
- V = vertices (locations)
- E = edges (roads)
- log V from heap operations

**Key Optimizations:**
1. **Early termination** - Stops when destination is reached
2. **Visited set** - Prevents reprocessing nodes
3. **Heap-based relaxation** - Efficient priority queue operations
4. **Path reconstruction** - Predecessors dictionary for backtracking

**Algorithm Steps:**
1. Initialize distances to ∞ for all nodes except start (0)
2. Use min-heap priority queue: (distance, node)
3. Pop minimum distance node
4. Update neighbor distances via edge relaxation
5. Track predecessors for path reconstruction
6. Return path and total weight

---

## 🎨 Visualization Enhancements

### Geographic Layout (Default)

**Real-world GPS positioning:**
- Uses actual latitude/longitude coordinates from `NARWANA_COORDINATES`
- **Adaptive scaling:** `scale = 400 / lat_range` ensures proper fit
- Coordinate transformation: `x = (lon - lon_center) * scale`, `y = (lat - lat_center) * scale`
- Cardinal directions match real map (North at top)

**Verification:**
- North: S.D. Model School (29.6025°N)
- South: K M College (29.5950°N)
- East: S D Kanya Mahavidhlya (76.1182°E)
- West: Patram Nagar (76.1118°E)

### Visual Effects

- **Gradient edge colors** - Blues colormap scaled by normalized weights
- **Edge width scaling** - Width proportional to travel time (min 1, max 5)
- **Path highlighting** - Two-layer glow effect:
  1. Background layer (wider, semi-transparent yellow)
  2. Foreground layer (narrower, solid red)
- **Node styling** - Size 700, dodgerblue color, black edge
- **Label customization** - Adjustable font size (6-20pt slider)

---

## 🛠 Configuration & Customization

| Area | How to Change |
|------|---------------|
| **Base theme** | Edit `.streamlit/config.toml` |
| **Progress delays** | Modify `time.sleep()` calls in app.py compute section |
| **Default network** | Update `get_road_network()` in data_loader.py |
| **GPS coordinates** | Modify `NARWANA_COORDINATES` dict in app.py |
| **Node label size** | Adjust slider default in Display Settings section |
| **Edge styling** | Edit `create_network_graph()` function parameters |
| **Title size** | Change h1 font-size in CSS (currently 3.2rem) |

---

## 🗺 Roadmap

**Planned Features:**
- [ ] Layout position caching to avoid recomputation
- [ ] Export capabilities (PNG/SVG graphs, JSON routes)
- [ ] Abbreviated label mode for dense graphs
- [ ] Alternative routes (Yen's K-shortest paths algorithm)
- [ ] Colorblind-friendly palette toggle
- [ ] Time-based traffic patterns (rush hour simulation)
- [ ] Undo/redo stack for editor actions
- [ ] Data persistence (save custom networks)
- [ ] A* algorithm option (heuristic pathfinding)
- [ ] Mobile-responsive layout

---

## 📦 Dependencies

**Production Dependencies** (from `requirements.txt`):
```
streamlit>=1.32,<2.0      # Web application framework
networkx>=3.2,<4.0        # Graph visualization (NOT pathfinding)
matplotlib>=3.8,<3.9      # Plotting library
scipy>=1.10,<2.0          # Scientific computing (Kamada-Kawai layout)
requests>=2.31,<3.0       # HTTP library (future API integration)
```

**Python Version:** 3.10+ (tested on 3.12)

**Note:** NetworkX is used **only for visualization**, not for pathfinding. Dijkstra's algorithm is implemented from scratch in `utils.py` using Python's heapq module.

---

## 🤝 Contributing

Pull requests are welcome! Please follow these guidelines:

1. **Code Quality:**
   - Keep functions small and focused (single responsibility)
   - Use type hints for function signatures
   - Follow PEP 8 style guidelines

2. **Testing:**
   - Add/update tests for behavior changes
   - Verify geographic layout with `verify_layout.py`
   - Test network modifications thoroughly

3. **Documentation:**
   - Update README for user-visible changes
   - Add docstrings to new functions
   - Comment complex logic

4. **Commit Messages:**
   - Use clear, descriptive messages
   - Reference issues/PRs where applicable

---

## 📄 License & Attribution

**License:** Educational / Personal Use Only  
**Attribution:** Please credit "UrbanFlow – Ayush Mittal" in derivatives

This project is intended for learning purposes and portfolio demonstration.

---

## 🙋 Support & Contact

**Issues:** Open a GitHub issue for bugs or feature requests

**Contact:**
- 🐙 GitHub: [@ayushmittal62](https://github.com/ayushmittal62)
- 💼 LinkedIn: [Ayush Mittal](https://www.linkedin.com/in/ayush-mittal629/)

---

<div align="center">

Made with ❤️ using **Streamlit**, **NetworkX** & **Matplotlib**

© 2025 UrbanFlow · Created by **Ayush Mittal**

</div>
