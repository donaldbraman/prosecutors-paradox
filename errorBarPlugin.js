// Error bar plugin for Chart.js
const errorBarPlugin = {
    id: 'errorBar',
    afterDatasetsDraw(chart, args, options) {
        const {ctx, data, chartArea: {top, bottom, left, right}, scales: {x, y}} = chart;

        data.datasets.forEach((dataset, i) => {
            if (!dataset.errorBars) return;

            const meta = chart.getDatasetMeta(i);
            
            ctx.save();
            ctx.strokeStyle = dataset.errorBars.color;
            ctx.lineWidth = 2;

            meta.data.forEach((point, index) => {
                const value = dataset.data[index];
                const plus = dataset.errorBars.plus[index];
                const minus = dataset.errorBars.minus[index];

                const xPos = point.x;
                const yPos = point.y;
                const yHigh = y.getPixelForValue(value + plus);
                const yLow = y.getPixelForValue(value - minus);

                // Draw vertical line
                ctx.beginPath();
                ctx.moveTo(xPos, yHigh);
                ctx.lineTo(xPos, yLow);
                ctx.stroke();

                // Draw horizontal caps
                const capWidth = 4;
                ctx.beginPath();
                ctx.moveTo(xPos - capWidth, yHigh);
                ctx.lineTo(xPos + capWidth, yHigh);
                ctx.moveTo(xPos - capWidth, yLow);
                ctx.lineTo(xPos + capWidth, yLow);
                ctx.stroke();
            });
            
            ctx.restore();
        });
    }
};

// Register the plugin
Chart.register(errorBarPlugin);