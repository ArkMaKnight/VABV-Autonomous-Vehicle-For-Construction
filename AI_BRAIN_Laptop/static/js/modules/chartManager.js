import { Chart } from "chart.js";

export class chartManager {
    constructor() {
        const ctx = document.getElementById('est-one');
        const radar = {
    labels: [
        'person',
        'animal',
        'hard-hat',
        'vest',
        'objects'
    ],
    datasets: [{
        label: 'Cantidad Detectada en Frames Transmitidos',
        data: [5,4,3,2,1],
        backgroundColor: [
            'rgb(96, 28, 255)',
            'rgb(0, 255, 34)',
            'rgb(255, 128, 0)',
            'rgb(255, 213, 0)',
            'rgb(255, 0, 0)'
        ]
    }]
};
    this.chartOne = new Chart(ctx, {
    type: 'polarArea',
    data: radar,
    options: {}
    })
    }

    updateCharts(newData) {
        this.chartOne.data.datasets[0].data = newData;
        this.chartOne.update();
    }
}
