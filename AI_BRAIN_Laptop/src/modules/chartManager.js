import { Chart, registerables } from "chart.js";

// Tema oscuro global para Chart.js
Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.08)';

export class ChartManager {
    constructor() {
        const ctx = document.getElementById('est-one');
        const ctx2 = document.getElementById('est-two');
        const ctx3 = document.getElementById('est-three');
        this.destroyCanvas(ctx);
        this.destroyCanvas(ctx2);
        this.destroyCanvas(ctx3);

        const labels = ['Personas', 'Animales', 'Cascos', 'Chalecos', 'Objetos'];
        const bgColors = [
            'rgba(96, 165, 250, 0.65)',
            'rgba(52, 211, 153, 0.65)',
            'rgba(251, 191, 36, 0.65)',
            'rgba(251, 146, 60, 0.65)',
            'rgba(248, 113, 113, 0.65)'
        ];
        const borderColors = [
            'rgb(96, 165, 250)',
            'rgb(52, 211, 153)',
            'rgb(251, 191, 36)',
            'rgb(251, 146, 60)',
            'rgb(248, 113, 113)'
        ];

        const chartData = {
            labels,
            datasets: [{
                label: 'Detecciones por Frame',
                data: [0, 0, 0, 0, 0],
                backgroundColor: bgColors,
                borderColor: borderColors,
                borderWidth: 1.5
            }]
        };

    this.chartOne = new Chart(ctx, {
        type: 'polarArea',
        data: JSON.parse(JSON.stringify(chartData)),
        options: {
            maintainAspectRatio: false,
            responsive: true,
            plugins: {
                legend: { labels: { color: '#cbd5e1', padding: 12 } }
            },
            scales: {
                r: {
                    grid: { color: 'rgba(255,255,255,0.08)' },
                    ticks: { color: '#94a3b8', backdropColor: 'transparent' }
                }
            }
        }
    });

    this.chartTwo = new Chart(ctx2, {
        type: 'radar',
        data: JSON.parse(JSON.stringify(chartData)),
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#cbd5e1', padding: 12 } }
            },
            scales: {
                r: {
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    angleLines: { color: 'rgba(255,255,255,0.1)' },
                    pointLabels: { color: '#cbd5e1', font: { size: 11 } },
                    ticks: { color: '#94a3b8', backdropColor: 'transparent' }
                }
            }
        }
    });

    this.chatThree = new Chart(ctx3, {
        type: 'bar',
        data: JSON.parse(JSON.stringify(chartData)),
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#cbd5e1', padding: 12 } }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#94a3b8', stepSize: 1 },
                    beginAtZero: true
                }
            }
        }
    });
}
    updateCharts(newData) {
        this.chartOne.data.datasets[0].data = newData;
        this.chartOne.update();

        this.chartTwo.data.datasets[0].data = newData;
        this.chartTwo.update();

        this.chatThree.data.datasets[0].data = newData;
        this.chatThree.update();
    }

    destroyCanvas(ctx) {
        let x = Chart.getChart(ctx);
        if (x) x.destroy();
        
     
    }
}