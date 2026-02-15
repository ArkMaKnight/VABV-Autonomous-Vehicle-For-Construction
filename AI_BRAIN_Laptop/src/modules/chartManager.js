import { Chart, registerables } from "chart.js";

export class ChartManager {
    constructor() {
        const ctx = document.getElementById('est-one');
        const ctx2 = document.getElementById('est-two');
        const ctx3 = document.getElementById('est-three');
        this.destroyCanvas(ctx);
        this.destroyCanvas(ctx2);
        this.destroyCanvas(ctx3);


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
    options: {
        maintainAspectRatio: false,
        responsive: true
    }
    });


    this.chartTwo = new Chart(ctx2, {
        type: 'radar',
        data: radar,
        options: {      
            responsive: true,  
            maintainAspectRatio: false,
        }
    });

    this.chatThree = new Chart(ctx3, {
        type: 'bar',
        
        data: radar,
        options: {
            responsive: true,
            maintainAspectRatio: false,
        }
    })
}
    updateCharts(newData) {
        this.chartOne.data.datasets[0].data = newData;
        this.chartOne.update();
    }

    destroyCanvas(ctx) {
        let x = Chart.getChart(ctx);
        if (x) x.destroy();
        
     
    }
}