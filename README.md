## Directory Descriptions

- **.rasa/cache/**: Contains cached data used by Rasa.
- **actions/**: Custom actions for your Rasa bot.
  - `__init__.py`: Initializes the actions module.
  - `actions.py`: Contains the implementation of custom actions.
- **data/**: Training data for the Rasa model.
  - `nlu.yml`: NLU training data.
  - `rules.yml`: Rules for dialogue management.
  - `stories.yml`: Stories for training the model.
- **models/**: Directory containing the trained models.
  - `20240911-025505-jovial-pixel.tar.gz`: A specific trained model file.
- **tests/**: Contains test files for validating the bot's behavior.
  - `test_stories.yml`: Test stories for ensuring the bot responds correctly.
- **config.yml**: Configuration file for Rasa.
- **credentials.yml**: Credentials for connecting to external services.
- **domain.yml**: Defines the domain of the assistant, including intents, entities, and responses.
- **endpoints.yml**: Configuration for external services and action servers.
- **update_rasa_from_excel.py**: A script to extract and update nlu.yml, domain.yml and stories.yml from an Excel file.

## Prerequisites

1. **Download C++ Redistributable**: You can download it from the official Microsoft website.

2. **Download and Install Anaconda**: Download Anaconda from the [official Anaconda website](https://www.anaconda.com/products/distribution) and follow the installation instructions for your operating system.

## Setting Up the Environment

1. **Create a New Anaconda Environment**:

   conda create -n install_demo python=3.8

2. **Activating the New Environment**:

   conda activate install_demo

3. **Uninstall Existing pip**:

   python -m pip uninstall pip

4. **Ensure pip is Installed**:

   python -m ensurepip

5. **Upgrade pip**:

   python -m pip install -U pip

6. **Install Rasa**:

   pip install rasa

7. **Running Rasa**:

   rasa shell
