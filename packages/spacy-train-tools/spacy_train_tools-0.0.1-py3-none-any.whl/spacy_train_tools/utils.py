import json
import logging
import re

import spacy
import unidecode
from spacy.tokens import DocBin
from spacy.tokens.doc import Doc


def remove_all_punc(text: str, replacement: str = '') -> str:
    punc = '''!()[]{};:'",<>.?@#$%^&*_~'''
    for ele in text:
        if ele in punc:
            text = text.replace(ele, replacement)

    return text


def load_cat_labels(from_file: str, cat_key: str = 'cats') -> list:
    all_labels = []
    with open(from_file, 'r', encoding='utf-8') as reader:
        for line in reader:
            text_json = json.loads(line)
            labels = text_json[cat_key]
            if labels is list:
                for label in labels:
                    if label not in all_labels:
                        all_labels.append(label)
            else:
                if labels not in all_labels:
                    all_labels.append(labels)

    return all_labels


def normalize_text(
        text: str,
        case_insensitive: bool,
        remove_accent: bool) -> list:
    def normalize_classify_text(name: str) -> str:
        cleaned_text = remove_all_punc(name, " ")
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        return cleaned_text

    s = text.strip()
    if remove_accent:
        s = unidecode.unidecode(s)

    if case_insensitive:
        s = s.lower()
    return [normalize_classify_text(s)]


def convert_to_spacy_doc_file(
        from_file: str,
        to_file: str,
        dataset_size: int = None,
        case_insensitive: bool = True,
        remove_accent: bool = False) -> str:
    binary_doc = create_spacy_doc(
        from_file,
        dataset_size=dataset_size,
        case_insensitive=case_insensitive,
        remove_accent=remove_accent,
        add_all_labels=True
    )
    binary_doc.to_disk(to_file)
    return to_file


def create_spacy_doc(
        from_file: str,
        cat_key: str = 'cats',
        entity_key: str = 'entities',
        dataset_size: int = None,
        case_insensitive: bool = True,
        remove_accent: bool = False,
        add_all_labels=True) -> DocBin:
    nlp = spacy.blank("en")

    train_doc_bin = DocBin()

    line_counter = 0
    doc_counter = 0
    entity_counter = 0
    skip_entity_counter = 0

    all_cat_set = load_cat_labels(from_file, cat_key=cat_key)

    with open(from_file, 'r', encoding='utf-8') as reader:
        for line in reader:
            text_json = json.loads(line)
            text = str(text_json['data'])

            cats = text_json[cat_key]
            entities = text_json[entity_key]

            text_list = normalize_text(text, case_insensitive, remove_accent)

            for cleaned_text in text_list:
                doc: Doc = nlp.make_doc(cleaned_text)

                if cats is not None:
                    apply_cats(doc, cats, all_cat_set if add_all_labels else None)
                if entities is not None:
                    num_entities, skip_entities = apply_entities(doc, entities)
                    entity_counter += num_entities
                    skip_entity_counter += skip_entities

                train_doc_bin.add(doc)
                doc_counter += 1

            line_counter += 1

            if dataset_size is not None and line_counter >= dataset_size:
                break

    logging.info(f'''
    Created binary doc from: {from_file}
    Line: {line_counter}
    Number of text: {doc_counter}
    Num of cats: {len(all_cat_set)} cats.
    Num of entities: {entity_counter} entities.
    Num of skip entities: {skip_entity_counter} entities.
    ''')
    return train_doc_bin


def apply_cats(doc: Doc, cats, all_cat_set: list = None):
    if all_cat_set is None:
        all_cat_set = []
    for label in all_cat_set:
        doc.cats[label] = 0
    if cats is list:
        for label in cats:
            doc.cats[label] = 1
    else:
        doc.cats[cats] = 1


def apply_entities(doc: Doc, entities) -> (int, int):
    entity_counter = 0
    skip_entity_counter = 0
    char_spans = []
    text = doc.text
    for start, end, label in entities:
        span = doc.char_span(start, end, label=label)
        if span is None:
            logging.info(f"Skipping entity: '{text[start:end]}'({start}:{end}) = {label} ")
            skip_entity_counter += 1
        else:
            char_spans.append(span)
            entity_counter += 1
    doc.ents = char_spans

    return entity_counter, skip_entity_counter
