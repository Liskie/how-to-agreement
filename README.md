# how-to-agreement

## Prerequisites

The following package is used in the code:
- nltk

You can install it by running:
```shell
pip install nltk
```

## Quick Start

To calculate agreement scores, one can use ```nltk.metrics.agreement```.

We provide a simple code snippet in _agreement.py_ :

```python
def fleiss_kappa(worker_tags: list[list[str]]) -> float:
    """
    Calculate the Fleiss' Kappa score of several(>=2) workers' annotations on the same sequence.
    Example of worker_tags:
    [
        ['B-POS', 'I-POS', 'O'    ], # worker 1
        ['B-POS', 'O',     'O'    ], # worker 2
        ['B-POS', 'I-POS', 'I-POS'], # worker 3
    ]
    """
    assert len(worker_tags) >= 2

    # Check if all workers give no annotation spans on the sequence.
    is_only_O = True
    for tags in worker_tags:
        if not is_only_O:
            break
        for tag in tags:
            if tag != 'O':
                is_only_O = False
                break
    if is_only_O:
        return 1.0

    # The NLTK implementation.
    data = []
    for worker_idx, tags in enumerate(worker_tags):
        for tag_idx, tag in enumerate(tags):
            data.append((worker_idx, tag_idx, tag))
    task = agreement.AnnotationTask(data=data)
    return task.multi_kappa()
```

The argument ```worker_tags: list[list[str]]``` is a list of annotations from different workers on the same sentence.

For example, 3 workers annotate the sentence _I love you_.
We split the sentence into words like ```['I', 'love', 'you']```. 
Each worker assigns a BIO tag on each word in the sentence like ```['B-POS', 'I-POS', 'O']```.
We collect annotations from all workers:
```python
worker_tags = [
    ['B-POS', 'I-POS', 'O'    ], # worker 1
    ['B-POS', 'O',     'O'    ], # worker 2
    ['B-POS', 'I-POS', 'I-POS'], # worker 3
]
```

Now, just call the function and get the fleiss' kappa score calculated.
```python
fleiss_kappa(worker_tags) # 0.3999999999999999
```

## Not enough for your experiments?

You can refer to the [official document](https://www.nltk.org/api/nltk.metrics.agreement.html) of the ```nltk.mertics.agreement``` module.