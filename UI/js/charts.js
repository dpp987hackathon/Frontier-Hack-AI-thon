/**
 * Charts Module
 * D3.js chart rendering functions
 */

const Charts = {
    /**
     * Draw a pie chart using D3.js
     */
    drawPieChart(containerId, data, colors) {
        // Clear existing chart
        d3.select(`#${containerId}`).selectAll('*').remove();
        
        const width = 400;
        const height = 400;
        const radius = Math.min(width, height) / 2 - 40;
        
        const svg = d3.select(`#${containerId}`)
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .append('g')
            .attr('transform', `translate(${width / 2}, ${height / 2})`);
        
        const pie = d3.pie()
            .value(d => d.value)
            .sort(null);
        
        const arc = d3.arc()
            .innerRadius(0)
            .outerRadius(radius);
        
        const arcHover = d3.arc()
            .innerRadius(0)
            .outerRadius(radius + 10);
        
        const arcs = svg.selectAll('arc')
            .data(pie(data))
            .enter()
            .append('g')
            .attr('class', 'arc');
        
        arcs.append('path')
            .attr('d', arc)
            .attr('fill', (d, i) => colors[i])
            .attr('class', 'pie-slice')
            .on('mouseover', function(event, d) {
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr('d', arcHover);
            })
            .on('mouseout', function(event, d) {
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr('d', arc);
            });
        
        arcs.append('text')
            .attr('transform', d => `translate(${arc.centroid(d)})`)
            .attr('text-anchor', 'middle')
            .attr('class', 'chart-label')
            .attr('fill', 'white')
            .style('font-size', '14px')
            .style('font-weight', 'bold')
            .text(d => {
                const percent = ((d.data.value / d3.sum(data, d => d.value)) * 100).toFixed(1);
                return `${d.data.label}: ${percent}%`;
            });
    },
    
    /**
     * Draw an interactive pie chart with click handlers and highlighting
     */
    drawInteractivePieChart(containerId, data, colors, onClickCallback, activeFilter) {
        // Clear existing chart
        d3.select(`#${containerId}`).selectAll('*').remove();
        
        const width = 600;
        const height = 450;
        const radius = Math.min(width, height) / 2 - 100;
        
        const svg = d3.select(`#${containerId}`)
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .append('g')
            .attr('transform', `translate(${width / 3}, ${height / 2})`);
        
        const pie = d3.pie()
            .value(d => d.value)
            .sort(null);
        
        const arc = d3.arc()
            .innerRadius(0)
            .outerRadius(radius);
        
        const arcHover = d3.arc()
            .innerRadius(0)
            .outerRadius(radius + 10);
        
        const arcSelected = d3.arc()
            .innerRadius(0)
            .outerRadius(radius + 15);
        
        const arcs = svg.selectAll('arc')
            .data(pie(data))
            .enter()
            .append('g')
            .attr('class', 'arc');
        
        arcs.append('path')
            .attr('d', d => d.data.label === activeFilter ? arcSelected(d) : arc(d))
            .attr('fill', (d, i) => colors[i % colors.length])
            .attr('class', 'pie-slice')
            .style('cursor', 'pointer')
            .style('opacity', d => d.data.label === activeFilter ? 1 : 0.8)
            .style('stroke', d => d.data.label === activeFilter ? '#333' : 'none')
            .style('stroke-width', d => d.data.label === activeFilter ? '3px' : '0')
            .on('mouseover', function(event, d) {
                if (d.data.label !== activeFilter) {
                    d3.select(this)
                        .transition()
                        .duration(200)
                        .attr('d', arcHover(d))
                        .style('opacity', 1);
                }
            })
            .on('mouseout', function(event, d) {
                if (d.data.label !== activeFilter) {
                    d3.select(this)
                        .transition()
                        .duration(200)
                        .attr('d', arc(d))
                        .style('opacity', 0.8);
                }
            })
            .on('click', function(event, d) {
                console.log('Pie slice clicked:', d.data.label);
                onClickCallback(d.data.label);
            });
        
        arcs.append('text')
            .attr('transform', d => `translate(${arc.centroid(d)})`)
            .attr('text-anchor', 'middle')
            .attr('class', 'chart-label')
            .attr('fill', 'white')
            .style('font-size', '12px')
            .style('font-weight', 'bold')
            .style('pointer-events', 'none')
            .text(d => {
                const percent = ((d.data.value / d3.sum(data, d => d.value)) * 100).toFixed(1);
                if (percent > 5) { // Only show label if segment is large enough
                    return `${d.data.label}`;
                }
                return '';
            });
        
        // Add percentage labels
        arcs.append('text')
            .attr('transform', d => {
                const centroid = arc.centroid(d);
                return `translate(${centroid[0]}, ${centroid[1] + 15})`;
            })
            .attr('text-anchor', 'middle')
            .attr('fill', 'white')
            .style('font-size', '11px')
            .style('font-weight', 'normal')
            .style('pointer-events', 'none')
            .text(d => {
                const percent = ((d.data.value / d3.sum(data, d => d.value)) * 100).toFixed(1);
                if (percent > 5) {
                    return `${percent}%`;
                }
                return '';
            });
        
        // Add legend
        const legend = svg.append('g')
            .attr('transform', `translate(${radius + 40}, ${-radius + 20})`);
        
        data.forEach((d, i) => {
            const legendRow = legend.append('g')
                .attr('transform', `translate(0, ${i * 20})`);
            
            legendRow.append('rect')
                .attr('width', 12)
                .attr('height', 12)
                .attr('fill', colors[i % colors.length]);
            
            legendRow.append('text')
                .attr('x', 16)
                .attr('y', 10)
                .style('font-size', '10px')
                .style('font-weight', '500')
                .text(`${d.label}: ${d.value.toLocaleString()}`);
        });
    },
    
    /**
     * Draw a horizontal bar chart
     */
    drawBarChart(containerId, data, colorMap) {
        // Clear existing chart
        d3.select(`#${containerId}`).selectAll('*').remove();
        
        // Get container width for responsive chart
        const container = document.getElementById(containerId);
        const containerWidth = container ? container.offsetWidth : 1200;
        
        const margin = { top: 20, right: 60, bottom: 80, left: 250 };
        const width = containerWidth - margin.left - margin.right;
        const height = Math.max(400, data.length * 80);
        
        const svg = d3.select(`#${containerId}`)
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left}, ${margin.top})`);
        
        const x = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.value)])
            .range([0, width]);
        
        const y = d3.scaleBand()
            .domain(data.map(d => d.label))
            .range([0, height])
            .padding(0.2);
        
        // Add bars
        svg.selectAll('.bar')
            .data(data)
            .enter()
            .append('rect')
            .attr('class', 'bar')
            .attr('x', 0)
            .attr('y', d => y(d.label))
            .attr('width', d => x(d.value))
            .attr('height', y.bandwidth())
            .attr('fill', d => colorMap[d.label] || '#667eea')
            .style('cursor', 'pointer')
            .on('mouseover', function() {
                d3.select(this)
                    .transition()
                    .duration(200)
                    .style('opacity', 0.7);
            })
            .on('mouseout', function() {
                d3.select(this)
                    .transition()
                    .duration(200)
                    .style('opacity', 1);
            });
        
        // Add value labels
        svg.selectAll('.label')
            .data(data)
            .enter()
            .append('text')
            .attr('class', 'label')
            .attr('x', d => x(d.value) + 10)
            .attr('y', d => y(d.label) + y.bandwidth() / 2)
            .attr('dy', '.35em')
            .style('font-size', '16px')
            .style('font-weight', 'bold')
            .style('fill', '#333')
            .text(d => {
                const total = d3.sum(data, d => d.value);
                const percent = ((d.value / total) * 100).toFixed(1);
                return `${d.value.toLocaleString()} (${percent}%)`;
            });
        
        // Add y-axis
        svg.append('g')
            .call(d3.axisLeft(y))
            .selectAll('text')
            .style('font-size', '14px')
            .style('font-weight', '500');
        
        // Add x-axis
        svg.append('g')
            .attr('transform', `translate(0, ${height})`)
            .call(d3.axisBottom(x).ticks(10).tickFormat(d => d.toLocaleString()))
            .selectAll('text')
            .style('font-size', '13px');
        
        // Add X axis label
        svg.append('text')
            .attr('x', width / 2)
            .attr('y', height + 55)
            .attr('text-anchor', 'middle')
            .style('font-size', '14px')
            .style('font-weight', '600')
            .style('fill', '#666')
            .text('Number of Customers');
    },
    
    /**
     * Create a simple vertical bar chart
     */
    drawVerticalBarChart(containerId, data, color = '#667eea') {
        d3.select(`#${containerId}`).selectAll('*').remove();
        
        const margin = { top: 20, right: 30, bottom: 60, left: 60 };
        const width = 600 - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;
        
        const svg = d3.select(`#${containerId}`)
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left}, ${margin.top})`);
        
        const x = d3.scaleBand()
            .domain(data.map(d => d.label))
            .range([0, width])
            .padding(0.1);
        
        const y = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.value)])
            .range([height, 0]);
        
        svg.selectAll('.bar')
            .data(data)
            .enter()
            .append('rect')
            .attr('class', 'bar')
            .attr('x', d => x(d.label))
            .attr('y', d => y(d.value))
            .attr('width', x.bandwidth())
            .attr('height', d => height - y(d.value))
            .attr('fill', color);
        
        svg.append('g')
            .attr('transform', `translate(0, ${height})`)
            .call(d3.axisBottom(x))
            .selectAll('text')
            .attr('transform', 'rotate(-45)')
            .style('text-anchor', 'end');
        
        svg.append('g')
            .call(d3.axisLeft(y));
    },
    
    /**
     * Draw an interactive horizontal bar chart with click handlers and highlighting
     */
    drawInteractiveBarChart(containerId, data, colors, onClickCallback, activeFilter) {
        // Clear existing chart
        d3.select(`#${containerId}`).selectAll('*').remove();
        
        // Get container width for responsive chart
        const container = document.getElementById(containerId);
        const containerWidth = container ? container.offsetWidth : 1200;
        
        const margin = { top: 30, right: 60, bottom: 80, left: 180 };
        const width = containerWidth - margin.left - margin.right;
        const height = Math.max(400, data.length * 60); // Dynamic height based on number of bars
        
        const svg = d3.select(`#${containerId}`)
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left}, ${margin.top})`);
        
        // Calculate total for percentages
        const total = d3.sum(data, d => d.value);
        
        const x = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.value)])
            .nice()
            .range([0, width]);
        
        const y = d3.scaleBand()
            .domain(data.map(d => d.label))
            .range([0, height])
            .padding(0.2);
        
        // Add bars with click handlers
        const bars = svg.selectAll('.bar')
            .data(data)
            .enter()
            .append('g')
            .attr('class', 'bar-group');
        
        bars.append('rect')
            .attr('class', 'bar')
            .attr('x', 0)
            .attr('y', d => y(d.label))
            .attr('width', d => x(d.value))
            .attr('height', y.bandwidth())
            .attr('fill', (d, i) => colors[i % colors.length])
            .attr('opacity', d => activeFilter && activeFilter !== d.label ? 0.3 : 1)
            .style('cursor', 'pointer')
            .style('stroke', d => activeFilter === d.label ? '#333' : 'none')
            .style('stroke-width', d => activeFilter === d.label ? 3 : 0)
            .on('click', function(event, d) {
                console.log('Bar clicked:', d.label);
                if (onClickCallback) {
                    onClickCallback(d.label);
                }
            })
            .on('mouseover', function(event, d) {
                if (!activeFilter || activeFilter === d.label) {
                    d3.select(this)
                        .transition()
                        .duration(200)
                        .attr('opacity', 0.8)
                        .style('stroke', '#333')
                        .style('stroke-width', 2);
                }
            })
            .on('mouseout', function(event, d) {
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr('opacity', activeFilter && activeFilter !== d.label ? 0.3 : 1)
                    .style('stroke', activeFilter === d.label ? '#333' : 'none')
                    .style('stroke-width', activeFilter === d.label ? 3 : 0);
            });
        
        // Add value labels on bars
        bars.append('text')
            .attr('x', d => x(d.value) + 5)
            .attr('y', d => y(d.label) + y.bandwidth() / 2)
            .attr('dy', '0.35em')
            .style('font-size', '14px')
            .style('font-weight', 'bold')
            .style('fill', '#333')
            .style('pointer-events', 'none')
            .text(d => d.value.toLocaleString());
        
        // Add percentage labels
        bars.append('text')
            .attr('x', d => x(d.value) + 5)
            .attr('y', d => y(d.label) + y.bandwidth() / 2 + 18)
            .attr('dy', '0.35em')
            .style('font-size', '11px')
            .style('fill', '#666')
            .style('pointer-events', 'none')
            .text(d => {
                const percent = ((d.value / total) * 100).toFixed(1);
                return `(${percent}%)`;
            });
        
        // Add Y axis (labels)
        svg.append('g')
            .call(d3.axisLeft(y))
            .selectAll('text')
            .style('font-size', '13px')
            .style('font-weight', '500');
        
        // Add X axis
        svg.append('g')
            .attr('transform', `translate(0, ${height})`)
            .call(d3.axisBottom(x).ticks(10).tickFormat(d => d.toLocaleString()))
            .selectAll('text')
            .style('font-size', '12px');
        
        // Add X axis label
        svg.append('text')
            .attr('x', width / 2)
            .attr('y', height + 50)
            .attr('text-anchor', 'middle')
            .style('font-size', '13px')
            .style('font-weight', '600')
            .style('fill', '#666')
            .text('Number of Devices');
        
        // Add clear filter button if there's an active filter
        if (activeFilter) {
            svg.append('text')
                .attr('x', width)
                .attr('y', -10)
                .attr('text-anchor', 'end')
                .style('font-size', '12px')
                .style('fill', '#2196F3')
                .style('cursor', 'pointer')
                .style('text-decoration', 'underline')
                .text('✕ Clear Filter')
                .on('click', function() {
                    if (onClickCallback) {
                        onClickCallback(null);
                    }
                });
        }
    }
};

window.Charts = Charts;

