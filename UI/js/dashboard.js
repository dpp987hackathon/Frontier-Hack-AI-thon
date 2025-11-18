/**
 * Dashboard Module
 * Handles device overview dashboard logic
 */

const Dashboard = {
    deviceData: null,
    activeThreshold: 30,
    
    /**
     * Initialize the dashboard
     */
    init(deviceData) {
        console.log('Dashboard.init called with deviceData:', deviceData ? deviceData.length : 'undefined');
        this.deviceData = deviceData;
        this.setupControls();
        this.updateDashboard();
    },
    
    /**
     * Setup control event listeners
     */
    setupControls() {
        // No controls needed - active threshold is fixed at 30 days
    },
    
    /**
     * Calculate statistics based on current threshold
     */
    calculateStats() {
        const currentDate = new Date();
        const thresholdMs = this.activeThreshold * 24 * 60 * 60 * 1000;
        
        const stats = {
            total: this.deviceData.length,
            frontier: 0,
            nonFrontier: 0,
            frontierActive: 0,
            frontierInactive: 0,
            nonFrontierActive: 0,
            nonFrontierInactive: 0
        };
        
        this.deviceData.forEach(device => {
            const isFrontier = device.isp === 'Frontier Communications';
            const isActive = (currentDate - device.last_alive_date) < thresholdMs;
            
            if (isFrontier) {
                stats.frontier++;
                if (isActive) {
                    stats.frontierActive++;
                } else {
                    stats.frontierInactive++;
                }
            } else {
                stats.nonFrontier++;
                if (isActive) {
                    stats.nonFrontierActive++;
                } else {
                    stats.nonFrontierInactive++;
                }
            }
        });
        
        return stats;
    },
    
    /**
     * Update all dashboard visualizations
     */
    updateDashboard() {
        const stats = this.calculateStats();
        this.updateStatCards(stats);
        this.updateTreeView(stats);
        this.updateCharts(stats);
    },
    
    /**
     * Update statistic cards
     */
    updateStatCards(stats) {
        console.log('Dashboard.updateStatCards called with stats:', stats);
        const totalEl = document.getElementById('total-devices');
        const targetEl = document.getElementById('target-devices');
        const frontierEl = document.getElementById('frontier-devices');
        const nonFrontierEl = document.getElementById('non-frontier-devices');
        const liabilityEl = document.getElementById('expected-liability');
        
        if (totalEl) totalEl.textContent = stats.total.toLocaleString();
        if (targetEl) targetEl.textContent = stats.frontierActive.toLocaleString();
        if (frontierEl) frontierEl.textContent = stats.frontier.toLocaleString();
        if (nonFrontierEl) nonFrontierEl.textContent = stats.nonFrontier.toLocaleString();
        
        // Calculate expected liability if no action is taken: Total devices × $6/device/year
        if (liabilityEl) {
            const licenseCostPerDevice = 6;
            const expectedLiability = stats.total * licenseCostPerDevice;
            console.log('Expected liability calculation:', stats.total, '×', licenseCostPerDevice, '=', expectedLiability);
            liabilityEl.textContent = '$' + expectedLiability.toLocaleString();
        } else {
            console.warn('Expected liability element not found');
        }
    },
    
    /**
     * Update tree visualization
     */
    updateTreeView(stats) {
        const treeHTML = `
            <div class="tree-level text-center">
                <div class="tree-node">
                    <strong>Total Devices</strong><br>
                    ${stats.total.toLocaleString()}
                </div>
            </div>
            <div style="text-align: center; font-size: 2em; color: #999;">↓</div>
            <div class="tree-level text-center">
                <div class="tree-node frontier">
                    <strong>Frontier</strong><br>
                    ${stats.frontier.toLocaleString()}
                </div>
                <div class="tree-node">
                    <strong>Non-Frontier</strong><br>
                    ${stats.nonFrontier.toLocaleString()}
                </div>
            </div>
            <div style="text-align: center; font-size: 2em; color: #999;">↓</div>
            <div class="tree-level text-center">
                <div class="tree-node active target">
                    <strong>🎯 Frontier Active</strong><br>
                    ${stats.frontierActive.toLocaleString()}
                </div>
                <div class="tree-node inactive">
                    <strong>Frontier Inactive</strong><br>
                    ${stats.frontierInactive.toLocaleString()}
                </div>
                <div class="tree-node active">
                    <strong>Non-Frontier Active</strong><br>
                    ${stats.nonFrontierActive.toLocaleString()}
                </div>
                <div class="tree-node inactive">
                    <strong>Non-Frontier Inactive</strong><br>
                    ${stats.nonFrontierInactive.toLocaleString()}
                </div>
            </div>
        `;
        
        const treeView = document.getElementById('tree-view');
        if (treeView) {
            treeView.innerHTML = treeHTML;
        }
    },
    
    /**
     * Update pie charts
     */
    updateCharts(stats) {
        // Frontier chart
        const frontierData = [
            { label: 'Active', value: stats.frontierActive },
            { label: 'Inactive', value: stats.frontierInactive }
        ];
        Charts.drawPieChart('frontier-chart', frontierData, ['#38ef7d', '#ee0979']);
        
        // Non-Frontier chart
        const nonFrontierData = [
            { label: 'Active', value: stats.nonFrontierActive },
            { label: 'Inactive', value: stats.nonFrontierInactive }
        ];
        Charts.drawPieChart('non-frontier-chart', nonFrontierData, ['#38ef7d', '#ee0979']);
    }
};

window.Dashboard = Dashboard;

