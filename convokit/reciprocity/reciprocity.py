from convokit.model import Corpus, User
from convokit.transformer import Transformer
from itertools import combinations
from typing import Tuple

class Reciprocity(Transformer):

    def __init__(self):
        pass

    @staticmethod
    def _calculate_something(arg):
        return [x for x in arg]

    def transform(self, corpus: Corpus):
        for convo in corpus.iter_conversations():
            reciprocal = 0
            onesided = 0
            user_to_targets = dict()
            for user in convo.iter_users():
                user_to_targets[user.name] = {corpus.get_utterance(utt.reply_to).user.name
                                              for utt in user.iter_utterances() if utt.reply_to is not None}

            for user1, user2 in combinations(convo.iter_users(), 2):
                user1_to_user2 = user2.name in user_to_targets[user1.name]
                user2_to_user1 = user1.name in user_to_targets[user2.name]

                if user1_to_user2 and user2_to_user1:
                    reciprocal += 1
                elif user1_to_user2 or user2_to_user1:
                    onesided += 1

            if reciprocal + onesided == 0:
                reciprocity_pct = 0
            else:
                reciprocity_pct = reciprocal / (reciprocal + onesided)

            convo.add_meta('reciprocity', reciprocity_pct)
        return corpus
