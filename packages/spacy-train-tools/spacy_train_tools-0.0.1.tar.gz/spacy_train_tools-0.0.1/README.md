# Spacy train tools

## Install

- Run `pip install spacy-train-tools` or `pip3 install spacy-train-tools` to install this library

## Usage

```python
from src.spacy_train_tools.train import train_spacy_model

if __name__ == "__main__":
    train_spacy_model(
        config_file='./en_config.cfg',
        vector_file='en_core_web_lg',
        train_file='./data/train.jsonl',
        dev_file='./data/dev.jsonl',
        output_folder='./models'
    )

```