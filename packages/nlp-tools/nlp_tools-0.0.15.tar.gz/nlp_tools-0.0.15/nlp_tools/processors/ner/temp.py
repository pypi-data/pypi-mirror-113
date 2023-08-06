# encoding: utf-8
from typing import Dict, List, Any, Union

import numpy as np
import tqdm

from nlp_tools.processors.abc_label_processor import ABCLabelProcessor
from nlp_tools.utils.ner_utils import get_entities
from nlp_tools.utils.ner_utils import span_extract_item,span_extract_item_no_hu
from tensorflow.keras.utils import to_categorical


class TempSentenceLabelProcessor(ABCLabelProcessor):
    """
    Generic processors for the sequence samples.
    """

    def to_dict(self) -> Dict[str, Any]:
        data = super(TempSentenceLabelProcessor, self).to_dict()
        data['config'].update({
            'embedding_max_position': self.embedding_max_position,
            'max_sentence_length':self.max_sentence_length,
        })
        return data

    def __init__(self,
                 return_one_hot=True,
                 **kwargs: Any) -> None:
        """

        Args:
            vocab_dict_type: initial vocab dict type, one of `text` `labeling`.
            **kwargs:
        """
        super(TempSentenceLabelProcessor, self).__init__(**kwargs)
        self._initial_vocab_dic = {
            "O": 0
        }
        self.return_one_hot = return_one_hot


    def update_length_info(self,embedding_max_position=None,max_sentence_length=None):
        self.embedding_max_position = embedding_max_position
        self.max_sentence_length = max_sentence_length

    def build_vocab_generator(self,generators) -> None:
        if not self.vocab2idx:
            tag_set = set()
            vocab2idx = self._initial_vocab_dic
            for gen in generators:
                for (_, label_list) in tqdm.tqdm(gen.sample(), desc="Preparing label dict"):
                    ## ner任务下面，label 应该是一个list
                    assert type(label_list) == list
                    for sublabel in label_list:
                        label = sublabel[2]
                        if label not in tag_set:
                            tag_set.add(label)


            for label in list(set(tag_set)):
                vocab2idx[label] = len(vocab2idx)

            self.vocab2idx = vocab2idx
            self.idx2vocab = dict([(v, k) for k, v in self.vocab2idx.items()])




    def transform(self,samples,seq_length):
        if not seq_length:
            seq_length = self.max_sentence_length

        if not seq_length:
            seq_length = self.embedding_max_position

        if self.embedding_max_position is not None and self.embedding_max_position < seq_length:
            seq_length = self.embedding_max_position

        labels_start = np.zeros((len(samples), seq_length))
        labels_end = np.zeros((len(samples), seq_length))

        for index, sample_labels in enumerate(samples):
            for sub_label in sample_labels:
                (start_position, end_position, label_type) = sub_label
                if start_position >= seq_length:
                    continue

                if end_position >= seq_length:
                    continue

                labels_start[index, start_position] = self.vocab2idx[label_type]
                labels_end[index,end_position] = self.vocab2idx[label_type]

        if self.return_one_hot:
            labels_start = to_categorical(labels_start,num_classes=self.vocab_size)
            labels_end = to_categorical(labels_end, num_classes=self.vocab_size)
            labels_start = self.smooth_labels(labels_start)
            labels_end = self.smooth_labels(labels_end)


        gloabl_labels = self.global_transform(samples,seq_length)

        return (labels_start,labels_end,gloabl_labels)

    def global_transform(self,samples,seq_length=None) -> np.ndarray:
        if not seq_length:
            seq_length = self.max_sentence_length

        if not seq_length:
            seq_length = self.embedding_max_position

        if self.embedding_max_position is not None and self.embedding_max_position < seq_length:
            seq_length = self.embedding_max_position

        labels_numpy = np.zeros((len(samples),len(self.vocab2idx), seq_length, seq_length))
        for index, sample_labels in enumerate(samples):
            for sub_label in sample_labels:
                (start_position, end_position, label_type) = sub_label
                label2index = self.vocab2idx[label_type]

                if start_position >= seq_length:
                    continue

                if end_position >= seq_length:
                    continue

                labels_numpy[index,label2index,start_position,end_position] = 1
        return labels_numpy

    def inverse_transform(self,
                          labels: Union[List[List[int]], np.ndarray],
                          lengths: List[int] = None,
                          mapping_list=None, **kwargs):
        span_result = self.span_inverse_transform([labels[0],labels[1]],lengths,None,**kwargs)
        glabal_result = self.glabal_inverse_transform(labels[2],lengths,mapping_list,**kwargs)


        result = []
        for span_label,glabal_label,length in zip(span_result,glabal_result,lengths):
            same_entity = [i for i in span_label if i in glabal_label]

            no_use_entity = [i for i in span_label if i not in same_entity] + [i for i in glabal_label if i not in same_entity]

            same_entity_sort = sorted(same_entity,key=lambda x:x[1])

            filter_same_entity = []
            current_end = -1
            for i in range(len(same_entity) -1):
                if same_entity_sort[i][1] <= current_end :
                    continue
                for j in range(i,len(same_entity)):

                    if same_entity_sort[i][2] >= same_entity_sort[j][1]:
                        if same_entity_sort[i][2] >= same_entity_sort[j][2]:
                            filter_same_entity.append(same_entity_sort[i])

                    else:
                        filter_same_entity.append(same_entity_sort[i])

                current_end = same_entity_sort[i][2]

            no_use_entity.extend([i for i in same_entity_sort if i not in filter_same_entity])

            tags = ['O' for _ in range(length)]
            for (start,end,label) in filter_same_entity:
                tags[start] = 'B-'+ label
                for idx_ in range(start+1,end+1):
                    tags[idx_] = "I-" + label
















    def span_inverse_transform(self,
                          labels: Union[List[List[int]], np.ndarray],
                          lengths: List[int] = None,
                          mapping_list = None,**kwargs ):
        result = []
        for index, (labels_start,labels_end, sequece_length) in enumerate(zip(labels[0],labels[1], lengths)):


            labels_start = labels_start[:sequece_length]
            labels_end = labels_end[:sequece_length]
            if len(np.shape(labels_start)) == 2:
                labels_start = np.argmax(labels_start,axis=-1)
                labels_end = np.argmax(labels_end, axis=-1)


            # 将position映射为真实的句子中的index，因为之前由于分词以后，会影响index
            format_entities = []

            entities = span_extract_item(labels_start,labels_end)
            for (tag_index,start,end) in entities:
                tagname = self.idx2vocab[tag_index]
                if mapping_list:
                    if mapping_list[index][start] and mapping_list[index][end]:
                        format_entities.append((mapping_list[index][start][0], mapping_list[index][end][-1], tagname))
                else:
                    format_entities.append((start , end , tagname))

            result.append(format_entities)
        return result


    def glabal_inverse_transform(self, labels, lengths=None, mapping_list=None, threshold=0, return_max_entity=False):
        result = []
        if return_max_entity:
            for index,(scores ,sequece_length )in enumerate(zip(labels,lengths)):
                entities = []
                scores = scores[:,:sequece_length,:sequece_length]
                scores[:, [0, -1]] -= np.inf  # 去除添加的[cls]和【seq】这一行的判断
                scores[ :, :, [0, -1]] -= np.inf  # 去除每一行的首尾添加的[cls]和【seq】
                scores = np.transpose(scores,[1,2,0])
                max_scores = np.max(scores,axis=-1)
                for (start,end,l) in zip(*np.where(scores > threshold)):
                    if max_scores[start, end] == scores[start, end, l]:
                        if mapping_list:
                            entities.append(
                                (mapping_list[index][start][0], mapping_list[index][end][-1], self.idx2vocab[l])
                            )
                        else:
                            # 如果mapping为空，start,end都要减一，因为在tokenizer的时候增加了[cls]，所以这边位置要减1
                            entities.append(
                                (start , end , self.idx2vocab[l])
                            )
                result.append(entities)

        else:
            for index,(scores ,sequece_length )in enumerate(zip(labels,lengths)):
                entities = []
                scores = scores[:,:sequece_length,:sequece_length]
                scores[:, [0, -1]] -= np.inf  # 去除添加的[cls]和【seq】这一行的判断
                scores[ :, :, [0, -1]] -= np.inf  # 去除每一行的首尾添加的[cls]和【seq】
                for l, start, end in zip(*np.where(scores > threshold)):
                    if mapping_list:
                        entities.append(
                            (mapping_list[index][start][0], mapping_list[index][end][-1], self.idx2vocab[l])
                        )
                    else:
                        # 如果mapping为空，start,end都要减一，因为在tokenizer的时候增加了[cls]，所以这边位置要减1
                        entities.append(
                            (start , end , self.idx2vocab[l])
                        )
                result.append(entities)
        return result





if __name__ == "__main__":
    pass
