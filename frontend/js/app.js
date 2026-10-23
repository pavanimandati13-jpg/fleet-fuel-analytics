  const API_BASE = 'https://fleet-fuel-analytics-2.onrender.com/api';

async function loadSummary() {
  const res = await fetch(`${API_BASE}/analytics/summary`);
  const data = await res.json();
  document.getElementById('total-fuel').textContent = data.total_fuel_liters + ' L';
  document.getElementById('total-cost').textContent = '$' + data.total_cost;
  document.getElementById('total-vehicles').textContent = data.total_vehicles;
  document.getElementById('total-logs').textContent = data.total_fuel_logs;
}

async function loadVehicles() {
  const res = await fetch(`${API_BASE}/vehicles`);
  const vehicles = await res.json();
  const tbody = document.querySelector('#vehicles-table tbody');
  tbody.innerHTML = '';
  for (const v of vehicles) {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${v.vehicle_code}</td>
      <td>${v.make} ${v.model}</td>
      <td>${v.year}</td>
      <td>${v.fuel_type}</td>
      <td><button onclick="loadVehicleAnalytics(${v.id}, '${v.vehicle_code}')">View</button></td>
    `;
    tbody.appendChild(tr);
  }
}

async function loadVehicleAnalytics(id, code) {
  const res = await fetch(`${API_BASE}/analytics/vehicle/${id}`);
  const data = await res.json();
  const box = document.getElementById('vehicle-detail');
  if (data.error) {
    box.innerHTML = `<h3>${code}</h3><p>${data.error}</p>`;
    return;
  }
  box.innerHTML = `
    <h3>${code} — Consumption Analytics</h3>
    <p>Total distance covered: ${data.total_distance_km} km</p>
    <p>Total fuel used: ${data.total_fuel_liters} L</p>
    <p>Average consumption: <strong>${data.avg_consumption_l_per_100km} L / 100km</strong></p>
    <p>Fuel log entries analyzed: ${data.log_count}</p>
  `;
}

let monthlyChart;
async function loadMonthlyChart() {
  const res = await fetch(`${API_BASE}/analytics/monthly`);
  const data = await res.json();
  const ctx = document.getElementById('monthlyChart').getContext('2d');
  if (monthlyChart) monthlyChart.destroy();
  monthlyChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map(d => d.month),
      datasets: [{
        label: 'Fuel Consumed (Liters)',
        data: data.map(d => d.total_liters),
        borderColor: '#2563eb',
        backgroundColor: 'rgba(37,99,235,0.1)',
        fill: true,
        tension: 0.3,
      }],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: true } },
    },
  });
}

loadSummary();
loadVehicles();
loadMonthlyChart();
