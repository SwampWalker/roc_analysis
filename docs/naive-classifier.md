# The naive classifier

Imagine you have some repeatable test that you can perform that gives a binary result:
positive or negative. Each test performed gives a result independent of the first and
with the same distribution for positive or negative. 

This model is naive because of the independence of the tests and repeatability.

There are a few parameters:

- Sensitivity: if the true value is postive, the probability of a positive test: `P(+|+) = p_p`
- Specificity: if the true value is negative, the probability of a negative test: `P(-|-) = p_n`
- number of tests
- Discrimination threshold, between 0 and the number of tests to consider repeated tests a positive or negative

## Math

This model requires no actual simulation. The specificity and sensitivity of repeated tests can be
computed as a function of the discrimination threshold.

Bear in mind there is always the strategy of: ignore evidence and assume positive, assume negative.
This is equivalent to the random classifier.

### 1 test:

- Sensitivity: `p_p`
- Specificity: `p_n`

### 2 tests,

Either 1 negative is allowed or 0 negatives are allowed (2 negatives is equivalent to always positive)

0 negatives allowed:
- Sensitivity: `p_p^2`
- Specificity: `1 - q_n^2`

1 negative allowed:
- Sensitivity: `p_p^2 + 2 p_p q_p`
- Specificity: `1 - q_n^2 - 2 p_n q_n`

### 2 tests,

From 0 - 2 negatives are allowed.

0 negatives allowed:
- Sensitivity: `p_p^3`
- Specificity: `1 - q_n^3`

1 negative allowed:
- Sensitivity: `p_p^3 + 3 p_p^2 q_p`
- Specificity: `1 - q_n^3 - 3 p_n q_n^2`

2 negatives allowed:
- Sensitivity: `p_p^3 + 3 p_p^2 q_p + 3 p_p q_p^2`
- Specificity: `1 - q_n^3 - 3 p_n q_n^2 - 3 p_n^2 q_n^2`

### N tests

From 0 - N-1 negatives are allowed, lets call the maximum number of negatives tolerated (the discrimination
threshold M).

- Sensitivity:
```
let sum = 0;
for i in 0..M
    sum += (N choose M) p_p^(N-i) q_p^i
```
- Specificity:
```
let sum = 1;
for i in 0..M
    sum -= (N choose M) p_n^i q_n^(N-i)
```

I feel like it should be possible to make a continuous version of the same basic behavior without 
going to gaussian probes.