 conversion appropriate suggested that she may have written this reasonably forceful that's a little bit surprising court order in order to get the attention. The attorney general and say look at this whether pursuing litigation could be could be submitted staffing or both and it seems like there's options to hire some experts that should be cheaper. They just might not hav, but I think Elon Musk revealed so far they might not feel like to pursue this grant in California has been mostly disputes like government.# Overpolicing & Criminal History Simulation

An interactive web-based simulation demonstrating the cumulative impact of differential arrest rates and escalating sentencing policies over time. This visualization helps illustrate the potential disparate impacts of overpolicing on different cohorts. You can view the simulation on GitHub Pages [here](https://donaldbraman.github.io/prosecutors-paradox/).


## Overview

This simulation allows users to explore how different arrest rates and sentencing policies can lead to cumulative differences in incarceration rates between cohorts over time. While simplified, it provides insights into how systemic differences in policing and sentencing can compound over years.

## Layout and Features

The webpage is organized into three main sections:

### 1. Parameter Controls
At the top of the page, users can adjust five key parameters:
- **Comparison Arrest Rate** (0-100%): Probability of arrest per year for the comparison cohort engaging in some kind of illegal conduct.
- **Target Arrest Rate** (0-100%): Probability of arrest per year for the target cohort engaging in the same kind of illegal contact.
- **First Offense Sentence** (0-10 years): Average sentence length for first-time offenders
- **Second Offense Sentence** (0-10 years): Average sentence length for second-time offenders
- **Third+ Offense Sentence** (0-10 years): Average sentence length for third or more offenses

### 2. Population Visualization Grids
The main visualization area features two grid displays:
- **Comparison Cohort Grid**: Shows arrest patterns for the comparison cohort
- **Target Cohort Grid**: Shows arrest patterns for the target cohort

Each grid represents 100 individuals (10x10) where:
- Individuals are represented by dots
- Dot size increases with number of arrests:
  - Small dot: 1 arrest
  - Medium dot: 2 arrests
  - Large dot: 3+ arrests
- Dot colors:
  - Blue dots: Comparison cohort
  - Red dots: Target cohort

### 3. Cumulative Impact Chart
Below the grids, a line chart displays:
- The cumulative years sentenced over a 20-year simulation period
- Separate lines for comparison and target cohorts
- Interactive tooltips showing exact values at each year
- Y-axis showing total sentence years
- X-axis showing simulation years (1-20)

## How the Simulation Works

1. The simulation runs over a 20-year period
2. Each year:
   - The simulation identifies the pool of individuals not currently serving sentences
   - From this eligible pool, individuals are randomly selected for arrest based on the cohort's arrest rate
   - The arrest rate is applied to the number of eligible individuals (not incarcerated) rather than the total cohort
   - When arrested:
     * Individuals receive sentences based on their arrest history
     * They are removed from the eligible pool for the duration of their sentence
     * Once their sentence is complete (counted down year by year), they automatically return to the eligible pool
   - This ensures that incarcerated individuals cannot be arrested again until they have completed their sentence
3. The visualization updates to show:
   - Growing dot sizes for repeat arrests
   - Cumulative sentenced years in the line chart

## Technical Details

- Built with vanilla JavaScript and HTML5 Canvas
- Uses Chart.js for data visualization
- Designed to be hostable on GitHub Pages
- Optimized for simplicity and maintainability

## Purpose

This simulation serves as an educational tool to visualize how seemingly small differences in arrest rates and sentencing policies can lead to significant disparities in cumulative incarceration rates between cohorts over time. It is intended to illustrate these effects conceptually rather than provide precise real-world predictions.
