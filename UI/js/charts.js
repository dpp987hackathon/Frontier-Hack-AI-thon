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
     * Draw a horizontal bar chart
     */
    drawBarChart(containerId, data, colorMap) {
        // Clear existing chart
        d3.select(`#${containerId}`).selectAll('*').remove();
        
        const margin = { top: 20, right: 30, bottom: 60, left: 200 };
        const width = 800 - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;
        
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
            .padding(0.1);
        
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
            .attr('x', d => x(d.value) + 5)
            .attr('y', d => y(d.label) + y.bandwidth() / 2)
            .attr('dy', '.35em')
            .style('font-size', '12px')
            .style('font-weight', 'bold')
            .text(d => {
                const total = d3.sum(data, d => d.value);
                const percent = ((d.value / total) * 100).toFixed(1);
                return `${d.value.toLocaleString()} (${percent}%)`;
            });
        
        // Add y-axis
        svg.append('g')
            .call(d3.axisLeft(y))
            .style('font-size', '12px');
        
        // Add x-axis
        svg.append('g')
            .attr('transform', `translate(0, ${height})`)
            .call(d3.axisBottom(x).ticks(5).tickFormat(d => d.toLocaleString()))
            .style('font-size', '12px');
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
    }
};

window.Charts = Charts;

