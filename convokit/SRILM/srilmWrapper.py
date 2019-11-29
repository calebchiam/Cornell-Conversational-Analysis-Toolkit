import os
import subprocess
from typing import Optional

class LanguageModel:
    def __init__(self, SRILM_path: str,
                 working_dir: str,
                 lm_output_path: str,
                 count_output_path: str,
                 lm_type: str = "ngram-count",
                 lm_filepath: Optional[str] = None,
                 order: int = 2,
                 smooth: int = 1, verbose=True):
        self.SRILM_path = os.path.join(SRILM_path, "bin/macosx")
        self.dir = working_dir
        assert lm_type in ["ngram-count", "laplace", "kneser-ney"]
        self.lm_type = lm_type
        self.lm_output_path = lm_output_path
        self.count_output_path = count_output_path
        self.order = order
        self.smooth = smooth
        self.lm_filepath = lm_filepath
        self.verbose = verbose

    @staticmethod
    def commands():
        return {'ngram-count': "{SRILM_path}/ngram-count -text {corpus_text} -lm {lm_output} "
                               "-order {order} -write {count_output}",
                'laplace': "{SRILM_path}/ngram-count -text {corpus_text} -order {order} -addsmooth {smooth} -write {count_output}"
                           " -lm {lm_output}",
                # https://linguistics.stackexchange.com/questions/11957/different-discounting-methods-with-srilm-toolikt
                'kneser-ney': "{SRILM_path}/ngram-count -kndiscount -interpolate -order {order} -write {count_output} -lm {lm_output}",
                'perplexity': "{SRILM_path}/ngram -lm {lm_filepath} -ppl {target_text}"
                }

    def train(self, corpus_text_file: str):
        if self.lm_filepath is not None:
            raise TypeError("LM is already trained. Initialize LanguageModel without a lm_filepath instead.")
        else:
            cmd = LanguageModel.commands()[self.lm_type].format(SRILM_path=self.SRILM_path,
                                                                corpus_text=corpus_text_file,
                                                                order=self.order,
                                                                smooth=self.smooth,
                                                                count_output=self.dir + self.count_output_path,
                                                                lm_output=self.dir + self.lm_output_path)

            result = subprocess.getoutput(cmd)
            self.lm_filepath = self.dir + self.lm_output_path
            print(result)

    def file_perplexity(self, target_text_file):
        cmd = LanguageModel.commands()['perplexity'].format(SRILM_path=self.SRILM_path,
                                                            lm_filepath=self.lm_filepath,
                                                            target_text=target_text_file)
        result = subprocess.getoutput(cmd)
        if self.verbose: print(result)
        ppl = float(result.split("ppl= ")[1].split()[0])
        return ppl

    def str_perplexity(self, str_: str):
        temp_folder = os.path.join(self.dir, 'temp')
        os.makedirs(temp_folder, exist_ok=True)

        hash_str = str(abs(hash(str_)))
        temp_file = os.path.join(temp_folder, hash_str+".txt")
        # print(temp_file)
        with open(temp_file, 'w') as f:
            f.write(str_)

        ppl = self.file_perplexity(temp_file)
        os.remove(temp_file)
        return ppl

    def file_perplexity1(self, target_text_file):
        cmd = LanguageModel.commands()['perplexity'].format(SRILM_path=self.SRILM_path,
                                                            lm_filepath=self.lm_filepath,
                                                            target_text=target_text_file)
        result = subprocess.getoutput(cmd)
        if self.verbose: print(result)
        ppl = float(result.split("ppl1= ")[1].split()[0])
        return ppl

    def str_perplexity1(self, str_: str):
        temp_folder = os.path.join(self.dir, 'temp')
        os.makedirs(temp_folder, exist_ok=True)

        hash_str = str(abs(hash(str_)))
        temp_file = os.path.join(temp_folder, hash_str+".txt")
        # print(temp_file)
        with open(temp_file, 'w') as f:
            f.write(str_)

        ppl = self.file_perplexity1(temp_file)
        os.remove(temp_file)
        return ppl
