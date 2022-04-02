# -*- coding: utf-8 -*-
"""Tests for transformer pipelines."""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.tree import DecisionTreeClassifier

from sktime.datasets import load_gunpoint
from sktime.transformations.panel.reduce import Tabularizer
from sktime.transformations.panel.segment import RandomIntervalSegmenter
from sktime.utils._testing.panel import make_classification_problem

# load data
X, y = make_classification_problem()
X_train, X_test, y_train, y_test = train_test_split(X, y)

mean_transformer = Tabularizer(FunctionTransformer(func=np.mean, validate=False))
std_transformer = Tabularizer(FunctionTransformer(func=np.mean, validate=False))


def test_FeatureUnion_pipeline():
    """Test pipeline with FeatureUnion."""
    # pipeline with segmentation plus multiple feature extraction

    steps = [
        ("segment", RandomIntervalSegmenter(n_intervals=1)),
        (
            "transform",
            FeatureUnion([("mean", mean_transformer), ("std", std_transformer)]),
        ),
        ("clf", DecisionTreeClassifier()),
    ]
    clf = Pipeline(steps)

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    assert y_pred.shape[0] == y_test.shape[0]
    np.testing.assert_array_equal(np.unique(y_pred), np.unique(y_test))


def test_FeatureUnion():
    """Test FeatureUnion fit_transform."""
    X, y = load_gunpoint(return_X_y=True)
    feature_union = FeatureUnion([("mean", mean_transformer), ("std", std_transformer)])
    Xt = feature_union.fit_transform(X, y)
    assert Xt.shape == (X.shape[0], X.shape[1] * len(feature_union.transformer_list))
