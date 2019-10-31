from convokit.transformer import Transformer
from convokit.model import Corpus
from nltk.tokenize import word_tokenize


class ImpModTracker(Transformer):
    self.ATTR_NAME = "politicization_reference_transformer"
    self.key_words = set(["word1","word2"])

def transform(self, corpus: Corpus):
        """Adds metadata about self-reflection to each utterance.

        :param corpus: the corpus to compute features for.
        :type corpus: Corpus
        """
        
        for conv_id in corpus.conversations:
            conv = corpus.get_conversation(conv_id)
            for utt in conv.iter_utterances():
                if utt.text != None:
                    tokenized = word_tokenize(utt.text.lower())
                    invocations = 0
                    length = len(tokenized)
                    pol_words = []
                    for token in tokenized:
                        if token in self.key_words:
                            invocations += 1
                            pol_words.append(token)
                    utt.meta["num_pol_refs"] = invocations
                    if (length > 0):
                        utt.meta["num_pol_refs_incidence"] = (invocations/length)
                    else:
                        utt.meta["num_pol_refs_incidence"] = 0
                    utt.meta["pol_words"] = pol_words
        return corpus