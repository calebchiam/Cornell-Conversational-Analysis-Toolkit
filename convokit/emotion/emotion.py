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
        self.categories=["negative_emotion", "shame", "violence", "rage", "pain", "anger", "disgust", "hate", 
                "love", "politics"]

    def transform(self, corpus: Corpus):
        """Adds metadata about politicization to each utterance.

        :param corpus: the corpus to compute features for.
        :type corpus: Corpus
        """
        assert 'stem_tokens' in next(corpus.iter_utterances()).meta
        counter = 1
        for utt in corpus.iter_utterances():
            if utt.meta['valid'] and counter < 500:

                utt.meta['analysis'] = lexicon.analyze(utt.text,categories=self.categories)
            else:
                utt.meta['analysis'] = None

            counter = counter + 1
            if counter % 500 == 0:
                print("processed ", counter, "utterances ")
        return corpus