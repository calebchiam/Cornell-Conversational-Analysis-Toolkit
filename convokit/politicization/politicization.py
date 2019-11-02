from convokit.transformer import Transformer
from convokit.model import Corpus
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer('english')

class PolTracker(Transformer):
    """
    Extracts information about politicization

    """
    def __init__(self):
        self.ATTR_NAME = "politicization_reference_transformer"
        self.key_words = {'reform', 'bill', 'control', 'senator', 'lobbyist', 'lobbying', 'congress', 'congressman',
                          'president', 'nra', 'rights', 'policy', 'politics', 'government', 'senate', 'representative',
                          'political', 'party', 'republican', 'democrat', 'amendment'}
        self.key_words = {stemmer.stem(word) for word in self.key_words}

    def transform(self, corpus: Corpus):
        """Adds metadata about politicization to each utterance.

        :param corpus: the corpus to compute features for.
        :type corpus: Corpus
        """
        assert 'stem_tokens' in next(corpus.iter_utterances()).meta
        for utt in corpus.iter_utterances():
            if utt.meta['valid']:
                utt.meta['num_pol_words'] = len(self.key_words.intersection(utt.meta['stem_tokens']))
                utt.meta['political'] = int(utt.meta['num_pol_words'] > 0)
            else:
                utt.meta['num_pol_words'] = None
                utt.meta['political'] = None

        # for conv_id in corpus.conversations:
        #     conv = corpus.get_conversation(conv_id)
        #     for utt in conv.iter_utterances():
        #         if utt.text != None:
        #             tokenized = word_tokenize(utt.text.lower())
        #             invocations = 0
        #             length = len(tokenized)
        #             pol_words = []
        #             for token in tokenized:
        #                 if token in self.key_words:
        #                     invocations += 1
        #                     pol_words.append(token)
        #             utt.meta["num_pol_refs"] = invocations
        #             if (length > 0):
        #                 utt.meta["num_pol_refs_incidence"] = (invocations/length)
        #             else:
        #                 utt.meta["num_pol_refs_incidence"] = 0
        #             utt.meta["pol_words"] = pol_words
        return corpus