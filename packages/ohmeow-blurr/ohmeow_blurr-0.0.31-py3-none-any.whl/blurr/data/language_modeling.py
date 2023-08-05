# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/02_data-language-modeling.ipynb (unless otherwise specified).

__all__ = ['LMType', 'LMStrategy', 'HF_LMBeforeBatchTransform', 'HF_CausalLMInput', 'CausalLMStrategy', 'HF_MLMInput',
           'BertMLMStrategy']

# Cell
import torch, pdb
from enum import Enum
from abc import ABC, abstractmethod

from transformers import *
from fastai.text.all import *

from ..utils import *
from .core import *
# from blurr.data.seq2seq.core import *

logging.set_verbosity_error()

# Cell
class LMType(Enum):
    CAUSAL = 1
    MASKED = 2

# Cell
class LMStrategy(ABC):
    """ABC for various language modeling strategies"""
    def __init__(self, hf_tokenizer, ignore_token_id=CrossEntropyLossFlat().ignore_index):
        store_attr(['hf_tokenizer', 'ignore_token_id'])

    @abstractmethod
    def build_inputs_targets(self, samples):
        pass

    # utility methods
    def _get_random_token_id(self,n):
        return random.sample(list(self.hf_tokenizer.get_vocab().values()), n)

    @classmethod
    @abstractmethod
    def get_lm_type(cls):
        pass

# Cell
class HF_LMBeforeBatchTransform(HF_BeforeBatchTransform):
    def __init__(self, hf_arch, hf_config, hf_tokenizer, hf_model, lm_strategy_cls:LMStrategy,
                 max_length=None, padding=True, truncation=True, is_split_into_words=False,
                 ignore_token_id = CrossEntropyLossFlat().ignore_index,
                 tok_kwargs={}, text_gen_kwargs={}, **kwargs):

        super().__init__(hf_arch, hf_config, hf_tokenizer, hf_model,
                         max_length=max_length, padding=padding, truncation=truncation,
                         is_split_into_words=is_split_into_words,
                         tok_kwargs=tok_kwargs.copy(), **kwargs)

        self.lm_strategy = lm_strategy_cls(hf_tokenizer=hf_tokenizer, ignore_token_id=ignore_token_id)
        self.text_gen_kwargs, self.ignore_token_id = text_gen_kwargs, ignore_token_id

    def encodes(self, samples):
        # because no target is specific in CLM, fastai will duplicate the inputs (which is just the raw text)
        samples = super().encodes(samples)
        if (len(samples[0]) == 1): return samples

        return self.lm_strategy.build_inputs_targets(samples)

# Cell
class HF_CausalLMInput(HF_BaseInput): pass

# Cell
class CausalLMStrategy(LMStrategy):
    """For next token prediction language modeling tasks, we want to use the `CausalLMStrategy` which makes the
    necessary changes in your inputs/targets for causal LMs
    """
    def build_inputs_targets(self, samples):
        updated_samples = []
        for s in samples:
            s[0]['labels'] = s[0]['input_ids'].clone()
            s[0]['labels'][s[0]['labels'] == self.hf_tokenizer.pad_token_id] = self.ignore_token_id
            targ_ids = torch.cat([s[0]['input_ids'][1:], tensor([self.hf_tokenizer.eos_token_id])])

            updated_samples.append((s[0], targ_ids))

        return updated_samples

    @classmethod
    def get_lm_type(cls):
        return LMType.CAUSAL

# Cell
@typedispatch
def show_batch(x:HF_CausalLMInput, y, samples, dataloaders, ctxs=None, max_n=6, trunc_at=None, **kwargs):
    # grab our tokenizer and ignore token to decode
    hf_before_batch_tfm = get_blurr_tfm(dataloaders.before_batch)
    hf_tokenizer = hf_before_batch_tfm.hf_tokenizer
    ignore_token_id = hf_before_batch_tfm.ignore_token_id

    res = L([ (hf_tokenizer.decode(s[0], skip_special_tokens=False)[:trunc_at],
               hf_tokenizer.decode(s[1][s[1] != ignore_token_id], skip_special_tokens=True)[:trunc_at])
             for s in samples ])

    display_df(pd.DataFrame(res, columns=['text', 'target'])[:max_n])
    return ctxs

# Cell
class HF_MLMInput(HF_BaseInput): pass

# Cell
class BertMLMStrategy(LMStrategy):
    """A masked language modeling strategy using the default BERT masking definition.
    """
    def __init__(self, hf_tokenizer, ignore_token_id=CrossEntropyLossFlat().ignore_index):
        super().__init__(hf_tokenizer, ignore_token_id)

        vocab = hf_tokenizer.get_vocab()
        self.dnm_tok_ids = [vocab[tok]  for tok in list(hf_tokenizer.special_tokens_map.values())
                            if vocab[tok] != hf_tokenizer.mask_token_id]

    def build_inputs_targets(self, samples):
        updated_samples = []
        for s in samples:
            # mask the input_ids
            masked_input_ids = s[0]['input_ids'].clone()

            # we want to mask 15% of the non-special tokens(e.g., special tokens inclue [CLS], [SEP], etc...)
            idxs = torch.randperm(len(masked_input_ids))
            total_masked_idxs = int(len(idxs) * .15)

            # of the 15% for masking, replace 80% with [MASK] token, 10% with random token, and 10% with correct token
            n_mask_idxs = int(total_masked_idxs * .8)
            n_rnd_idxs = int(total_masked_idxs * .1)

            # we only want non-special tokens
            mask_idxs = [ idx for idx in idxs if masked_input_ids[idx] not in self.dnm_tok_ids ][:total_masked_idxs]

            # replace 80% with [MASK]
            if (n_mask_idxs > 0 and  len(mask_idxs) >= n_mask_idxs):
                masked_input_ids[[mask_idxs[:n_mask_idxs]]] = self.hf_tokenizer.mask_token_id

            # replace 10% with a random token
            if (n_rnd_idxs > 0 and  len(mask_idxs) >= (n_mask_idxs + n_rnd_idxs)):
                rnd_tok_ids = self._get_random_token_id(n_rnd_idxs)
                masked_input_ids[[mask_idxs[n_mask_idxs:(n_mask_idxs + n_rnd_idxs)]]] = tensor(rnd_tok_ids)

            # ignore padding when calculating the loss
            lbls = s[0]['input_ids'].clone()
            lbls[[[idx for idx in idxs if idx not in mask_idxs]]] = self.ignore_token_id

            # update the inputs to use our masked input_ids and labels; set targ_ids = labels (will use when
            # we calculate the loss ourselves)
            s[0]['input_ids'] = masked_input_ids
            s[0]['labels'] = lbls
            targ_ids = lbls.clone()

            updated_samples.append((s[0], targ_ids))

        return updated_samples

    @classmethod
    def get_lm_type(cls):
        return LMType.MASKED

# Cell
@typedispatch
def show_batch(x:HF_MLMInput, y, samples, dataloaders, ctxs=None, max_n=6, trunc_at=None, **kwargs):
    # grab our tokenizer and ignore token to decode
    hf_before_batch_tfm = get_blurr_tfm(dataloaders.before_batch)
    hf_tokenizer = hf_before_batch_tfm.hf_tokenizer
    ignore_token_id = hf_before_batch_tfm.ignore_token_id

    # grab our mask token id and do-not-mask token ids
    mask_token_id = hf_tokenizer.mask_token_id
    dnm_tok_ids = hf_before_batch_tfm.lm_strategy.dnm_tok_ids

    res = L()
    for s in samples:
        # exclue dnm tokens from input
        inps = [ hf_tokenizer.decode(tok_id)
                if (tok_id == mask_token_id or s[1][idx] == ignore_token_id)
                else f'[{hf_tokenizer.decode(tok_id)}]'
                for idx, tok_id in enumerate(s[0]) if (tok_id not in dnm_tok_ids) ]

        # replaced masked tokens with "[{actual_token}]"
        trgs = [ hf_tokenizer.decode(s[0][idx])
                if (tok_id == ignore_token_id)
                else f'[{hf_tokenizer.decode(tok_id)}]'
                for idx, tok_id in enumerate(s[1]) if (s[0][idx] not in dnm_tok_ids) ]

        res.append((' '.join(inps[:trunc_at]).strip(), ' '.join(trgs[:trunc_at]).strip()))

    display_df(pd.DataFrame(res, columns=['text', 'target'])[:max_n])
    return ctxs