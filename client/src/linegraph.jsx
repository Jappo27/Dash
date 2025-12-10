
import React, { useState, useEffect } from 'react';
import { Chart } from 'primereact/chart';

export default function LineStylesDemo({title, labels, dataset, colour}) {
    const [chartData, setChartData] = useState({});
    const [chartOptions, setChartOptions] = useState({});

    useEffect(() => {
        const documentStyle = getComputedStyle(document.documentElement);
        const textColor = documentStyle.getPropertyValue('--text-color');
        const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
        const surfaceBorder = documentStyle.getPropertyValue('--surface-border');

        let avg = 0;
        let minimum = 0;
        let maximum = 0;

        if (dataset.length > 0) {
            for (let i = 0; i < dataset.length; i++) {
                avg += dataset[i];
            }
            avg = avg / dataset.length;
            minimum = Math.min(...dataset) - avg;
            maximum = Math.max(...dataset) + avg;
        } else {
            minimum = Math.min(...dataset);
            maximum = Math.max(...dataset);
        }

        const data = {
            labels: labels,
            datasets: [
                {
                    label: title,
                    data: dataset,
                    borderColor: [colour],
           
                }
                ]
        };
        const options = {
            maintainAspectRatio: false,
            aspectRatio: 0.6,
            plugins: {
                legend: {
                    labels: {
                        color: textColor
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: ["#FFFFFF"]
                    },
                    grid: {
                        color: ['#FFFFFF'],
                        opacity: 0,
                    }
                },
                y: {
                    max: maximum,
                    min: minimum,
                    ticks: {
                        color: ["#FFFFFF"]
                    },
                    grid: {
                        color: ['#FFFFFF'],
                        opacity: 0,
                    }
                }
            }
        };

        setChartData(data);
        setChartOptions(options);
    }, [title, labels, dataset, colour]);

    return (
        <div className="card">
            <Chart type="line" data={chartData} options={chartOptions} />
        </div>
    )
}
        