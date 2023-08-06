import logging
import os
from pathlib import Path
from uuid import uuid1

from py_profiler import profiler, profiling_service

from src.spacy_train_tools.command_line import run_command_line
from src.spacy_train_tools.utils import convert_to_spacy_doc_file


@profiler("train_spacy_model")
def train_spacy_model(
        config_file: str,
        vector_file: str,
        train_file: str,
        dev_file: str,
        output_folder: str
):
    tmp_train_file = f'{Path(train_file).parent.absolute()}/{uuid1()}.spacy'
    tmp_dev_file = f'{Path(dev_file).parent.absolute()}/{uuid1()}.spacy'
    try:

        tmp_train_file = convert_to_spacy_doc_file(
            train_file,
            tmp_train_file,
            dataset_size=None,
            case_insensitive=True,
            remove_accent=False
        )

        tmp_dev_file = convert_to_spacy_doc_file(
            dev_file,
            tmp_dev_file,
            dataset_size=None,
            case_insensitive=True,
            remove_accent=False
        )

        run_command_line([
            'python3',
            '-m',
            'spacy',
            'train',
            config_file,
            '--output',
            output_folder,
            '--paths.train', tmp_train_file,
            '--paths.dev', tmp_dev_file,
            '--paths.vectors', vector_file
        ])
    except Exception as ex:
        logging.error(ex)
    finally:
        os.remove(tmp_train_file)
        os.remove(tmp_dev_file)

    logging.info(profiling_service.as_table())
    logging.info(f'Output model: {output_folder}')
