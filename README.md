# Genetic Algorithm for Equipment Scheduling

This Python script implements a genetic algorithm to optimize the scheduling of laboratory equipment for various analyses. The goal is to minimize the total time and ensure the validity of the schedule according to the given constraints.

## Features

- **Random Individual Generation**: Creates a random schedule for the equipment.
- **Fitness Calculation**: Evaluates how good a schedule is based on total time and validity.
- **Mutation**: Introduces random changes to an individual's schedule.
- **Crossover**: Combines two individuals' schedules to create a new one.
- **Selection**: Chooses the best individuals from the population.
- **Tragedy Selection**: Applies a tragedy selection mechanism after a set number of iterations.
- **Validity Check**: Ensures the schedule adheres to the equipment usage restrictions.

## Parameters

- `TAXA_DE_MUTACAO`: Mutation rate (default 0.50).
- `TAXA_DE_CROSSOVER`: Crossover rate (default 0.20).
- `NUMERO_DE_INDIVIDUOS`: Number of individuals in the population (default 1000).
- `ITERACOES_PARA_TRAGEDIA`: Iterations before applying tragedy selection (default 1000).

## Data Structures

- `analises`: Dictionary mapping analyses to required equipment.
- `restricoes`: Dictionary mapping equipment to its usage limit.
- `dias`: List of weekdays.
- `horarios`: List of possible hours for scheduling.
- `dias_da_semana`: Dictionary mapping weekdays to numerical values.

## Usage

Run the script to start the genetic algorithm process. The algorithm will output the best schedule found and its fitness score.

## Requirements

- Python 3.12.5
- `random` module
- `math` module

## Contributors
- Henrique Marques
- Gabriel Reimberg
- Murilo Oliveira

## License

This project is open-sourced under the MIT license.

## Acknowledgments

This algorithm was inspired by the need for efficient scheduling in busy laboratories.

