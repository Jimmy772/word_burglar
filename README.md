# Word Buglar

## Overview

The project is a versatile program designed to interact with a PostgreSQL database, extracting valuable information about books within the dataset. Leveraging natural language processing capabilities, users can seamlessly query the extensive database.

## Features

1. **Natural Language Querying:**
   - Harness the power of natural language to query the database effortlessly.

2. **Similarity Search:**
   - Conduct similarity searches based on user input and book descriptions, facilitating intuitive exploration of related literature.

3. **Under-the-Hood Technology:**
   - Utilizes Python for dataset preparation.
   - PostgreSQL stores the data efficiently.
   - pgvector stores vector representations of book descriptions.
   - RASA transforms user natural language inputs into precise PostgreSQL queries.

## Usage Examples

Explore the program's capabilities through [examples and showcases](#) to understand its potential.

## Dependencies

Ensure you have the necessary dependencies installed. Check the `requirements.txt` file and refer to the `environments.yml` in the chat folder for specific details.

## Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── chat 
    │   ├── actions        <- Data from third party sources.
    |       └── actions.py <- Custom code for handling actions in response to user inputs. 
    │   ├── data  
    |       ├── nlu.yml    <- Examples fot training NLU model.
    |       ├── rules.yml  <- Specifies rules for dialogue management.
    |       └── stories.yml<- Defies example dialogues for training dialogue model.         
    │   ├── models         <- models created when training RASA chatbot.
    │   ├── tests          <- Evaluate that chatbot behaves as expected.
    │   ├── config.yml     <- Configure the pipline and training settings for NLU and dialogue management.
    │   ├── credentials.yml<- Configure authentication  details for external services.
    │   ├── domain.yml     <- Specifying chatbot's configuration details.
    |   ├── endpoints.yml
    │   └── environments.yml<- packages required to run and train RASA chatbot.  
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
