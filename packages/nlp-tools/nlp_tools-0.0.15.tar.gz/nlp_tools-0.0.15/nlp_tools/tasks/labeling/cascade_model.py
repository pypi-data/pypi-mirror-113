from typing import Dict, Any

from tensorflow import keras
import tensorflow as tf
import numpy as np

from nlp_tools.layers import L, KConditionalRandomField
from nlp_tools.tasks.labeling.abc_model import ABCLabelingModel
from nlp_tools.logger import logger
from nlp_tools.layers.pool_layer import PoolerInputLayer

from tensorflow.keras.metrics import sparse_categorical_accuracy
from nlp_tools.layers.non_masking_layer import MaskingSaverLayer





class Cascade_Model(ABCLabelingModel):

    @classmethod
    def default_hyper_parameters(cls) -> Dict[str, Dict[str, Any]]:
        return {
            'layer_blstm': {
                'units': 64,
                'return_sequences': True
            },
            'layer_dropout': {
                'rate': 0.5
            },
            'layer_time_distributed': {},
        }



    def build_model_arc(self) -> None:

        segment_output_dim = len(self.label_processor.segmetn_idx_2_label.items())

        label_output_dim = self.label_processor.vocab_size
        self.mask_save_layer = MaskingSaverLayer()

        config = self.hyper_parameters
        embed_model = self.embedding.embed_model



        crf = KConditionalRandomField()
        layer_stack = [
            L.Bidirectional(L.LSTM(**config['layer_blstm']), name='layer_blstm'),
            L.Dropout(**config['layer_dropout'], name='layer_dropout'),
        ]

        tensor = embed_model.output
        # for layer in layer_stack:
        #     tensor = layer(tensor)
        tensor = self.mask_save_layer(tensor)


        # crf层输出
        segment_output = L.Dense(128,activation='tanh')(tensor)
        segment_output = L.Dense(segment_output_dim, **config['layer_time_distributed'])(segment_output)
        crf_output = crf(segment_output)





        # label predict输出
        #predict_label_embedding = L.Dense(64)(crf_output)
        #logit_classify = embed_model.output
        # for layer in layer_stack:
        #     logit_classify = layer(logit_classify)
        from bert4keras.layers import LayerNormalization

        output = self.embedding.embed_model.layers[-2].get_output_at(-1)

        #logits_label = LayerNormalization(conditional=True)([output, crf_output])

        logits_label = PoolerInputLayer(128,label_output_dim)([embed_model.output,crf_output])
        #input = tf.keras.layers.Concatenate()([embed_model.output,crf_output])
        #x = tf.keras.layers.Dense(128)(input)
        #logits_label = L.Dense(label_output_dim, **config['layer_time_distributed1'])(logits_label)
        logits_label = L.Bidirectional(L.LSTM(**config['layer_blstm']), name='layer_blstm2')(logits_label)
        logits_label = L.Dense(label_output_dim, **config['layer_time_distributed'])(logits_label)
        #label_predict_output = tf.nn.softmax(logits_label,axis=-1)

        crf2 = KConditionalRandomField()
        crf_classify_output = crf2(logits_label)


        self.tf_model = keras.Model(embed_model.inputs, [crf_output,crf_classify_output])
        #self.tf_model = keras.Model(embed_model.inputs, crf_output)
        self.crf_layer = crf
        self.crf_layer2 = crf2

    def compile_model(self,
                      loss: Any = None,
                      optimizer: Any = None,
                      metrics: Any = None,
                      **kwargs: Any) -> None:

        if loss is None:
            from tensorflow_addons.losses import SigmoidFocalCrossEntropy
            from tensorflow.keras.losses import SparseCategoricalCrossentropy
            #self.mask_save_layer.set_loss_func(SparseCategoricalCrossentropy())
            loss = [self.crf_layer.loss,self.crf_layer2.loss]
        if metrics is None:
            metrics = [[self.crf_layer.accuracy],[self.crf_layer2.accuracy]]
        super(Cascade_Model, self).compile_model(loss=loss,
                                                    optimizer=optimizer,
                                                    metrics=metrics,
                                                    **kwargs)


    def predict(self,
                x_data,
                batch_size: int = 32,
                truncating: bool = False,
                predict_kwargs: Dict = None) :
        """
        Generates output predictions for the input samples.

        Computation is done in batches.

        Args:
            x_data: The input data, as a Numpy array (or list of Numpy arrays if the model has multiple inputs).
            batch_size: Integer. If unspecified, it will default to 32.
            truncating: remove values from sequences larger than `model.embedding.sequence_length`
            predict_kwargs: arguments passed to :meth:`tf.keras.Model.predict`

        Returns:
            array(s) of predictions.
        """
        if predict_kwargs is None:
            predict_kwargs = {}

        if truncating:
            seq_length = self.max_sequence_length
        else:
            seq_length = None

        if type(x_data[0]) == list:
            x_data = ["".join(x).replace("##","").replace('[CLS]',"").replace("[SEP]","") for x in x_data]
        x_data_tokenized = [self.text_processor.text_tokenizer.tokenize(x) for x in x_data]
        lengths = [len(x) for x in x_data_tokenized]

        tensor = self.text_processor.transform(x_data,seq_length=seq_length)
        (pred,pred_labels) = self.tf_model.predict(tensor, batch_size=batch_size, verbose=1, **predict_kwargs)
        #pred= self.tf_model.predict(tensor, batch_size=batch_size, verbose=1, **predict_kwargs)
        pred = pred.argmax(-1)
        pred_labels = pred_labels.argmax(-1)

        x_data_mapping = [self.text_processor.text_tokenizer.rematch(x, x_tokens) for x, x_tokens in
                          zip(x_data, x_data_tokenized)]

        res = self.label_processor.inverse_transform((pred,pred_labels),lengths=lengths,mapping_list=x_data_mapping)
        logger.debug('predict output: {}'.format(np.array(pred).shape))
        logger.debug('predict output argmax: {}'.format(pred))
        return res

    def cascade_label_cross_entropy(self, y_true, y_pred):
        from tensorflow.keras.losses import sparse_categorical_crossentropy
        from tensorflow.keras import backend as K
        import tensorflow as tf
        y_pred = tf.cast(y_pred,tf.float32)
        y_true = tf.cast(y_true,tf.float32)
        mask = K.cast(K.not_equal(y_true, 0),tf.int32)  # 将y_true 中所有为0的找出来，标记为False

        loss_ = sparse_categorical_crossentropy(y_true, y_pred)
        mask = K.cast(mask, dtype=loss_.dtype)  # 将前面统计的是否零转换成1，0的矩阵
        loss_ *= mask  # 将正常计算的loss加上mask的权重，就剔除了padding 0的影响
        loss_ = tf.math.divide_no_nan(tf.reduce_sum(loss_, axis=-1), tf.reduce_sum(mask,axis=-1))
        #loss_ = tf.reduce_mean(sparse_categorical_crossentropy(y_true, y_pred))
        return loss_#K.mean(loss_)
