/**
 * Main Application Module
 * Initializes and coordinates all dashboard components
 */

const App = {
    data: null,
    
    /**
     * Initialize the application
     */
    async init() {
        try {
            this.showLoading();
            this.setupTabs();
            await this.loadData();
            this.initializeModules();
            this.hideLoading();
        } catch (error) {
            this.showError(error.message);
            console.error('Application initialization error:', error);
        }
    },
    
    /**
     * Load all required data
     */
    async loadData() {
        this.data = await DataLoader.loadAllData();
        console.log('Data loaded successfully:', {
            customers: this.data.customerData.length,
            devices: this.data.deviceData.length,
            nba: this.data.nbaData.length
        });
    },
    
    /**
     * Setup tab navigation
     */
    setupTabs() {
        const tabs = document.querySelectorAll('.tab');
        const tabContents = document.querySelectorAll('.tab-content');
        
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                // Remove active class from all tabs and contents
                tabs.forEach(t => t.classList.remove('active'));
                tabContents.forEach(tc => tc.classList.remove('active'));
                
                // Add active class to clicked tab
                tab.classList.add('active');
                
                // Show corresponding content
                const tabName = tab.dataset.tab;
                const content = document.getElementById(`${tabName}-content`);
                if (content) {
                    content.classList.add('active');
                }
                
                // Initialize tab-specific modules if needed
                this.onTabChange(tabName);
            });
        });
        
        // Activate first tab by default
        if (tabs.length > 0) {
            tabs[0].click();
        }
    },
    
    /**
     * Initialize dashboard modules
     */
    initializeModules() {
        // Initialize Device Overview Dashboard
        Dashboard.init(this.data.deviceData);
        
        // Get NBA data merged with device serial numbers
        const nbaWithSerialNumbers = DataLoader.getNBAMergedData();
        
        // Initialize NBA Module
        NBA.init(nbaWithSerialNumbers);
    },
    
    /**
     * Handle tab change events
     */
    onTabChange(tabName) {
        console.log('Tab changed to:', tabName);
        
        // Refresh visualizations when switching tabs
        switch(tabName) {
            case 'overview':
                Dashboard.updateDashboard();
                break;
            case 'nba':
                NBA.updateNBAView();
                break;
            default:
                break;
        }
    },
    
    /**
     * Show loading indicator
     */
    showLoading() {
        // Create loading overlay
        const overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(102, 126, 234, 0.95);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            color: white;
        `;
        overlay.innerHTML = `
            <div style="text-align: center;">
                <h2 style="color: white; font-size: 2em;">⏳ Loading Dashboard...</h2>
                <p style="font-size: 1.2em; margin-top: 20px;">Loading customer and device data...</p>
                <p style="font-size: 0.9em; margin-top: 10px; opacity: 0.9;">This may take a few seconds for large datasets.</p>
            </div>
        `;
        document.body.appendChild(overlay);
    },
    
    /**
     * Hide loading indicator
     */
    hideLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.remove();
        }
    },
    
    /**
     * Show error message
     */
    showError(message) {
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = `
            <div class="error">
                <h2>❌ Error Loading Dashboard</h2>
                <p><strong>${message}</strong></p>
                <hr style="margin: 20px 0; border: 1px solid #dc3545;">
                <h3>Troubleshooting Steps:</h3>
                <ol style="text-align: left; display: inline-block; line-height: 2;">
                    <li>Open browser console (Press F12) to see detailed errors</li>
                    <li>Try hard refresh: <strong>Ctrl + Shift + R</strong></li>
                    <li>Verify server is running at: <strong>http://localhost:8000</strong></li>
                    <li>Check that CSV files exist in: <strong>Data/Data Output/</strong></li>
                </ol>
                <p style="margin-top: 20px;">
                    <button onclick="location.reload()" style="padding: 10px 20px; font-size: 16px; cursor: pointer;">
                        🔄 Retry Loading
                    </button>
                </p>
            </div>
        `;
    }
};

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});

window.App = App;

