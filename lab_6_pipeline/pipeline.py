"""
Pipeline for CONLL-U formatting
"""
from pathlib import Path
from typing import List
import re

from core_utils.article.article import SentenceProtocol, get_article_id_from_filepath
from core_utils.article.io import from_raw, to_cleaned, to_conllu
from core_utils.article.ud import OpencorporaTagProtocol, TagConverter
from core_utils.constants import ASSETS_PATH


class FileNotFoundError(Exception):
    """
    file does not exist
    """


class NotADirectoryError(Exception):
    """
    path does not lead to directory
    """


class InconsistentDatasetError(Exception):
    """
    IDs contain slips, number of meta and raw files is not equal, files are empty
    """


class EmptyDirectoryError(Exception):
    """
    directory is empty
    """


# pylint: disable=too-few-public-methods
class CorpusManager:
    """
    Works with articles and stores them
    """

    def __init__(self, path_to_raw_txt_data: Path):
        """
        Initializes CorpusManager
        """
        self.path_to_data = path_to_raw_txt_data
        self._storage = {}
        self._validate_dataset()
        self._scan_dataset()

    def _validate_dataset(self) -> None:
        """
        Validates folder with assets
        """
        if not self.path_to_data.exists():
            raise FileNotFoundError

        if not self.path_to_data.is_dir():
            raise NotADirectoryError

        if not any(self.path_to_data.iterdir()):
            raise EmptyDirectoryError

        raw_files = [file for file in self.path_to_data.glob('*_raw.txt')]
        # meta_files = [file for file in self.path_to_data.glob(r'*_meta.json')]

        # if len(meta_files) != len(raw_files):
        #     raise InconsistentDatasetError

        for file in raw_files:
            if not file.stat().st_size:
                raise InconsistentDatasetError

        list_of_ids = []
        for file in raw_files:
            list_of_ids.append(int(file.name[:file.name.index('_')]))
        if sorted(list_of_ids) != list(range(1, len(list_of_ids) + 1)):
            raise InconsistentDatasetError

    def _scan_dataset(self) -> None:
        """
        Register each dataset entry
        """
        raw_files = [i for i in self.path_to_data.glob('*_raw.txt')]
        for file in raw_files:
            article_id = get_article_id_from_filepath(file)
            self._storage[article_id] = from_raw(path=file)

    def get_articles(self) -> dict:
        """
        Returns storage params
        """
        return self._storage


class MorphologicalTokenDTO:
    """
    Stores morphological parameters for each token
    """

    def __init__(self, lemma: str = "", pos: str = "", tags: str = ""):
        """
        Initializes MorphologicalTokenDTO
        """


class ConlluToken:
    """
    Representation of the CONLL-U Token
    """

    def __init__(self, text: str):
        """
        Initializes ConlluToken
        """
        self._text = text

    def set_morphological_parameters(self, parameters: MorphologicalTokenDTO) -> None:
        """
        Stores the morphological parameters
        """

    def get_morphological_parameters(self) -> MorphologicalTokenDTO:
        """
        Returns morphological parameters from ConlluToken
        """

    def get_conllu_text(self, include_morphological_tags: bool) -> str:
        """
        String representation of the token for conllu files
        """

    def get_cleaned(self) -> str:
        """
        Returns lowercase original form of a token
        """
        text = self._text.lower()
        cleaned_text = re.sub(r'[^\w\s]', '', text)
        return cleaned_text


class ConlluSentence(SentenceProtocol):
    """
    Representation of a sentence in the CONLL-U format
    """

    def __init__(self, position: int, text: str, tokens: list[ConlluToken]):
        """
        Initializes ConlluSentence
        """
        self._position = position
        self._text = text
        self._tokens = tokens

    def get_conllu_text(self, include_morphological_tags: bool) -> str:
        """
        Creates string representation of the sentence
        """

    def get_cleaned_sentence(self) -> str:
        """
        Returns the lowercase representation of the sentence
        """
        sentence = ''
        for token in self._tokens:
            cleaned_token = token.get_cleaned()
            if cleaned_token:
                sentence += cleaned_token + ' '
        sentence = sentence.strip()
        return sentence

    def get_tokens(self) -> list[ConlluToken]:
        """
        Returns sentences from ConlluSentence
        """


class MystemTagConverter(TagConverter):
    """
    Mystem Tag Converter
    """

    def convert_morphological_tags(self, tags: str) -> str:  # type: ignore
        """
        Converts the Mystem tags into the UD format
        """

    def convert_pos(self, tags: str) -> str:  # type: ignore
        """
        Extracts and converts the POS from the Mystem tags into the UD format
        """


class OpenCorporaTagConverter(TagConverter):
    """
    OpenCorpora Tag Converter
    """

    def convert_pos(self, tags: OpencorporaTagProtocol) -> str:  # type: ignore
        """
        Extracts and converts POS from the OpenCorpora tags into the UD format
        """

    def convert_morphological_tags(self, tags: OpencorporaTagProtocol) -> str:  # type: ignore
        """
        Converts the OpenCorpora tags into the UD format
        """


class MorphologicalAnalysisPipeline:
    """
    Preprocesses and morphologically annotates sentences into the CONLL-U format
    """

    def __init__(self, corpus_manager: CorpusManager):
        """
        Initializes MorphologicalAnalysisPipeline
        """
        self._corpus = corpus_manager

    def _process(self, text: str) -> List[ConlluSentence]:
        """
        Returns the text representation as the list of ConlluSentence
        """
        conllu_sentences = []
        sentences = split_by_sentence(text)
        for position, sentence in enumerate(sentences):
            tokens = [ConlluToken(word.strip()) for word in sentence.split()]
            conllu_sentences.append(ConlluSentence(position, sentence, tokens))
        return conllu_sentences

    def run(self) -> None:
        """
        Performs basic preprocessing and writes processed text to files
        """
        for article in self._corpus.get_articles().values():
            sentences = self._process(article.text)
            article.set_conllu_sentences(sentences)
            to_cleaned(article)


class AdvancedMorphologicalAnalysisPipeline(MorphologicalAnalysisPipeline):
    """
    Preprocesses and morphologically annotates sentences into the CONLL-U format
    """

    def __init__(self, corpus_manager: CorpusManager):
        """
        Initializes MorphologicalAnalysisPipeline
        """

    def _process(self, text: str) -> List[ConlluSentence]:
        """
        Returns the text representation as the list of ConlluSentence
        """

    def run(self) -> None:
        """
        Performs basic preprocessing and writes processed text to files
        """


def main() -> None:
    """
    Entrypoint for pipeline module
    """
    corpus_manager = CorpusManager(ASSETS_PATH)
    pipeline = MorphologicalAnalysisPipeline(corpus_manager)
    pipeline.run()

if __name__ == "__main__":
    main()