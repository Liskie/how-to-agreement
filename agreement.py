from nltk.metrics import agreement


def fleiss_kappa(worker_tags: list[list[str]]) -> float:
    """
    Calculate the Fleiss' Kappa score of several(>=2) workers' annotations on the same sequence.
    Example of worker_tags:
    [
        ['B-POS', 'I-POS', 'O'    ],  # worker 1
        ['B-POS', 'O',     'O'    ],  # worker 2
        ['B-POS', 'I-POS', 'I-POS'],  # worker 3
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


if __name__ == '__main__':
    # Running example.

    data = [
        ['B-POS', 'I-POS', 'O'    ],  # worker 1
        ['B-POS', 'O',     'O'    ],  # worker 2
        ['B-POS', 'I-POS', 'I-POS'],  # worker 3
    ]

    print(fleiss_kappa(data))  # 0.3999999999999999
