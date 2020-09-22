import math
from dataclasses import dataclass
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class OrdinaryLeastSquare:
    def __call__(self, X, Y):
        m = len(X)

        x_mean = sum(X) / m
        y_mean = sum(Y) / m

        t1 = sum((x - x_mean) * (y - y_mean) for x, y in zip(X, Y)) / sum(
            (x - x_mean) ** 2 for x in X
        )
        t0 = y_mean - t1 * x_mean

        return t0, t1


@dataclass
class GradientDescent:
    alpha: float
    iterations: int

    @staticmethod
    def h(t0, t1):
        """Hypothesis"""
        return lambda x: t0 + t1 * x

    def __call__(self, X, Y):
        m = len(X)
        t0 = t1 = 0

        for i in range(self.iterations):
            tmp0 = t0 - self.alpha / m * sum(
                (self.h(t0, t1)(x) - y) for x, y in zip(X, Y)
            )
            tmp1 = t1 - self.alpha / m * sum(
                (self.h(t0, t1)(x) - y) * x for x, y in zip(X, Y)
            )
            t0 = tmp0
            t1 = tmp1

        return t0, t1


class LearningProcedure(Enum):
    ORDINARY_LEAST_SQUARE = 1
    GRADIENT_DESCENT = 2


class LearningProcedureFactory:
    @classmethod
    def create_learning_procedure(
        cls, learning_procedure, alpha=0.00000001, iterations=1000
    ):
        if learning_procedure == LearningProcedure.ORDINARY_LEAST_SQUARE:
            return OrdinaryLeastSquare()
        elif learning_procedure == LearningProcedure.GRADIENT_DESCENT:
            return GradientDescent(alpha, iterations)


class SimpleLinearRegression:
    """Linear regression with one input variable"""

    def __init__(self, X, Y, learning_procedure):
        self._X = X
        self._Y = Y
        self._m = len(X)
        self.predict = None
        self._learning_procedure = learning_procedure
        self._t0 = self._t1 = 0

    @staticmethod
    def h(t0, t1):
        """Hypothesis"""
        return lambda x: t0 + t1 * x

    def _c(self, t0, t1):
        """Cost function"""
        return sum(
            (self.h(t0, t1)(x) - y) ** 2 for x, y in zip(self._X, self._Y)
        ) / (2 * self._m)

    def _rmse(self, t0, t1):
        """Root mean squared error"""
        return math.sqrt(
            sum((self.h(t0, t1)(x) - y) ** 2 for x, y in zip(self._X, self._Y))
            / self._m
        )

    def _cod(self, t0, t1):
        """Coefficient of determination"""
        y_mean = sum(Y) / self._m

        return 1 - sum((y_mean - y) ** 2 for y in Y) / sum(
            (self.h(t0, t1)(x) - y) ** 2 for x, y in zip(self._X, self._Y)
        )

    def train(self):
        """Train a model"""
        self._t0, self._t1 = self._learning_procedure(self._X, self._Y)
        self.predict = self.h(self._t0, self._t1)


if __name__ == "__main__":
    data = pd.read_csv("headbrain.csv")

    X = data["Head Size(cm^3)"].values
    Y = data["Brain Weight(grams)"]

    lp = LearningProcedureFactory.create_learning_procedure(
        LearningProcedure.GRADIENT_DESCENT
    )
    lr = SimpleLinearRegression(X, Y, lp)

    lr.train()

    print(f"{lr._t0=} {lr._t1=}")

    # Plotting Values and Regression Line
    max_x = np.max(X) + 100
    min_x = np.min(X) - 100

    # Calculating line values x and y
    x = np.linspace(min_x, max_x, 1000)
    y = lr._t0 + lr._t1 * x

    # Ploting Line
    plt.plot(x, y, color="#58b970", label="Regression Line")
    # Ploting Scatter Points
    plt.scatter(X, Y, c="#ef5423", label="Scatter Plot")

    plt.xlabel("Head Size in cm3")
    plt.ylabel("Brain Weight in grams")
    plt.legend()
    plt.show()

    print(lr.predict(4000))
