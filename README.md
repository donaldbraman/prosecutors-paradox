# Overpolicing & Criminal History Simulation

An interactive web-based simulation demonstrating the cumulative impact of differential arrest rates and escalating sentencing policies over time. This visualization helps illustrate the potential disparate impacts of overpolicing on different populations.

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

## View the Simulation

You can view the simulation on GitHub Pages [here](https://donaldbraman.github.io/prosecutors-paradox/).

## Recent Changes

The webpage has been updated to be more compact in appearance, reducing the need for a wide screen and scrolling, while maintaining readability and intelligibility. The changes include:
- Reduced maximum width of the main container to 800px
- Changed layout of the parameters and visualization containers to a single column
- Reduced height of the chart container to 300px
- Reduced width of the parameters container to 100% and maximum width to 600px
- Reduced width and height of the grid elements to 200px each
- Reduced minimum width of the legend elements to 100px

## Automated Deployment Process

This project uses GitHub Actions to automate the deployment process. Whenever changes are pushed to the `main` branch, the workflow will automatically build the project and deploy it to the `gh-pages` branch.

### How to Trigger the Deployment

To trigger the deployment process, simply push your changes to the `main` branch. The GitHub Actions workflow will take care of the rest, ensuring that the `gh-pages` branch is updated with the latest version of the project.

### Creating a Personal Access Token (PAT)

To resolve the permission issues encountered during deployment, you need to create a Personal Access Token (PAT) with the necessary permissions:

1. Go to your GitHub account settings.
2. Navigate to "Developer settings" and then "Personal access tokens".
3. Click on "Generate new token".
4. Give your token a descriptive name, such as "GitHub Pages Deployment".
5. Select the necessary scopes for the token. At a minimum, you need to select:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
6. Click "Generate token" and copy the generated token. Make sure to store it securely as you won't be able to see it again.

### Storing the PAT as a Secret

Next, you need to store the PAT as a secret in your repository settings:

1. Go to your repository on GitHub.
2. Click on "Settings" and then "Secrets and variables" in the left sidebar.
3. Click on "New repository secret".
4. Name the secret `PERSONAL_ACCESS_TOKEN`.
5. Paste the PAT you generated earlier into the "Value" field.
6. Click "Add secret".
7. Ensure the `PERSONAL_ACCESS_TOKEN` secret is correctly set and accessible in the repository settings.

### Referencing the PAT in the Workflow File

Finally, update your workflow file to reference the PAT instead of the default `GITHUB_TOKEN`:

1. Open the `.github/workflows/deploy.yml` file in your repository.
2. Replace the `github_token` in the `Deploy to GitHub Pages` step with `personal_access_token`.
3. Reference the PAT secret in the `with` section of the `Deploy to GitHub Pages` step:

```yaml
with:
  personal_access_token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
  publish_dir: ./dist
```

### Verifying the PAT

To verify that the `PERSONAL_ACCESS_TOKEN` secret is correctly set and accessible in the repository settings, follow these steps:

1. Go to your repository on GitHub.
2. Click on "Settings" and then "Secrets and variables" in the left sidebar.
3. Ensure that the `PERSONAL_ACCESS_TOKEN` secret is listed and has the correct value.
4. If the secret is not listed or has an incorrect value, repeat the steps to create and store the PAT as a secret.
