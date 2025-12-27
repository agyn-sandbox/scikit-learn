from sklearn import config_context
from sklearn.model_selection import (
    RepeatedKFold,
    RepeatedStratifiedKFold,
)


def test_repeated_kfold_repr_default():
    with config_context(print_changed_only=False):
        assert (
            repr(RepeatedKFold())
            == "RepeatedKFold(n_splits=5, n_repeats=10, random_state=None)"
        )


def test_repeated_stratified_kfold_repr_default():
    with config_context(print_changed_only=False):
        assert (
            repr(RepeatedStratifiedKFold())
            == "RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=None)"
        )


def test_repeated_kfold_repr_nondefault():
    with config_context(print_changed_only=False):
        assert (
            repr(RepeatedKFold(n_splits=3, n_repeats=2, random_state=42))
            == "RepeatedKFold(n_splits=3, n_repeats=2, random_state=42)"
        )


def test_repeated_stratified_kfold_repr_nondefault():
    with config_context(print_changed_only=False):
        assert (
            repr(RepeatedStratifiedKFold(n_splits=4, n_repeats=3, random_state=0))
            == "RepeatedStratifiedKFold(n_splits=4, n_repeats=3, random_state=0)"
        )
