from shiny import App, ui, render, reactive
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import plotly.graph_objects as go

# Load data
customer_data = pd.read_csv("Data/Data Output/customer_data.csv")
device_data = pd.read_csv("Data/Data Output/device_data.csv")

# Convert last_alive_date to datetime
device_data['last_alive_date'] = pd.to_datetime(device_data['last_alive_date'])

# Define active threshold (30 days)
ACTIVE_THRESHOLD_DAYS = 30

# Calculate active status
current_date = datetime.now()
device_data['is_active'] = (current_date - device_data['last_alive_date']).dt.days < ACTIVE_THRESHOLD_DAYS

# Categorize ISP
device_data['is_frontier'] = device_data['isp'] == 'Frontier Communications'

# App UI
app_ui = ui.page_fluid(
    ui.panel_title("Device Analytics Dashboard"),
    ui.navset_tab(
        ui.nav_panel(
            "Device Overview",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.h3("Filters"),
                    ui.input_slider(
                        "active_days",
                        "Active threshold (days):",
                        min=7,
                        max=90,
                        value=30,
                        step=1
                    ),
                    ui.hr(),
                    ui.h4("Summary"),
                    ui.output_ui("summary_stats")
                ),
                ui.card(
                    ui.card_header("Device Breakdown by ISP and Status"),
                    ui.output_ui("device_tree"),
                    full_screen=True
                ),
                ui.row(
                    ui.column(
                        6,
                        ui.card(
                            ui.card_header("Frontier Devices Distribution"),
                            ui.output_plot("frontier_chart")
                        )
                    ),
                    ui.column(
                        6,
                        ui.card(
                            ui.card_header("Non-Frontier Devices Distribution"),
                            ui.output_plot("non_frontier_chart")
                        )
                    )
                )
            )
        ),
        ui.nav_panel(
            "Customer Analysis",
            ui.card(
                ui.card_header("Customer Analysis"),
                ui.p("Customer analysis features will be added here...")
            )
        ),
        ui.nav_panel(
            "Device Details",
            ui.card(
                ui.card_header("Device Details"),
                ui.p("Device details and additional metrics will be added here...")
            )
        )
    )
)


def server(input, output, session):
    
    @reactive.Calc
    def filtered_device_data():
        """Recalculate active status based on slider input"""
        df = device_data.copy()
        current_date = datetime.now()
        df['is_active'] = (current_date - df['last_alive_date']).dt.days < input.active_days()
        return df
    
    @reactive.Calc
    def device_stats():
        """Calculate device statistics"""
        df = filtered_device_data()
        
        total_devices = len(df)
        
        # Frontier devices
        frontier_df = df[df['is_frontier']]
        frontier_total = len(frontier_df)
        frontier_active = len(frontier_df[frontier_df['is_active']])
        frontier_inactive = frontier_total - frontier_active
        
        # Non-Frontier devices
        non_frontier_df = df[~df['is_frontier']]
        non_frontier_total = len(non_frontier_df)
        non_frontier_active = len(non_frontier_df[non_frontier_df['is_active']])
        non_frontier_inactive = non_frontier_total - non_frontier_active
        
        return {
            'total': total_devices,
            'frontier': {
                'total': frontier_total,
                'active': frontier_active,
                'inactive': frontier_inactive
            },
            'non_frontier': {
                'total': non_frontier_total,
                'active': non_frontier_active,
                'inactive': non_frontier_inactive
            }
        }
    
    @output
    @render.ui
    def summary_stats():
        """Display summary statistics in sidebar"""
        stats = device_stats()
        
        return ui.div(
            ui.tags.table(
                ui.tags.tr(
                    ui.tags.td(ui.strong("Total Devices:")),
                    ui.tags.td(f"{stats['total']:,}", style="text-align: right; padding-left: 10px;")
                ),
                ui.tags.tr(
                    ui.tags.td(ui.strong("Frontier (Active):")),
                    ui.tags.td(
                        f"{stats['frontier']['active']:,}", 
                        style="text-align: right; padding-left: 10px; color: #28a745; font-weight: bold;"
                    )
                ),
                ui.tags.tr(
                    ui.tags.td("  Frontier Total:"),
                    ui.tags.td(f"{stats['frontier']['total']:,}", style="text-align: right; padding-left: 10px;")
                ),
                ui.tags.tr(
                    ui.tags.td("  Frontier Inactive:"),
                    ui.tags.td(f"{stats['frontier']['inactive']:,}", style="text-align: right; padding-left: 10px;")
                ),
                ui.tags.tr(ui.tags.td(ui.hr(), colspan="2")),
                ui.tags.tr(
                    ui.tags.td("Non-Frontier Total:"),
                    ui.tags.td(f"{stats['non_frontier']['total']:,}", style="text-align: right; padding-left: 10px;")
                ),
                ui.tags.tr(
                    ui.tags.td("  Non-Frontier Active:"),
                    ui.tags.td(f"{stats['non_frontier']['active']:,}", style="text-align: right; padding-left: 10px;")
                ),
                ui.tags.tr(
                    ui.tags.td("  Non-Frontier Inactive:"),
                    ui.tags.td(f"{stats['non_frontier']['inactive']:,}", style="text-align: right; padding-left: 10px;")
                ),
                style="width: 100%;"
            )
        )
    
    @output
    @render.ui
    def device_tree():
        """Display hierarchical device breakdown"""
        stats = device_stats()
        
        # Calculate percentages
        frontier_pct = (stats['frontier']['total'] / stats['total'] * 100) if stats['total'] > 0 else 0
        non_frontier_pct = (stats['non_frontier']['total'] / stats['total'] * 100) if stats['total'] > 0 else 0
        
        frontier_active_pct = (stats['frontier']['active'] / stats['frontier']['total'] * 100) if stats['frontier']['total'] > 0 else 0
        frontier_inactive_pct = (stats['frontier']['inactive'] / stats['frontier']['total'] * 100) if stats['frontier']['total'] > 0 else 0
        
        non_frontier_active_pct = (stats['non_frontier']['active'] / stats['non_frontier']['total'] * 100) if stats['non_frontier']['total'] > 0 else 0
        non_frontier_inactive_pct = (stats['non_frontier']['inactive'] / stats['non_frontier']['total'] * 100) if stats['non_frontier']['total'] > 0 else 0
        
        return ui.div(
            ui.tags.style("""
                .tree-container {
                    font-family: 'Courier New', monospace;
                    padding: 20px;
                    background-color: #f8f9fa;
                    border-radius: 5px;
                }
                .tree-level-0 {
                    font-size: 24px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 20px;
                }
                .tree-level-1 {
                    font-size: 18px;
                    font-weight: bold;
                    margin-left: 30px;
                    margin-top: 15px;
                    margin-bottom: 10px;
                }
                .tree-level-2 {
                    font-size: 16px;
                    margin-left: 60px;
                    margin-top: 8px;
                }
                .frontier {
                    color: #0066cc;
                }
                .non-frontier {
                    color: #6c757d;
                }
                .active {
                    color: #28a745;
                    font-weight: bold;
                }
                .inactive {
                    color: #dc3545;
                }
                .target-highlight {
                    background-color: #d4edda;
                    padding: 5px 10px;
                    border-radius: 3px;
                    border-left: 4px solid #28a745;
                }
            """),
            ui.div(
                ui.div(
                    f"📊 Total Devices: {stats['total']:,}",
                    class_="tree-level-0"
                ),
                
                # Frontier Branch
                ui.div(
                    f"├─ 🏢 Frontier Communications: {stats['frontier']['total']:,} ({frontier_pct:.1f}%)",
                    class_="tree-level-1 frontier"
                ),
                ui.div(
                    f"│  ├─ ✅ Active: {stats['frontier']['active']:,} ({frontier_active_pct:.1f}%) 🎯 TARGET GROUP",
                    class_="tree-level-2 active target-highlight"
                ),
                ui.div(
                    f"│  └─ ❌ Inactive: {stats['frontier']['inactive']:,} ({frontier_inactive_pct:.1f}%)",
                    class_="tree-level-2 inactive"
                ),
                
                # Non-Frontier Branch
                ui.div(
                    f"└─ 🌐 Non-Frontier ISPs: {stats['non_frontier']['total']:,} ({non_frontier_pct:.1f}%)",
                    class_="tree-level-1 non-frontier"
                ),
                ui.div(
                    f"   ├─ ✅ Active: {stats['non_frontier']['active']:,} ({non_frontier_active_pct:.1f}%)",
                    class_="tree-level-2"
                ),
                ui.div(
                    f"   └─ ❌ Inactive: {stats['non_frontier']['inactive']:,} ({non_frontier_inactive_pct:.1f}%)",
                    class_="tree-level-2"
                ),
                
                class_="tree-container"
            )
        )
    
    @output
    @render.plot
    def frontier_chart():
        """Pie chart for Frontier devices"""
        import matplotlib.pyplot as plt
        
        stats = device_stats()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        if stats['frontier']['total'] > 0:
            sizes = [stats['frontier']['active'], stats['frontier']['inactive']]
            labels = [f"Active\n{stats['frontier']['active']:,}", f"Inactive\n{stats['frontier']['inactive']:,}"]
            colors = ['#28a745', '#dc3545']
            explode = (0.1, 0)  # Explode active slice
            
            ax.pie(sizes, labels=labels, colors=colors, explode=explode, autopct='%1.1f%%',
                   shadow=True, startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
            ax.set_title(f"Frontier Devices\n(Total: {stats['frontier']['total']:,})", fontsize=14, weight='bold')
        else:
            ax.text(0.5, 0.5, 'No Frontier Devices', ha='center', va='center', fontsize=14)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        
        return fig
    
    @output
    @render.plot
    def non_frontier_chart():
        """Pie chart for Non-Frontier devices"""
        import matplotlib.pyplot as plt
        
        stats = device_stats()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        if stats['non_frontier']['total'] > 0:
            sizes = [stats['non_frontier']['active'], stats['non_frontier']['inactive']]
            labels = [f"Active\n{stats['non_frontier']['active']:,}", f"Inactive\n{stats['non_frontier']['inactive']:,}"]
            colors = ['#17a2b8', '#6c757d']
            
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                   shadow=True, startangle=90, textprops={'fontsize': 12})
            ax.set_title(f"Non-Frontier Devices\n(Total: {stats['non_frontier']['total']:,})", fontsize=14, weight='bold')
        else:
            ax.text(0.5, 0.5, 'No Non-Frontier Devices', ha='center', va='center', fontsize=14)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        
        return fig


app = App(app_ui, server)

