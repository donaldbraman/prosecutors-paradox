# Overpolicing & Criminal History Simulation

An interactive web-based simulation demonstrating the cumulative impact of differential arrest rates and escalating sentencing policies over time. This visualization helps illustrate the potential disparate impacts of overpolicing on different populations. You can view the simulation on GitHub Pages [here](https://donaldbraman.github.io/prosecutors-paradox/).


## Overview

This simulation allows users to explore how different arrest rates and sentencing policies can lead to cumulative differences in incarceration rates between populations over time. While simplified, it provides insights into how systemic differences in policing and sentencing can compound over years.

## Layout and Features

The webpage is organized into three main sections:

### 1. Parameter Controls
At the top of the page, users can adjust five key parameters:
- **White Arrest Rate** (0-100%): Probability of arrest per year for the white population engaging in some kind of illegal conduct.
- **Black Arrest Rate** (0-100%): Probability of arrest per year for the black population engaging in the same kind of illegal contact.
- **First Offense Sentence** (0-10 years): Average sentence length for first-time offenders
- **Second Offense Sentence** (0-10 years): Average sentence length for second-time offenders
- **Third+ Offense Sentence** (0-10 years): Average sentence length for third or more offenses

### 2. Population Visualization Grids
The main visualization area features two grid displays:
- **White Population Grid**: Shows arrest patterns for the white population
- **Black Population Grid**: Shows arrest patterns for the black population

Each grid represents 100 individuals (10x10) where:
- Individuals are represented by dots
- Dot size increases with number of arrests:
  - Small dot: 1 arrest
  - Medium dot: 2 arrests
  - Large dot: 3+ arrests
- Dot colors:
  - Blue dots: White population
  - Red dots: Black population

### 3. Cumulative Impact Chart
Below the grids, a line chart displays:
- The cumulative years sentenced over a 20-year simulation period
- Separate lines for white and black populations
- Interactive tooltips showing exact values at each year
- Y-axis showing total sentence years
- X-axis showing simulation years (1-20)

## How the Simulation Works

1. The simulation runs over a 20-year period
2. Each year:
   - The simulation identifies the pool of individuals not currently serving sentences
   - From this eligible pool, individuals are randomly selected for arrest based on the population's arrest rate
   - The arrest rate is applied to the number of eligible individuals (not incarcerated) rather than the total population
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

This simulation serves as an educational tool to visualize how seemingly small differences in arrest rates and sentencing policies can lead to significant disparities in cumulative incarceration rates between populations over time. It is intended to illustrate these effects conceptually rather than provide precise real-world predictions.
