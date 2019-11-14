from convokit.transformer import Transformer
from convokit.model import Corpus
from nltk.stem import SnowballStemmer
from empath import Empath
stemmer = SnowballStemmer('english')
lexicon = Empath()

class EmoTracker(Transformer):
    """
    Extracts information about politicization

    """
    def __init__(self):
        self.ATTR_NAME = "emotion_tranformer"
        self.categories=["sadness", "violence", "rage", "pain", "anger", "love", "politics"]

    def transform(self, corpus: Corpus):
        """Adds metadata about politicization to each utterance.

        :param corpus: the corpus to compute features for.
        :type corpus: Corpus
        """
        assert 'stem_tokens' in next(corpus.iter_utterances()).meta
        counter = 1
        for utt in corpus.iter_utterances():
            if utt.meta['valid']:
                utt.meta['analysis'] = lexicon.analyze(utt.text,categories=self.categories)
                for k in utt.meta['analysis'].keys():
                    if utt.meta['analysis'][k] != 0.0:
                        utt.meta['analysis'][k] = 1
            else:
                utt.meta['analysis'] = None

            counter = counter + 1
            if counter % 10000 == 0:
                print("processed ", counter, "utterances ")
        return corpus