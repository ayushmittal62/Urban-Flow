<div align="center">

# 🚦 UrbanFlow
**Adaptive route intelligence for dynamic city networks**

Interactive shortest-path routing + live traffic simulation + editable city graph.

![Status](https://img.shields.io/badge/status-active-brightgreen) ![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B) ![License](https://img.shields.io/badge/license-Educational-blue)

</div>

---

## ✨ Key Features

| Area | Capability |
|------|------------|
| Route Planning | Fastest path between any two locations using Dijkstra |
| Dynamic Network | Add / remove locations and roads at runtime |
| Traffic Simulation | Adjust bidirectional edge weights (travel time) live |
| Visualization | Multiple layouts (spring, Kamada-Kawai, circular, shell) |
| Styling Controls | Toggle edge colors, weight labels, width scaling, label size |
| Path Highlighting | Glowing layered emphasis of active shortest path |
| Progress Feedback | Simulated staged buffering during route computation |
| Metrics & History | Route history, network stats, modification status |
| Dark Theming | Custom dark UI with compact typography |

---

## 🗂 Project Structure
```
app.py                    # Streamlit UI + visualization + editors
data_loader.py            # Base road network & helpers
utils.py                  # Dijkstra + path utilities
requirements.txt          # Python dependencies
README.md                 # Documentation (this file)
```

---

## 🚀 Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```
Open: http://localhost:8501

Python 3.10+ recommended (tested on 3.12).

---

## 🧭 Using UrbanFlow

1. Open the app – the default network loads into session state.
2. Choose a Source and Destination in the Route Planner.
3. Click “⚡ Step 1 · Compute Fastest Route” → a staged progress bar (buffering) shows internal steps.
4. View the styled result card (time + path + stop count).
5. Expand “Display Settings” to adjust visualization (layout, colors, widths, labels, node label size).
6. Click “🛠 Show Traffic & Network Editor” to:
   - Change existing road weights
   - Add / remove locations (nodes)
   - Add / update / remove roads (edges)
   - Clear all roads (danger) or restore defaults
7. Re‑compute a route to see the impact instantly.

### Buffering / Progress Simulation
The staged progress bar is purely UX (not actual heavy compute):

| Stage | Message | Purpose |
|-------|---------|---------|
| 0–20% | Initializing route engine... | Session setup & validation |
| 20–45% | Building graph structures... | Conceptual graph prep |
| 45–65% | Scanning edges & weights... | Emphasize network traversal |
| 65–85% | Exploring candidate paths... | Path exploration feel |
| 85–100% | Finalizing shortest path... | Wrap-up & display |

Want it faster? Reduce or remove the internal `time.sleep()` delays inside the compute block of `app.py`.

### Dynamic Locations
The route planner now reflects any new nodes you add during the session (no restart required). Nodes and edges persist only in-memory—reset restores the original baseline network from `data_loader.get_road_network()`.

---

## 🧱 Architecture Overview

### Data Representation
```
road_network: Dict[str, Dict[str, int]]  # adjacency list
```
Bidirectional updates keep weights symmetric when edited.

### Core Functions
File | Function | Responsibility
-----|----------|--------------
`data_loader.py` | `get_road_network()` | Returns baseline graph
`data_loader.py` | `get_edge_list()` | Deduplicated edge tuples
`data_loader.py` | `update_traffic_weight()` | Mutates weight both directions
`utils.py` | `dijkstra_shortest_path()` | Shortest path core
`utils.py` | `get_path_edges()` | Edge list for highlighting
`app.py` | `create_network_graph()` | Visualization with theming & effects

### Algorithm (Dijkstra)
Complexity: O((V + E) log V) with a binary heap.
Optimizations: early destination break, visited set, heap-based relaxation.

---

## 🎨 Visualization Enhancements
- Gradient edge colors (Blues) scaled by weight
- Optional edge weight labels
- Edge width proportional to weight
- Multiple layout algorithms
- Highlight glow (two-layer edge drawing)
- Adjustable node label font size (slider)

---
## 🛠 Configuration & Customization
Area | How to Change
-----|---------------
Base theme | `.streamlit/config.toml`
Progress delays | Edit `time.sleep()` calls in compute section
Default graph | Modify `get_road_network()` in `data_loader.py`
Node label size default | Slider default in Display Settings
Edge styling rules | `create_network_graph()`

---

## 🗺 Roadmap
- [ ] Layout position caching per layout to avoid recompute
- [ ] Export graph (PNG / SVG) & route JSON
- [ ] Abbreviated label mode for dense graphs
- [ ] Alternative routes (Yen’s algorithm)
- [ ] Colorblind-friendly palette toggle
- [ ] Time-based traffic patterns (rush hours)
- [ ] Undo stack for editor actions

---

## 📦 Dependencies
See `requirements.txt`:
```
streamlit
networkx
matplotlib
```
Python 3.10+ recommended.

Optional (future): pandas, numpy, rich, pytest.

---

## 🤝 Contributing
Pull requests welcome. Please:
1. Keep functions small & typed.
2. Add / update tests for behavior changes.
3. Note UI/UX changes in the README if user-visible.

---

## 📄 License & Attribution
Educational / personal use. Credit “UrbanFlow – Ayush Mittal” in derivatives.

---

## 🙋 Support / Questions
Open an issue or reach out via:
- GitHub: https://github.com/ayushmittal62
- LinkedIn: https://www.linkedin.com/in/ayush-mittal629/

---

Made with ❤️ using Streamlit, NetworkX & Matplotlib.

© 2025 UrbanFlow · Created by Ayush Mittal
