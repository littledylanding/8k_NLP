import pandas as pd
from transformers import BartForConditionalGeneration, BartTokenizer

df = pd.read_pickle('df_item_full_sp600.pkl')

bart_model_name = 'facebook/bart-large-cnn'
bart_model = BartForConditionalGeneration.from_pretrained(bart_model_name)
bart_tokenizer = BartTokenizer.from_pretrained(bart_model_name)


def bart_summarize(text):
    inputs = bart_tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
    summary_ids = bart_model.generate(inputs.input_ids, num_beams=4, min_length=30, max_length=250, early_stopping=True)
    return bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True)


df['summary_bart'] = df['Content'].apply(bart_summarize)
df.to_csv("full_summary.csv")
