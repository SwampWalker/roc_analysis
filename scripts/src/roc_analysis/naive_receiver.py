import sys
from typing import List, Tuple
import matplotlib.pyplot as plt

class OperatingCharacteristic:
    specificities: List[float]
    sensitivities: List[float]

    def __init__(self, specificities: List[float], sensitivities: List[float]):
        self.specificities = specificities
        self.sensitivities = sensitivities

        if len(sensitivities) != len(specificities):
            raise ValueError("Received a differing amount of sensitivities and specificities.")


class NaiveClassifier:
    """
    Operates by generating n independent random variables that have a positive or negative outcome dictated
    by an identical sensitivity and specificity.

    Calling this classifier naive is a bit of a misnomer. Instead it is the model that is naive:
    this classifier is capable or repeated probes each one of which provides binary evidence
    and is independent and identically distributed.

    That's more powerful than naive, but unrealistic and hence naive. Simple to model, so here it
    is.
    """
    specificity: float
    sensitivity: float

    def __init__(self, specificity: float, sensitivity: float):
        self.specificity = specificity
        self.sensitivity = sensitivity

        errors = []
        if specificity > 1:
            errors.append("Specificity cannot be greater than 1, received " + str(specificity) + ".")
        if sensitivity > 1:
            errors.append("Sensitivity cannot be greater than 1, received " + str(sensitivity) + ".")
        if specificity < 0:
            errors.append("Specificity cannot be less than 0, received " + str(specificity) + ".")
        if sensitivity < 0:
            errors.append("Sensitivity cannot be less than 0, received " + str(sensitivity) + ".")

        if errors:
            raise ValueError(", ".join(errors))

    def operating_characteristics(self, n_questions: int) -> List[OperatingCharacteristic]:
        """
        Why return multiple characteristics all at once?

        Iterative multiplication is often faster than floating point powers (exponentiation).
        Moreover, the previous powers are relevant in the following (or previous depending on p or q),
        operating point of the characteristic. So it is cheaper to compute the n'th characteristic
        from the (n-1)'th characteristic (it is O(n)).

        Since I want to visualize multiple characteristics, just compute them all up to the last one
        of interest.
        """
        assert n_questions >= 0

        sensitivity_combos = combinatorics(self.sensitivity, n_questions)
        sensitivities_by_n = probability_sums(sensitivity_combos)

        specificity_combos = combinatorics(self.specificity, n_questions)
        specificities_by_n = []
        for sum in probability_sums(specificity_combos):
            specificity_n = list(reversed(sum))
            specificities_by_n.append(specificity_n)

        return [
            OperatingCharacteristic(sensitivities, specificities)
            for (sensitivities, specificities)
            in zip(sensitivities_by_n, specificities_by_n)
        ]


def combinatorics(p: float, n: int) -> List[List[float]]:
    """
    There is this nice triangle pattern for computing the terms in (p + q)^n.

    For n = 0, the single term is 1.
    For n = 1, the terms are [p, q].
    For n = 2, the terms are [p^2, 2pq, q^2].
    For n = 3, the terms are [p^3, 3p^2q, 3pq^2, q^3].

    The evolving pattern is of course recursion: (p + q)^n = p(p + q)^(n-1) + q(p + q)^(n-1),
    multiply the n-1 list by p and q, insert 0 at the end and beginning respectively, then
    sum the corresponding terms of the lists.

    Of course each term is nCr p^(n-r) q^r or something like that.
    """
    assert n >= 0
    q = 1 - p

    current = [1]
    combinations = [current]

    for i in range(0, n):
        current_p = [p * combo for combo in current]
        current_q = [q * combo for combo in current]

        current_p.append(0)
        current_q.insert(0, 0)

        current = [left + right for (left, right) in zip(current_p, current_q)]
        combinations.append(current)

    return combinations


def probability_sums(combinatorics: List[List[float]]) -> List[List[float]]:
    sums = []
    for combinations in combinatorics:
        current_sum = 0
        sum = [current_sum]
        for term in combinations:
            current_sum += term
            sum.append(current_sum)
        sums.append(sum)

    return sums


def graph(characteristics: List[OperatingCharacteristic]):
    fig, ax = plt.subplots()
    for operating_characteristic in characteristics[1:7:2]:
        label = "n = " + str(len(operating_characteristic.sensitivities) - 2)
        ax.scatter(operating_characteristic.sensitivities, operating_characteristic.specificities, label=label)

    ax.set_xlabel("Sensitivity")
    ax.set_ylabel("Specificity")

    ax.legend()

    plt.show()


def main():
    classifier = NaiveClassifier(0.85, 0.8)
    characteristics = classifier.operating_characteristics(20)
    graph(characteristics)


if __name__ == '__main__':
    sys.exit(main())