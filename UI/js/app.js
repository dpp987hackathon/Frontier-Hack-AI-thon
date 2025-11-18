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
        
        // Initialize Actuals module
        this.initializeActuals();
    },
    
    /**
     * Initialize Actuals tab functionality
     */
    initializeActuals() {
        // Filter for Frontier Active devices only
        const frontierActiveDevices = this.getFrontierActiveDevices();
        
        // Update device count
        const deviceCountEl = document.getElementById('actuals-device-count');
        const rowCountEl = document.getElementById('actuals-row-count');
        
        if (deviceCountEl) {
            deviceCountEl.textContent = frontierActiveDevices.length.toLocaleString();
        }
        if (rowCountEl) {
            rowCountEl.textContent = frontierActiveDevices.length.toLocaleString();
        }
        
        // Setup download button
        const downloadBtn = document.getElementById('download-actuals');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => this.downloadActualsFile());
        }
    },
    
    /**
     * Get Frontier Active devices only
     */
    getFrontierActiveDevices() {
        if (!this.data || !this.data.deviceData) {
            return [];
        }
        
        const currentDate = new Date();
        const activeThreshold = 30; // days
        const thresholdMs = activeThreshold * 24 * 60 * 60 * 1000;
        
        return this.data.deviceData.filter(device => {
            // Must be on Frontier network
            const isFrontier = device.isp === 'Frontier Communications';
            
            // Must be active (last alive within threshold)
            const lastAliveDate = new Date(device.last_alive_date);
            const isActive = (currentDate - lastAliveDate) < thresholdMs;
            
            return isFrontier && isActive;
        });
    },
    
    /**
     * Download Eero Audit File (CSV)
     */
    downloadActualsFile() {
        if (!this.data || !this.data.deviceData) {
            alert('No data available to download');
            return;
        }
        
        try {
            // Get Frontier Active devices only
            const frontierActiveDevices = this.getFrontierActiveDevices();
            
            if (frontierActiveDevices.length === 0) {
                alert('No Frontier Active devices found to export');
                return;
            }
            
            // Prepare data with only required columns: serial_number, customer_id, device_model
            const auditData = frontierActiveDevices.map(device => ({
                serial_number: device.serial_number || '',
                customer_id: device.customer_id || '',
                device_model: device.device_model || ''
            }));
            
            // Create CSV header
            const headers = ['serial_number', 'customer_id', 'device_model'];
            const csvRows = [headers.join(',')];
            
            // Add data rows
            auditData.forEach(row => {
                const values = headers.map(header => {
                    const value = row[header];
                    // Escape values that contain commas or quotes
                    const escaped = String(value).replace(/"/g, '""');
                    return `"${escaped}"`;
                });
                csvRows.push(values.join(','));
            });
            
            // Create CSV blob
            const csvContent = csvRows.join('\n');
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            
            // Create download link
            const link = document.createElement('a');
            const url = URL.createObjectURL(blob);
            const timestamp = new Date().toISOString().split('T')[0];
            const filename = `eero_audit_frontier_active_${timestamp}.csv`;
            
            link.setAttribute('href', url);
            link.setAttribute('download', filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            console.log(`Downloaded Eero Audit File (Frontier Active): ${filename} (${auditData.length} devices)`);
        } catch (error) {
            console.error('Error downloading actuals file:', error);
            alert('Error generating download file. Please check console for details.');
        }
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
            case 'actuals':
                // Actuals tab is static, no refresh needed
                console.log('Actuals tab loaded - ready for download');
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

