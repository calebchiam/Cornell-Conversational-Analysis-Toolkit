from .srilmWrapper import LanguageModel
from convokit import Transformer, Corpus


class LMTransformer(Transformer):
    def __init__(self, model: LanguageModel, model_name: str, utt_selector: lambda utt: True,
                 utt_text_func = lambda utt: utt.text):
        self.model = model
        self.model_name = model_name
        self.utt_selector = utt_selector
        self.utt_text_func = utt_text_func
        self.perplexity_feat_name = self.model_name + '_perplexity'

    def transform(self, corpus: Corpus) -> Corpus:
        for utt in corpus.iter_utterances():
            if self.utt_selector(utt):
                utt.add_meta(self.perplexity_feat_name, self.model.str_perplexity(self.utt_text_func(utt)))
            else:
                utt.add_meta(self.perplexity_feat_name, None)
        return corpus