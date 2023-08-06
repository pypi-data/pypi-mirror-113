from nlp_tools.tasks.labeling.abc_model import ABCLabelingModel
from nlp_tools.tasks.labeling.bi_lstm_model import BiLSTM_Model
from nlp_tools.tasks.labeling.bi_lstm_crf_model import BiLSTM_CRF_Model



from nlp_tools.tokenizer.bert_tokenizer import BertTokenizer
model_pipeline = {
    'global_point':{
        'tokeninzer':BertTokenizer
    }
}