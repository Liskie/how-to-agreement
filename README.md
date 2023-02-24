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

### Different Agreements

- Cohen's Kappa: This kappa is initially designed for two annotators. For multiple (>= 3) annotators, it is pairwise calculated and averaged.
    ```python
    AnnotationTask.kappa()
    ```
- Fleiss' Kappa: By default, you should use this kappa for the multi-annotator situation.
    ```python
    AnnotationTask.multi_kappa()
    ```
- Krippendorff's Alpha: This is another implementation of multi-annotator agreement. The value of this agreement is very close to Fleiss' Kappa.
    ```python
    AnnotationTask.alpha()
    ```

### How to deal with nested spans (e.g. trees)?

We provide one possible solution:
1. Extract all subsequences from the original sequence.
2. Concatenate the subsequences into a long sequence.
3. Copy annotation spans to corresponding subsequences in the long sequence.
4. Calculate agreement with long annotation sequences.

Following is an example:

The original sequence is 
```python
['I', 'love', 'you']
```

We extract all subsequences and concatenate them into 
```python
[
  'I', 'love', 'you', # length = 3 
  'I', 'love',        # length = 2
  'love', 'you',      # length = 2
  'I',                # length = 1
  'love',             # length = 1
  'you'               # length = 1
]
```

An annotator gives a syntax tree annotation like 

!['[S [NP I] [VP [V love] [NP you]]]'](img/syntax_tree_1.png "Syntax Tree")

We can translate it into nested spans:
```python
[(0, 3, 'S'), (0, 1, 'NP'), (1, 3, 'VP'), (1, 2, 'V'), (2, 3, 'NP')]
```

Then overwrite the concatenated sequence with these spans:
```python
[
  'B-S', 'I-S', 'I-S', # ['I', 'love', 'you'] is 'S'
  'O', 'O',            #        ['I', 'love'] is not annotated 
  'B-VP', 'I-VP',      #      ['love', 'you'] is 'VP'
  'B-NP',              #                ['I'] is 'NP'
  'B-V',               #             ['love'] is 'V'
  'B-NP'               #              ['you'] is 'NP'
]
# We use BIO tags here.
```

Now, we can calculate Fleiss' Kappa of such concatenated annotation sequences from different annotators.

### What if nested spans completely overlap?

Consider the following syntax tree:

!['[S [NP [N I]] [VP [V love] [NP you]]]'](img/syntax_tree_2.png "Syntax Tree")

We may translate this annotation of syntax tree into:
```python
[
  ['B-S',  'I-S',  'I-S' ], # S
  ['B-NP', 'O',    'N-NP'], # NP
  ['O',    'B-VP', 'I-VP'], # VP
  ['B-N',  'O',    'O'   ], # N
  ['O',    'B-V',  'O'   ], # VP
# ['I',    'love', 'you' ]
]
```
Then Fleiss' Kappa can be calculated.

## Not enough for your experiments?

You can refer to the [official document](https://www.nltk.org/api/nltk.metrics.agreement.html) of the ```nltk.mertics.agreement``` module.