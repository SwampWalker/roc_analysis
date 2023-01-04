# The random classifier

Choose some proportion and randomly assign that proportion of subjects to an outcome of positive.

This classifier has an equal true positive rate and false positive rate. It is a counter example
to the idea that maximizing the true positives or minimizing the false positives ignoring the
other proportion can make sense: any particular value can be achieved by this classifier at the
price of having the equal proportion in the other quality measure.

This can be measured by the Informedness: TPR + TNR - 1, which will always be zero.