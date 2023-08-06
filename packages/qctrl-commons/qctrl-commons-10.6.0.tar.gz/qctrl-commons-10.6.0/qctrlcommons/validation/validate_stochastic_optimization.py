"""
Validator for core__calculateStochasticOptimization mutation.
"""

from qctrlcommons.exceptions import QctrlFieldError
from qctrlcommons.validation.base import BaseMutationInputValidator


def _check_adam_optimizer(input_):
    """
    Checks the configuration for the Adam optimizer.
    """

    learning_rate = input_["optimizer"]["adam"]["learningRate"]
    if learning_rate <= 0:
        raise QctrlFieldError(
            message="'learning_rate' of the Adam optimizer must be positive.",
            fields=["adam"],
        )


AVAILABLE_OPTIMIZERS = {"adam": _check_adam_optimizer}


class CalculateStochasticOptimizationValidator(BaseMutationInputValidator):
    """
    Validator for core__calculateStochasticOptimization mutation.
    """

    properties = {"iterationCount": {"type": "number", "exclusiveMinimum": 0}}

    def check_optimizer(self, input_):  # pylint:disable=no-self-use
        """
        Check optimizer.

        1. if not set, skip
        2. if set, must be one of those supported
        3. check configuration

        Raises
        ------
        QctrlFieldError
            If one of conditions above fails.
        """

        optimizer = input_.get("optimizer")

        # skip checking if default optimizer is used.
        if optimizer is None:
            return

        optimizer_name = next(iter(optimizer))

        if optimizer_name not in AVAILABLE_OPTIMIZERS.keys():
            raise QctrlFieldError(
                message="One of the following optimizers must be set: "
                f"{AVAILABLE_OPTIMIZERS.keys()}",
                fields=["optimizer"],
            )

        AVAILABLE_OPTIMIZERS[optimizer_name](input_)
