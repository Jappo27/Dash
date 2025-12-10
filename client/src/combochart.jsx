import React, { useState, useEffect } from 'react';
import { Chart } from 'primereact/chart';

export default function ComboDemo({ labels, dataset, budget }) {
    const [chartData, setChartData] = useState({});
    const [chartOptions, setChartOptions] = useState({});

    useEffect(() => {
        const documentStyle = getComputedStyle(document.documentElement);
        const textColor = documentStyle.getPropertyValue('--text-color');
        const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
        const surfaceBorder = documentStyle.getPropertyValue('--surface-border');
        
        
        if (budget === '') {
            budget = 0;
        }

        const safeBudget = budget ?? 0;
        const safeDataset = Array.isArray(dataset) ? dataset : [];

        let cumulativeTotal = 0;
        const remainingBudget = safeBudget !== 0
            ? safeDataset.map(value => {
                cumulativeTotal += value;
                return safeBudget - cumulativeTotal;
            })
            : [];

        const data = {
            labels: labels,
            datasets: [
                {
                    type: 'line',
                    label: 'Remaining Budget',
                    /*https://www.geeksforgeeks.org/javascript/chart-js-general-colors/*/
                    borderColor: ['#DCB9F8'],
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4,
                    data: remainingBudget
                },
                {
                    type: 'bar',
                    label: 'Cost',
                    backgroundColor: ['#46E1FB'],
                    data: safeDataset,
                    borderColor: 'white',
                    borderWidth: 2
                }
            ]
        };

        const maxY = Math.max(...safeDataset, safeBudget);

        const options = {
            maintainAspectRatio: false,
            aspectRatio: 0.6,
            plugins: {
                legend: {
                    labels: {
                        color: ["#FFFFFF"]
                    }
                },
            },
            scales: {
                x: {
                    ticks: {
                        color: ["#FFFFFF"]
                    },
                    grid: {
                        color: ["#FFFFFF"]
                    }
                },
                y: {
                    ticks: {
                        color: ["#FFFFFF"]
                    },
                    grid: {
                        color: ["#FFFFFF"]
                    }
                }
            }
        };

        setChartData(data);
        setChartOptions(options);
    }, [labels, dataset, budget]);

    return (
        <div className="card">
            <Chart type="bar" data={chartData} options={chartOptions} />
        </div>
    );
}