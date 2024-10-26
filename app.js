// Initialize map
const map = L.map('map').setView([51.505, -0.09], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Function to fetch and visualize data
async function fetchData(location) {
    const response = await fetch(http://127.0.0.1:8000/data/${location});
    const result = await response.json();
    
    // Visualize using D3.js
    const svg = d3.select("#visualization").append("svg").attr("width", 500).attr("height", 300);
    
    svg.selectAll("rect")
        .data(result.data)
        .enter()
        .append("rect")
        .attr("x", (d, i) => i * 100)
        .attr("y", d => 300 - d.pm25 * 5)
        .attr("width", 90)
        .attr("height", d => d.pm25 * 5)
        .attr("fill", "steelblue");

    // Display data on the map
    result.data.forEach(d => {
        const marker = L.marker([51.5 + Math.random() * 0.1, -0.09 + Math.random() * 0.1]).addTo(map);
        marker.bindPopup(<b>Location:</b> ${d.location}<br><b>PM2.5:</b> ${d.pm25});
    });
}

// Initial data fetch
fetchData('SampleLocation');