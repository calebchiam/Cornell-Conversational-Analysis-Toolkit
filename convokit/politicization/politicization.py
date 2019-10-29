from convokit.transformer import Transformer
from convokit.model import Corpus
from nltk.tokenize import word_tokenize


class PolTracker(Transformer):
    """
    Extracts information about invoking the self in utterances.

    """
    def __init__(self):
        #self.ATTR_NAME = "self_reference_transformer"
        #self.key_words = set(
        #    ["i", "we", "my", "our", "ours", "me", "us", "mine"])

        ##code goes here

    def transform(self, corpus: Corpus):
        """Adds metadata about self-reflection to each utterance.

        :param corpus: the corpus to compute features for.
        :type corpus: Corpus
        """

        ##code goes here
        
        #for conv_id in corpus.conversations:
        #    conv = corpus.get_conversation(conv_id)
        #    for utt in conv.iter_utterances():
        #        if utt.text != None:
        #            tokenized = word_tokenize(utt.text.lower())
        #            invocations = 0
        #            for token in tokenized:
        #                if token in self.key_words:
        #                    invocations += 1
        #            utt.meta["num_self_invocations"] = invocations
        return corpus