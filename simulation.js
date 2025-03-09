const comparisonRateInput = document.getElementById('comparison_rate');
const targetRateInput = document.getElementById('target_rate');
const avgFirstInput = document.getElementById('avg_first');
const avgSecondInput = document.getElementById('avg_second');
const avgThirdInput = document.getElementById('avg_third');
const runSimulationButton = document.getElementById('run_simulation');
const comparisonGrid = document.getElementById('comparison_grid');
const targetGrid = document.getElementById('target_grid');

// Chart Elements
const singleChartCanvas = document.getElementById('single_sim_chart');
const multipleChartCanvas = document.getElementById('multiple_sims_chart');
const singleChartCtx = singleChartCanvas.getContext('2d');
const multipleChartCtx = multipleChartCanvas.getContext('2d');

// State Variables
const gridSize = 10;
let comparisonPeople = [];
let targetPeople = [];
let singleChart;
let multipleChart;

// Input validation
function validateInputs() {
    const inputs = [comparisonRateInput, targetRateInput, avgFirstInput, avgSecondInput, avgThirdInput];
    let isValid = true;
    inputs.forEach(input => {
        const value = parseFloat(input.value);
        if (input.id.includes('rate')) {
            if (value < 0 || value > 100) {
                input.style.borderColor = 'red';
                isValid = false;
            } else {
                input.style.borderColor = '#ccc';
            }
        } else {
            if (value < 0 || value > 10) {
                input.style.borderColor = 'red';
                isValid = false;
            } else {
                input.style.borderColor = '#ccc';
            }
        }
    });
    return isValid;
}

function initializePeople() {
    comparisonPeople = Array.from({ length: gridSize * gridSize }, () => ({ 
        arrests: 0, 
        sentenceServed: 0, 
        sentenceRemaining: 0,
        x: Math.random(),
        y: Math.random()
    }));
    targetPeople = Array.from({ length: gridSize * gridSize }, () => ({ 
        arrests: 0, 
        sentenceServed: 0, 
        sentenceRemaining: 0,
        x: Math.random(),
        y: Math.random()
    }));
}

function drawGrid(gridElement, people, isComparison) {
    gridElement.innerHTML = '';
    people.forEach(person => {
        if (person.arrests > 0) {
            const dot = document.createElement('div');
            dot.className = `dot ${isComparison ? 'comparison-dot' : 'target-dot'}`;
            const baseSize = 8;
            const dotSize = baseSize + (person.arrests - 1) * 4;
            dot.style.width = `${dotSize}px`;
            dot.style.height = `${dotSize}px`;
            dot.style.left = `${person.x * 100}%`;
            dot.style.top = `${person.y * 100}%`;
            gridElement.appendChild(dot);
        }
    });
}

function getSentence(arrestCount) {
    const avgFirst = parseFloat(avgFirstInput.value);
    const avgSecond = parseFloat(avgSecondInput.value);
    const avgThird = parseFloat(avgThirdInput.value);
    if (arrestCount === 1) return avgFirst;
    if (arrestCount === 2) return avgSecond;
    return avgThird;
}

function simulateArrests(people, arrestRate) {
    const eligiblePeople = people.filter(person => person.sentenceRemaining <= 0);
    const totalEligible = eligiblePeople.length;
    const expectedArrests = Math.round(totalEligible * arrestRate);
    
    for (let i = 0; i < expectedArrests; i++) {
        if (eligiblePeople.length === 0) break;
        
        const randomIndex = Math.floor(Math.random() * eligiblePeople.length);
        const selectedPerson = eligiblePeople[randomIndex];
        
        selectedPerson.arrests++;
        const sentence = getSentence(selectedPerson.arrests);
        selectedPerson.sentenceRemaining = sentence;
        
        eligiblePeople.splice(randomIndex, 1);
    }
}

function updateSentences(people) {
    people.forEach(person => {
        if (person.sentenceRemaining > 0) {
            person.sentenceServed++;
            person.sentenceRemaining--;
        }
    });
}

function getChartOptions(titleText) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            intersect: false,
            mode: 'index'
        },
        plugins: {
            title: {
                display: true,
                display: false,
                text: titleText,
                font: {
                    size: 18,
                    weight: '600',
                    family: "'Arial', 'Helvetica Neue', sans-serif"
                },
                color: '#2c3e50'
            },
            legend: {
                position: 'top', 
                align: 'center',
                labels: {
                    padding: 8,
                    usePointStyle: true, 
                    pointStyle: 'circle',
                    font: {
                        size: 13,
                        family: "'Arial', 'Helvetica Neue', sans-serif"
                    },
                    generateLabels: function(chart) {
                        // This ensures the legend items maintain their horizontal layout
                        return Chart.defaults.plugins.legend.labels.generateLabels(chart);
                    },
                    boxWidth: 8,
                    boxHeight: 8,
                    color: '#2c3e50'
                }
            },
            tooltip: {
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                titleColor: '#2c3e50',
                titleFont: {
                    size: 14,
                    weight: '600',
                    family: "'Arial', 'Helvetica Neue', sans-serif"
                },
                bodyColor: '#34495e',
                bodyFont: {
                    size: 13,
                    family: "'Arial', 'Helvetica Neue', sans-serif"
                },
                borderColor: 'rgba(0,0,0,0.1)',
                borderWidth: 1,
                padding: 12,
                cornerRadius: 6,
                displayColors: true,
                boxWidth: 8,
                boxHeight: 8,
                callbacks: {
                    label: (context) => {
                        const dataset = context.dataset;
                        const value = context.parsed.y;
                        let label = `${dataset.label}: ${value.toFixed(1)} years`;
                        
                        if (dataset.errorBars && dataset.errorBars.plus) {
                            const stdDev = dataset.errorBars.plus[context.dataIndex];
                            if (stdDev > 0) {
                                label += ` ±${stdDev.toFixed(1)}`;
                            }
                        }
                        
                        return label;
                    }
                }
            }
        },
        // Add layout configuration to properly position elements
        layout: {
            padding: {
                // Add padding at the top for the legend
                top: 10,
                bottom: 20,
                left: 15,
                right: 0
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Cumulative Sentence Years',
                    padding: {top: 5, bottom: 5},
                    font: {
                        size: 14,
                        weight: '600',
                        family: "'Arial', 'Helvetica Neue', sans-serif"
                    },
                    color: '#2c3e50'
                },
                ticks: {
                    font: {
                        size: 12,
                        family: "'Arial', 'Helvetica Neue', sans-serif"
                    },
                    color: '#34495e',
                    padding: 5
                },
                grid: {
                    color: 'rgba(0,0,0,0.05)',
                    drawBorder: false
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Simulation Year',
                    padding: {top: 5, bottom: 5},
                    font: {
                        size: 14,
                        weight: '600',
                        family: "'Arial', 'Helvetica Neue', sans-serif"
                    },
                    color: '#2c3e50'
                },
                ticks: {
                    font: {
                        size: 12,
                        family: "'Arial', 'Helvetica Neue', sans-serif"
                    },
                    color: '#34495e',
                    padding: 5
                },
                grid: {
                    color: 'rgba(0,0,0,0.05)',
                    drawBorder: false
                }
            }
        }
    };
}

function runSimulation() {
    if (!validateInputs()) {
        alert('Please check input values. Arrest rates must be between 0-100%, sentences between 0-10 years.');
        return;
    }

    initializePeople();
    const comparisonRate = parseFloat(comparisonRateInput.value) / 100;
    const targetRate = parseFloat(targetRateInput.value) / 100;
    let comparisonCumulativeSentences = [];
    let targetCumulativeSentences = [];

    for (let year = 0; year < 20; year++) {
        simulateArrests(comparisonPeople, comparisonRate);
        simulateArrests(targetPeople, targetRate);
        updateSentences(comparisonPeople);
        updateSentences(targetPeople);

        const totalComparisonSentences = comparisonPeople.reduce((sum, person) => sum + person.sentenceServed, 0);
        const totalTargetSentences = targetPeople.reduce((sum, person) => sum + person.sentenceServed, 0);
        comparisonCumulativeSentences.push(totalComparisonSentences);
        targetCumulativeSentences.push(totalTargetSentences);

        drawGrid(comparisonGrid, comparisonPeople, true);
        drawGrid(targetGrid, targetPeople, false);
    }

    renderSingleSimChart(comparisonCumulativeSentences, targetCumulativeSentences);
}

function renderSingleSimChart(comparisonData, targetData) {
    if (singleChart) {
        singleChart.destroy();
    }

    const labels = Array.from({ length: 20 }, (_, i) => `Year ${i + 1}`);
    
    singleChart = new Chart(singleChartCtx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Targeted Cohort',
                data: targetData,
                borderColor: '#D32F2F',
                borderWidth: 2.5,
                tension: 0.3,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: '#D32F2F',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverBackgroundColor: '#D32F2F',
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 2,
                fill: false
            }, {
                label: 'Comparison Cohort',
                data: comparisonData,
                borderColor: '#1976D2',
                borderWidth: 2.5,
                tension: 0.3,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: '#1976D2',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverBackgroundColor: '#1976D2',
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 2,
                fill: false
            }]
        },
        options: getChartOptions('Single Simulation Results')
    });
}

function calculateStats(simulations) {
    const timePoints = simulations[0].length;
    const means = Array(timePoints).fill(0);
    const stdDevs = Array(timePoints).fill(0);
    
    // Calculate means for each time point
    for (let t = 0; t < timePoints; t++) {
        means[t] = simulations.reduce((sum, sim) => sum + sim[t], 0) / simulations.length;
    }
    
    // Calculate standard deviations for each time point
    for (let t = 0; t < timePoints; t++) {
        const squaredDiffs = simulations.map(sim => Math.pow(sim[t] - means[t], 2));
        const variance = squaredDiffs.reduce((sum, diff) => sum + diff, 0) / simulations.length;
        stdDevs[t] = Math.sqrt(variance);
    }
    
    return { means, stdDevs };
}

function runMultipleSimulations() {
    if (!validateInputs()) {
        alert('Please check input values. Arrest rates must be between 0-100%, sentences between 0-10 years.');
        return;
    }

    const numSimulations = 10000;
    const comparisonSimulations = [];
    const targetSimulations = [];

    for (let i = 0; i < numSimulations; i++) {
        initializePeople();
        const comparisonRate = parseFloat(comparisonRateInput.value) / 100;
        const targetRate = parseFloat(targetRateInput.value) / 100;
        let comparisonCumulativeSentences = [];
        let targetCumulativeSentences = [];

        for (let year = 0; year < 20; year++) {
            simulateArrests(comparisonPeople, comparisonRate);
            simulateArrests(targetPeople, targetRate);
            updateSentences(comparisonPeople);
            updateSentences(targetPeople);

            const totalComparisonSentences = comparisonPeople.reduce((sum, person) => sum + person.sentenceServed, 0);
            const totalTargetSentences = targetPeople.reduce((sum, person) => sum + person.sentenceServed, 0);
            comparisonCumulativeSentences.push(totalComparisonSentences);
            targetCumulativeSentences.push(totalTargetSentences);
        }

        comparisonSimulations.push(comparisonCumulativeSentences);
        targetSimulations.push(targetCumulativeSentences);
    }

    const comparisonStats = calculateStats(comparisonSimulations);
    const targetStats = calculateStats(targetSimulations);

    renderMultipleSimsChart(comparisonStats, targetStats);
}

// Define custom plugin for ratio text
const ratioTextPlugin = {
    id: 'ratioText',
    beforeDraw: (chart, args, options) => {
        const {ctx, chartArea: {left, top, right, bottom}} = chart;
        
        if (!options.text) return;
        
        // Save context state
        ctx.save();
        
        // Set text style
        ctx.font = '16px Arial, "Helvetica Neue", sans-serif';
        ctx.fillStyle = '#2c3e50';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'top';
        
        // Calculate position (5% from left, 5% from top)
        const x = left + (right - left) * 0.05;
        const y = top + (bottom - top) * 0.05;
        
        // Draw background
        const textLines = options.text.split('\n');
        const lineHeight = 28;
        const padding = 20;
        const textWidth = Math.max(...textLines.map(line => ctx.measureText(line).width));
        
        ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
        ctx.fillRect(
            x - padding,
            y - padding,
            textWidth + padding * 2,
            (textLines.length * lineHeight) + padding * 2
        );
        
        // Draw text
        ctx.fillStyle = '#2c3e50';
        textLines.forEach((line, i) => {
            ctx.fillText(line, x, y + (i * lineHeight));
        });
        
        // Restore context state
        ctx.restore();
    }
};

// Register the plugin
Chart.register(ratioTextPlugin);

function renderMultipleSimsChart(comparisonStats, targetStats) {
    if (multipleChart) {
        multipleChart.destroy();
    }

    const labels = Array.from({ length: 20 }, (_, i) => `Year ${i + 1}`);
    
    // Calculate target-to-comparison ratio at year 20
    const targetToComparisonRatio = targetStats.means[19] / comparisonStats.means[19];
    const ratioText = `For every year that people in the comparison cohort\nare incarcerated for criminal conduct, people in the\ntargeted cohort engaging in the same conduct\nspend ${targetToComparisonRatio.toFixed(1)} years incarcerated.`;
    
    multipleChart = new Chart(multipleChartCtx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Targeted Cohort',
                data: targetStats.means,
                borderColor: '#D32F2F',
                borderWidth: 2.5,
                tension: 0.3,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: '#D32F2F',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverBackgroundColor: '#D32F2F',
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 2,
                fill: false,
                errorBars: {
                    plus: targetStats.stdDevs,
                    minus: targetStats.stdDevs,
                    color: 'rgba(211, 47, 47, 0.3)'
                }
            }, {
                label: 'Comparison Cohort',
                data: comparisonStats.means,
                borderColor: '#1976D2',
                borderWidth: 2.5,
                tension: 0.3,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: '#1976D2',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#1976D2',
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 2,
                fill: false,
                errorBars: {
                    plus: comparisonStats.stdDevs,
                    minus: comparisonStats.stdDevs,
                    color: 'rgba(25, 118, 210, 0.3)'
                }
            }]
        },
        options: {
            ...getChartOptions('Multiple Simulations Results (with Standard Deviation)'),
            plugins: {
                ...getChartOptions('').plugins,
                ratioText: {
                    text: ratioText
                }
            }
        }
    });
}

// Add event listeners
runSimulationButton.addEventListener('click', () => {
    runSimulation();
    drawGrid(comparisonGrid, comparisonPeople, true);
    drawGrid(targetGrid, targetPeople, false);
});

document.getElementById('run_multiple_simulations').addEventListener('click', () => {
    runMultipleSimulations();
});

// Initialize with single simulation
runSimulation();
