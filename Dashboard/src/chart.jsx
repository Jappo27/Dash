import React, { useState, useEffect } from 'react';
import { Chart } from 'primereact/chart';
import { elements } from 'chart.js';

export default function DoughnutChartDemo({correct, incorrect, unattempted}) {
    const [chartData, setChartData] = useState({});
    const [chartOptions, setChartOptions] = useState({});

    useEffect(() => {
        const documentStyle = getComputedStyle(document.documentElement);
        const data = {
            labels: ['Correct', 'Incorrect', 'Unattempted'],
            datasets: [
                {
                    data: [correct, incorrect, unattempted],
                    backgroundColor: [
                        '#436ff4',
                        '#f0598b',
                        '#f47348'
                    ],
                    hoverBackgroundColor: [
                        '#436ff480',
                        '#f0598b80',
                        '#f4734880'
                    ]

                }
            ]
        };
        const options = {
            cutout: '50%',
            elements: {
                arc: {
                    borderWidth:0,
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#FFFFFF',
                    }
                }
            },
        };

        setChartData(data);
        setChartOptions(options);
    }, [correct, incorrect, unattempted]);

    return (
        <div className="card flex justify-content-center">
            <Chart type="doughnut" data={chartData} options={chartOptions} className="w-full md:w-30rem" />
        </div>
    );
}