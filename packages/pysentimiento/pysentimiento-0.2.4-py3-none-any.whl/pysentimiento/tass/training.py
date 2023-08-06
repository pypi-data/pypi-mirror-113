from transformers import (
    AutoModelForSequenceClassification, AutoTokenizer, BertTokenizerFast
)
from ..preprocessing import special_tokens
from .datasets import load_datasets, id2label, label2id

dont_add_tokens = {
    "vinai/bertweet-base"
}

def load_model(base_model, id2label=id2label, label2id=label2id, max_length=128):
    """
    Loads model and tokenizer
    """
    print(f"Loading model {base_model}")
    model = AutoModelForSequenceClassification.from_pretrained(
        base_model, return_dict=True, num_labels=len(id2label)
    )

    tokenizer = AutoTokenizer.from_pretrained(base_model)
    tokenizer.model_max_length = max_length

    #model.config.hidden_dropout_prob = 0.20
    model.config.id2label = id2label
    model.config.label2id = label2id

    if base_model not in dont_add_tokens:
        vocab = tokenizer.get_vocab()
        new_tokens_to_add = [tok for tok in special_tokens if tok not in tokenizer.get_vocab()]

        if new_tokens_to_add:
            """
            TODO: Perdoname Wilkinson, te he fallado

            Hay una interfaz diferente acá, no entiendo bien por qué
            """
            if hasattr(tokenizer, "is_fast") and tokenizer.is_fast:
                tokenizer.add_special_tokens({'additional_special_tokens': new_tokens_to_add})
            else:
                tokenizer.add_special_tokens(new_tokens_to_add)
            model.resize_token_embeddings(len(tokenizer))
    return model, tokenizer