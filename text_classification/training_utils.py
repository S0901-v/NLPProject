from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import evaluate
from evaluate import load

metric = load("accuracy")
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references = labels)

def get_class_weights(df):
    class_weights =  compute_class_weight("balanced",
                                          #classes = sorted(df["label"].unique().tolist()),
                                          classes = np.array(sorted(df["label"].unique())),
                                          y = df["label"].to_numpy()
                                          )
    return class_weights