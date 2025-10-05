"""Main Streamlit application for the Traffic Congestion Predictor.
Provides UI for route selection, prediction, visualization and traffic editing."""

from __future__ import annotations

import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime
from typing import List, Tuple, Optional

from data_loader import (
    get_road_network,
    get_locations,
    get_edge_list,
    update_traffic_weight,
)
from utils import dijkstra_shortest_path, get_path_edges
import time


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="UrbanFlow",
    page_icon="🌐",
    layout="wide",
)

# Global style tweaks (slightly smaller base font)
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-size: 0.9rem !important;
    }
    h1 { font-size: 2.05rem !important; font-weight:600; }
    h2 { font-size: 1.45rem !important; }
    h3 { font-size: 1.15rem !important; }
    section.main > div { padding-top: 1rem; }
    .stButton button { border-radius:6px !important; font-weight:600; }
    .stButton button:hover { filter:brightness(1.05); }
    .stMetric label { font-size: 0.65rem !important; letter-spacing:.5px; }
    .stMetric [data-testid="stMetricValue"] { font-size: 1.05rem !important; }
    .route-box { background:#1E293B; border:1px solid #475569; padding:1rem 1.1rem; border-radius:10px; box-shadow:0 4px 10px -2px rgba(0,0,0,0.45), 0 0 0 1px #334155 inset; }
    .route-path { font-size:.95rem; line-height:1.4; letter-spacing:.5px; color:#E2E8F0; word-break:break-word; }
    .route-time { font-size:1.25rem; font-weight:600; color:#38bdf8; display:inline-block; margin:.25rem 0 .5rem 0; }
    .small-note { font-size:.75rem; color:#94a3b8; text-transform:uppercase; letter-spacing:1px; }
    @media (min-width:1200px){ .route-path { font-size:1rem; } .route-time { font-size:1.35rem; } }
    .step-badge {display:inline-block; background:#1E88E5; color:#fff; padding:2px 8px; border-radius:12px; font-size:.65rem; margin-right:6px; letter-spacing:.5px; }
    .sidebar .stButton button { background:#1E88E520 !important; }
    .legend-box { background:#1E293B; padding:.6rem .75rem; border-radius:6px; border:1px solid #334155; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------------------------
def initialize_session_state() -> None:
    if "road_network" not in st.session_state:
        st.session_state.road_network = get_road_network()
    if "route_history" not in st.session_state:
        st.session_state.route_history = []  # type: ignore[assignment]
    if "show_traffic_editor" not in st.session_state:
        st.session_state.show_traffic_editor = False
    if "network_modified" not in st.session_state:
        st.session_state.network_modified = False
    if "current_path" not in st.session_state:
        st.session_state.current_path = None  # type: ignore[assignment]
    if "current_weight" not in st.session_state:
        st.session_state.current_weight = None  # type: ignore[assignment]
    if "path_edges" not in st.session_state:
        st.session_state.path_edges = None  # type: ignore[assignment]
    if "total_queries" not in st.session_state:
        st.session_state.total_queries = 0


# ---------------------------------------------------------------------------
# Graph Creation & Visualization
# ---------------------------------------------------------------------------
def create_network_graph(
    road_network: dict,
    highlight_edges: Optional[List[Tuple[str, str]]] = None,
    layout: str = "spring",
    color_edges: bool = True,
    show_edge_labels: bool = True,
    scale_widths: bool = True,
    label_font_size: int = 8,
) -> plt.Figure:
    """Create an enhanced NetworkX graph figure.

    Parameters:
        road_network: adjacency mapping
        highlight_edges: edges belonging to the active shortest path
        layout: one of 'spring', 'kamada', 'circular', 'shell'
        color_edges: apply gradient color map based on weight
        show_edge_labels: toggle drawing of edge weight labels
        scale_widths: scale edge widths proportionally to weight
    """
    G = nx.Graph()

    # Add nodes & edges (deduplicated)
    added = set()
    for src, neighbors in road_network.items():
        for dst, weight in neighbors.items():
            if (dst, src) in added:
                continue
            G.add_edge(src, dst, weight=weight)
            added.add((src, dst))

    if layout == "kamada":
        pos = nx.kamada_kawai_layout(G)
    elif layout == "circular":
        pos = nx.circular_layout(G)
    elif layout == "shell":
        pos = nx.shell_layout(G)
    else:
        pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("City Traffic Network", fontsize=14, pad=12)
    ax.axis("off")

    # Edge weights for styling
    weights = [d["weight"] for _, _, d in G.edges(data=True)]
    min_w, max_w = (min(weights), max(weights)) if weights else (1, 1)

    def width_for(w: float) -> float:
        if not scale_widths or max_w == min_w:
            return 1.6
        # normalize 0..1 then scale
        norm = (w - min_w) / (max_w - min_w)
        return 1.0 + norm * 3.0

    widths = [width_for(d["weight"]) for _, _, d in G.edges(data=True)]

    if color_edges and weights:
        # Map weights to a blue gradient (lighter = shorter / faster)
        import matplotlib as mpl
        cmap = mpl.cm.get_cmap("Blues")
        norm = mpl.colors.Normalize(vmin=min_w, vmax=max_w)
        colors = [cmap(norm(w)) for w in weights]
    else:
        colors = ["#64748b"] * len(weights)

    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax,
        edge_color=colors,
        width=widths,
        alpha=0.85,
        edge_cmap=None,
    )

    # Highlighted path edges
    if highlight_edges:
        # Glow effect: draw thicker transparent layer beneath
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=highlight_edges,
            ax=ax,
            edge_color="#1E3A8A",
            width=8.0,
            alpha=0.25,
        )
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=highlight_edges,
            ax=ax,
            edge_color="#3B82F6",
            width=4.0,
            alpha=0.95,
        )

    # Nodes & labels
    nx.draw_networkx_nodes(G, pos, node_size=880, node_color="#2196F3", edgecolors="#ffffff", linewidths=1.4)
    nx.draw_networkx_labels(G, pos, font_size=label_font_size, font_weight="bold")

    # Edge weight labels (optional)
    if show_edge_labels:
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            font_color="#94a3b8",
            font_size=8,
            label_pos=0.5,
        )
    return fig


# ---------------------------------------------------------------------------
# Route History Management
# ---------------------------------------------------------------------------
def add_route_to_history(path: List[str], weight: float, source: str, destination: str) -> None:
    st.session_state.route_history.append(
        {
            "source": source,
            "destination": destination,
            "path": path,
            "weight": weight,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


# ---------------------------------------------------------------------------
# Sidebar (Hamburger) Menu
# ---------------------------------------------------------------------------
def create_sidebar() -> None:
    with st.sidebar:
        st.title("☰ Menu")

        # Metrics
        st.metric("Total Routes", len(st.session_state.route_history))
        st.metric("Traffic Modified", "Yes" if st.session_state.network_modified else "No")
        st.metric("Queries Run", st.session_state.total_queries)

        st.divider()
        st.subheader("Session Controls")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Restore Traffic", use_container_width=True):
                st.session_state.road_network = get_road_network()
                st.session_state.network_modified = False
                st.success("Traffic reset.")
                st.rerun()
        with col_b:
            if st.button("Clear History", use_container_width=True):
                st.session_state.route_history = []
                st.success("History cleared.")

        if st.button("Full Session Reset", type="primary", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.success("Fresh session started.")
            st.rerun()

        st.divider()
        st.subheader("Recent Routes")
        if st.session_state.route_history:
            for idx, record in enumerate(reversed(st.session_state.route_history[-8:]), 1):
                with st.expander(f"{idx}. {record['source']} → {record['destination']}"):
                    st.caption(" → ".join(record["path"]))
                    st.caption(f"Time: {record['weight']:.1f} min · {record['timestamp']}")
        else:
            st.info("No routes yet.")

        st.divider()
        st.subheader("Network Stats")
        edges = get_edge_list(st.session_state.road_network)
        locations = sorted(list(st.session_state.road_network.keys()))
        total_weight = sum(w for _, _, w in edges)
        avg_weight = total_weight / len(edges) if edges else 0
        st.metric("Locations", len(locations))
        st.metric("Roads", len(edges))
        st.metric("Avg Weight", f"{avg_weight:.1f}")
        if edges:
            fast = min(edges, key=lambda e: e[2])
            slow = max(edges, key=lambda e: e[2])
            st.caption(f"Fastest: {fast[0]} ↔ {fast[1]} ({fast[2]})")
            st.caption(f"Slowest: {slow[0]} ↔ {slow[1]} ({slow[2]})")

        st.divider()
        with st.expander("About", expanded=False):
            st.markdown(
                """
                **UrbanFlow**  
                Adaptive route intelligence for dynamic city networks.  
                Powered by Dijkstra's Algorithm.  
                
                Made by **Ayush Mittal ❤️**
                
                [GitHub](https://github.com/ayushmittal62) · [LinkedIn](https://www.linkedin.com/in/ayush-mittal629/)
                """
            )


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------
def main() -> None:
    initialize_session_state()
    create_sidebar()

    st.title("🚦 UrbanFlow")
    st.markdown(
        """A simple, clear tool to plan the fastest route between two locations.
        Adjust traffic weights to simulate congestion and re‑evaluate paths."""
    )
    st.divider()

    col1, col2 = st.columns([1, 2])

    # ------------------------- Left Column: Controls ----------------------
    with col1:
        st.subheader("🧭 Route Planner")
        st.caption("Select any two distinct locations.")
        # Dynamic locations reflect newly added nodes during the session
        locations = sorted(list(st.session_state.road_network.keys()))
        source = st.selectbox("Source", locations, index=0)
        destination = st.selectbox("Destination", locations, index=min(5, len(locations) - 1))

        compute = st.button("⚡ Step 1 · Compute Fastest Route", use_container_width=True, type="primary")
        if compute:
            if source == destination:
                st.warning("Select two different locations.")
            else:
                progress = st.progress(0, text="Initializing route engine...")
                time.sleep(0.15)
                progress.progress(20, text="Building graph structures...")
                time.sleep(0.15)
                progress.progress(45, text="Scanning edges & weights...")
                time.sleep(0.15)
                progress.progress(65, text="Exploring candidate paths...")
                # Actual compute
                path, weight = dijkstra_shortest_path(st.session_state.road_network, source, destination)
                progress.progress(85, text="Finalizing shortest path...")
                time.sleep(0.12)
                progress.progress(100, text="Route ready ✅")
                time.sleep(0.08)
                progress.empty()
                st.session_state.current_path = path
                st.session_state.current_weight = weight
                st.session_state.path_edges = get_path_edges(path) if path else None
                st.session_state.total_queries += 1
                if path:
                    add_route_to_history(path, weight, source, destination)

        if st.session_state.current_path is not None:
            st.subheader("🎯 Step 2 · Route Result")
            if st.session_state.current_path:
                path_str = " → ".join(st.session_state.current_path)
                stops = len(st.session_state.current_path) - 1
                html = (
                    "<div class='route-box'>"
                    "<div class='route-time'>" 
                    f"{st.session_state.current_weight:.1f} min" 
                    "</div>"
                    "<div class='route-path'><strong>Path:</strong><br>"
                    f"{path_str}" 
                    "</div>"
                    f"<div class='small-note'>Stops: {stops}</div>"
                    "</div>"
                )
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.error("No route available between these points.")
    with col2:
        st.subheader("🌐 Network Visualizer")
        with st.expander("Display Settings", expanded=False):
            layout = st.selectbox(
                "Layout", ["spring", "kamada", "circular", "shell"], index=0, help="Graph layout algorithm"
            )
            c1, c2, c3 = st.columns(3)
            with c1:
                color_edges = st.checkbox("Edge colors", value=True, help="Color edges by weight")
            with c2:
                show_labels = st.checkbox("Weights", value=True, help="Show edge weights")
            with c3:
                scale_widths = st.checkbox("Width scale", value=True, help="Scale edge width by weight")
            label_font_size = st.slider("Node label size", min_value=6, max_value=14, value=8, step=1, help="Adjust node name text size")

        # Graph buffering for layout changes
        graph_buffer_key = f"graph_buffer_{layout}_{color_edges}_{show_labels}_{scale_widths}"
        with st.spinner("Rendering network..."):
            fig = create_network_graph(
                st.session_state.road_network,
                st.session_state.path_edges if st.session_state.current_path else None,
                layout=layout,
                color_edges=color_edges,
                show_edge_labels=show_labels,
                scale_widths=scale_widths,
                label_font_size=label_font_size,
            )
        st.pyplot(fig)
        plt.close(fig)

        st.markdown(
            """<div class='legend-box'><strong>Legend</strong><br>
            🔵 Node = Location<br>
            🔷 Glowing line = Fastest path<br>
            🎨 Edge tone = Relative travel time (if enabled)<br>
            ↕ Thickness = Weight magnitude (if enabled)</div>""",
            unsafe_allow_html=True,
        )

        # ------------------- Traffic / Network Editor Toggle -----------------
        toggle_label = (
            "🛠 Show Traffic & Network Editor" if not st.session_state.show_traffic_editor else "⬅ Hide Traffic & Network Editor"
        )
        if st.button(toggle_label, use_container_width=True):
            st.session_state.show_traffic_editor = not st.session_state.show_traffic_editor
            st.rerun()

        # ------------------- Traffic Editor & Network Structure --------------
        if st.session_state.show_traffic_editor:
            st.divider()
            st.subheader("🧪 Traffic Lab")
            st.caption("Adjust weights or modify the network structure. Higher weight = slower travel time.")

            # Weight Adjustments
            with st.expander("Adjust Existing Road Weights", expanded=True):
                edges = get_edge_list(st.session_state.road_network)
                if not edges:
                    st.info("No roads available. Add new roads below.")
                else:
                    cols = st.columns(3)
                    for idx, (a, b, w) in enumerate(edges):
                        with cols[idx % 3]:
                            current = st.session_state.road_network.get(a, {}).get(b, w)
                            new_w = st.number_input(
                                f"{a} ↔ {b}",
                                min_value=1,
                                max_value=100,
                                value=int(current),
                                step=1,
                                key=f"edge_{a}_{b}",
                            )
                            if new_w != current:
                                st.session_state.road_network = update_traffic_weight(
                                    st.session_state.road_network, a, b, new_w
                                )
                                st.session_state.network_modified = True

                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Restore Default Weights", use_container_width=True):
                        st.session_state.road_network = get_road_network()
                        st.session_state.network_modified = False
                        st.success("Weights restored.")
                        st.rerun()
                with c2:
                    if st.button("Clear All Routes (Danger)", use_container_width=True):
                        # Clear all edges but keep nodes
                        for n in list(st.session_state.road_network.keys()):
                            st.session_state.road_network[n] = {}
                        st.session_state.network_modified = True
                        st.warning("All road weights cleared. Now an empty graph of nodes.")

            # Network Structure Editor
            with st.expander("Network Structure Editor", expanded=False):
                st.caption("Add/remove locations and roads. Use responsibly – this changes the active graph.")
                nodes = sorted(list(st.session_state.road_network.keys()))

                # Add Node
                st.markdown("**Add New Location**")
                new_node = st.text_input("Location name", key="add_node_name")
                add_node_btn = st.button("➕ Add Location", key="add_node_btn")
                if add_node_btn:
                    nn = new_node.strip()
                    if not nn:
                        st.warning("Enter a location name first.")
                    elif nn in st.session_state.road_network:
                        st.info("Location already exists.")
                    else:
                        st.session_state.road_network[nn] = {}
                        st.session_state.network_modified = True
                        st.success(f"Location '{nn}' added.")
                        st.rerun()

                st.markdown("---")
                st.markdown("**Add / Update Road**")
                if len(nodes) >= 2:
                    colA, colB, colW = st.columns([1, 1, 1])
                    with colA:
                        road_a = st.selectbox("From", nodes, key="road_from")
                    with colB:
                        road_b = st.selectbox("To", nodes, key="road_to")
                    with colW:
                        road_w = st.number_input("Weight", min_value=1, max_value=100, value=5, key="road_weight")
                    add_edge_btn = st.button("🔗 Add / Update Road", key="add_edge_btn")
                    if add_edge_btn:
                        if road_a == road_b:
                            st.warning("Choose two distinct locations.")
                        else:
                            # Ensure adjacency entries exist
                            st.session_state.road_network.setdefault(road_a, {})[road_b] = int(road_w)
                            st.session_state.road_network.setdefault(road_b, {})[road_a] = int(road_w)
                            st.session_state.network_modified = True
                            st.success(f"Road {road_a} ↔ {road_b} set to {road_w}.")
                            st.rerun()
                else:
                    st.info("Add at least 2 locations to create a road.")

                st.markdown("---")
                st.markdown("**Remove Road**")
                current_edges = get_edge_list(st.session_state.road_network)
                if current_edges:
                    edge_labels = [f"{a} ↔ {b} ({w})" for a, b, w in current_edges]
                    edge_choice = st.selectbox("Select road", edge_labels, key="remove_edge_select")
                    if st.button("❌ Remove Selected Road", key="remove_edge_btn"):
                        # Parse selection
                        idx = edge_labels.index(edge_choice)
                        a, b, w = current_edges[idx]
                        # Remove both directions if present
                        if b in st.session_state.road_network.get(a, {}):
                            del st.session_state.road_network[a][b]
                        if a in st.session_state.road_network.get(b, {}):
                            del st.session_state.road_network[b][a]
                        st.session_state.network_modified = True
                        st.warning(f"Removed road {a} ↔ {b}.")
                        st.rerun()
                else:
                    st.info("No roads to remove.")

                st.markdown("---")
                st.markdown("**Remove Location**")
                if nodes:
                    node_to_remove = st.selectbox("Location", nodes, key="remove_node_select")
                    if st.button("🗑 Remove Location", key="remove_node_btn"):
                        # Delete node and any references
                        if node_to_remove in st.session_state.road_network:
                            del st.session_state.road_network[node_to_remove]
                        for n in list(st.session_state.road_network.keys()):
                            st.session_state.road_network[n].pop(node_to_remove, None)
                        st.session_state.network_modified = True
                        st.warning(f"Location '{node_to_remove}' removed.")
                        st.rerun()
                else:
                    st.info("No locations present.")

    # ------------------------- Footer -------------------------------------
    st.divider()
    st.markdown(
        """
        <div style='text-align:center; color:#7f8c8d; padding:16px 0;'>
            <p style='margin:4px 0;'>🌐 UrbanFlow</p>
            <p style='margin:4px 0; font-size:12px;'>Adaptive route intelligence for dynamic city networks · Made by <strong>Ayush Mittal ❤️</strong></p>
            <p style='margin:4px 0; font-size:12px;'>
                <a href='https://github.com/ayushmittal62' target='_blank'>GitHub</a> ·
                <a href='https://www.linkedin.com/in/ayush-mittal629/' target='_blank'>LinkedIn</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":  # pragma: no cover
    main()