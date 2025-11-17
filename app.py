from shiny import App, ui, render, reactive
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import plotly.graph_objects as go
import numpy as np

# Load data
customer_data = pd.read_csv("Data/Data Output/customer_data.csv")
device_data = pd.read_csv("Data/Data Output/device_data.csv")

# Merge customer and device data for Next Best Action analysis
merged_data = pd.merge(customer_data, device_data, on='customer_id', how='inner')

# Convert last_alive_date to datetime
device_data['last_alive_date'] = pd.to_datetime(device_data['last_alive_date'])

# Define active threshold (30 days)
ACTIVE_THRESHOLD_DAYS = 30

# Calculate active status
current_date = datetime.now()
device_data['is_active'] = (current_date - device_data['last_alive_date']).dt.days < ACTIVE_THRESHOLD_DAYS

# Categorize ISP
device_data['is_frontier'] = device_data['isp'] == 'Frontier Communications'

# Function to determine Next Best Action
def determine_next_best_action(row):
    """
    Apply business rules to determine the next best action for a customer.
    
    Rules:
    1. Speed upgrade, no device upgrade: Fiber customer, CLV 1-3, SQS = 3
    2. Speed Upgrade, new device upgrade: Fiber customer, CLV 7-10, segment is Aspirational Adopters or Peak Performers
    3. Keep As Is: SQS = 3, Churn = 0, segment is Budget Balancers, Foolproof Followers, or Settled Simplifiers
    4. Ship new device: SQS = 1, Churn = 1, segment = Aspirational Adopters
    """
    
    # Rule 4: Ship new device (highest priority for at-risk customers)
    if row['sqs_score'] == 1 and row['churn_risk'] == 1 and row['customer_segment'] == 'Aspirational Adopters':
        return 'Ship new device'
    
    # Rule 2: Speed Upgrade + new device upgrade
    if (row['broadband_type'] == 'Fiber' and 
        row['clv_decile'] >= 7 and row['clv_decile'] <= 10 and 
        row['customer_segment'] in ['Aspirational Adopters', 'Peak Performers']):
        return 'Speed upgrade + new device'
    
    # Rule 1: Speed upgrade, no device upgrade
    if (row['broadband_type'] == 'Fiber' and 
        row['clv_decile'] >= 1 and row['clv_decile'] <= 3 and 
        row['sqs_score'] == 3):
        return 'Speed upgrade only'
    
    # Rule 3: Keep As Is
    if (row['sqs_score'] == 3 and 
        row['churn_risk'] == 0 and 
        row['customer_segment'] in ['Budget Balancers', 'Foolproof Followers', 'Settled Simplifiers']):
        return 'Keep as is'
    
    # Default: No specific action
    return 'No action recommended'

# Apply the Next Best Action logic to merged data
merged_data['next_best_action'] = merged_data.apply(determine_next_best_action, axis=1)

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
        ),
        ui.nav_panel(
            "Next Best Action",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.h3("Filters"),
                    ui.input_select(
                        "action_filter",
                        "Filter by Action:",
                        choices={
                            "All": "All Actions",
                            "Ship new device": "Ship new device",
                            "Speed upgrade + new device": "Speed upgrade + new device",
                            "Speed upgrade only": "Speed upgrade only",
                            "Keep as is": "Keep as is",
                            "No action recommended": "No action recommended"
                        },
                        selected="All"
                    ),
                    ui.hr(),
                    ui.h4("Summary"),
                    ui.output_ui("nba_summary")
                ),
                ui.row(
                    ui.column(
                        12,
                        ui.card(
                            ui.card_header("Next Best Action Distribution"),
                            ui.output_plot("nba_distribution_chart"),
                            full_screen=True
                        )
                    )
                ),
                ui.row(
                    ui.column(
                        12,
                        ui.card(
                            ui.card_header("Customer Details"),
                            ui.output_data_frame("nba_table"),
                            full_screen=True
                        )
                    )
                )
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
    
    # Next Best Action Tab Functions
    @reactive.Calc
    def filtered_nba_data():
        """Filter NBA data based on action selection"""
        df = merged_data.copy()
        
        if input.action_filter() != "All":
            df = df[df['next_best_action'] == input.action_filter()]
        
        return df
    
    @reactive.Calc
    def nba_stats():
        """Calculate Next Best Action statistics"""
        df = merged_data.copy()
        
        action_counts = df['next_best_action'].value_counts().to_dict()
        total_customers = len(df)
        
        return {
            'total': total_customers,
            'actions': action_counts
        }
    
    @output
    @render.ui
    def nba_summary():
        """Display NBA summary statistics in sidebar"""
        stats = nba_stats()
        filtered_df = filtered_nba_data()
        
        action_items = []
        for action, count in stats['actions'].items():
            pct = (count / stats['total'] * 100) if stats['total'] > 0 else 0
            action_items.append(
                ui.tags.tr(
                    ui.tags.td(action),
                    ui.tags.td(f"{count:,}", style="text-align: right; padding-left: 10px;"),
                    ui.tags.td(f"({pct:.1f}%)", style="text-align: right; padding-left: 5px;")
                )
            )
        
        return ui.div(
            ui.tags.table(
                ui.tags.tr(
                    ui.tags.td(ui.strong("Total Customers:")),
                    ui.tags.td(f"{stats['total']:,}", style="text-align: right; padding-left: 10px;", colspan="2")
                ),
                ui.tags.tr(
                    ui.tags.td(ui.strong("Filtered View:")),
                    ui.tags.td(f"{len(filtered_df):,}", style="text-align: right; padding-left: 10px;", colspan="2")
                ),
                ui.tags.tr(ui.tags.td(ui.hr(), colspan="3")),
                *action_items,
                style="width: 100%; font-size: 12px;"
            )
        )
    
    @output
    @render.plot
    def nba_distribution_chart():
        """Bar chart showing distribution of Next Best Actions"""
        import matplotlib.pyplot as plt
        
        stats = nba_stats()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if stats['actions']:
            actions = list(stats['actions'].keys())
            counts = list(stats['actions'].values())
            
            # Define colors for different actions
            color_map = {
                'Ship new device': '#dc3545',  # Red - urgent
                'Speed upgrade + new device': '#28a745',  # Green - high value
                'Speed upgrade only': '#17a2b8',  # Blue - medium value
                'Keep as is': '#6c757d',  # Gray - no action needed
                'No action recommended': '#ffc107'  # Yellow - review needed
            }
            
            colors = [color_map.get(action, '#6c757d') for action in actions]
            
            bars = ax.bar(actions, counts, color=colors, edgecolor='black', linewidth=1.5)
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height):,}',
                       ha='center', va='bottom', fontweight='bold', fontsize=10)
            
            ax.set_xlabel('Next Best Action', fontsize=12, fontweight='bold')
            ax.set_ylabel('Number of Customers', fontsize=12, fontweight='bold')
            ax.set_title('Distribution of Next Best Actions', fontsize=14, fontweight='bold', pad=20)
            ax.tick_params(axis='x', rotation=45)
            plt.xticks(ha='right')
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            
            # Add percentage labels
            total = sum(counts)
            for i, (bar, count) in enumerate(zip(bars, counts)):
                pct = (count / total * 100) if total > 0 else 0
                ax.text(bar.get_x() + bar.get_width()/2., height * 0.5,
                       f'{pct:.1f}%',
                       ha='center', va='center', fontsize=9, color='white', fontweight='bold')
        else:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=14)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        
        plt.tight_layout()
        return fig
    
    @output
    @render.data_frame
    def nba_table():
        """Display filtered customer data with Next Best Action"""
        df = filtered_nba_data()
        
        # Select relevant columns for display
        display_columns = [
            'customer_id', 
            'next_best_action',
            'customer_segment',
            'clv_decile',
            'churn_risk',
            'sqs_score',
            'broadband_type',
            'current_bb_speed',
            'device_model',
            'device_status',
            'isp'
        ]
        
        display_df = df[display_columns].copy()
        
        # Rename columns for better readability
        display_df.columns = [
            'Customer ID',
            'Next Best Action',
            'Customer Segment',
            'CLV Decile',
            'Churn Risk',
            'SQS Score',
            'Broadband Type',
            'Current Speed',
            'Device Model',
            'Device Status',
            'ISP'
        ]
        
        # Sort by Next Best Action priority
        action_priority = {
            'Ship new device': 1,
            'Speed upgrade + new device': 2,
            'Speed upgrade only': 3,
            'Keep as is': 4,
            'No action recommended': 5
        }
        
        display_df['_priority'] = display_df['Next Best Action'].map(action_priority)
        display_df = display_df.sort_values('_priority').drop('_priority', axis=1)
        
        return render.DataGrid(display_df, width="100%", height="600px")


app = App(app_ui, server)

