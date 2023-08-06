from abc import ABC
from typing import Dict,List,Any,Tuple
import numpy as np

from nlp_tools.generators import  CorpusGenerator
from nlp_tools.types import TextSamplesVar



class MultipleProcessor(ABC):
    def to_dict(self) -> Dict[str, Any]:
        return {
            '__class_name__': self.__class__.__name__,
            '__module__': self.__class__.__module__,
        }

    def __init__(self,processors) -> None:
        self.processors = processors





    def build_vocab(self,
                    x_data: TextSamplesVar,
                    y_data: TextSamplesVar) -> None:
        corpus_gen = CorpusGenerator(x_data, y_data)
        self.build_vocab_generator([corpus_gen])

    def build_vocab_generator(self,
                              generators: List[CorpusGenerator]) -> None:
        raise NotImplementedError

    def get_tensor_shape(self, batch_size: int, seq_length: int) -> Tuple:
        return batch_size, seq_length

    def transform(self,samples,seq_length = None):
        raise NotImplementedError

    def inverse_transform(self,
                          labels,
                          lengths = None,
                          mapping_list=None,
                          threshold= 0.5) :
        raise NotImplementedError

    def smooth_labels(self,labels, factor=0.1):
        # smooth the labels
        labels *= (1 - factor)
        labels += (factor / labels.shape[1])

        # returned the smoothed labels
        return labels



