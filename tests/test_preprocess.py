import os
import sys

import pandas.api.types as ptypes

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import preprocess


def test_encode_cat_cols(sample_dataframe):
    cols_to_cast = "Name"
    sample_dataframe = preprocess.cast_to_string(
        sample_dataframe, cols_to_cast=[cols_to_cast]
    )

    assert ptypes.is_string_dtype(
        sample_dataframe[cols_to_cast]
    ), f"Column {cols_to_cast} is not of type string"


def test_exist_unnecessary_columns(sample_dataframe):
    cols_to_drop = ["City"]  # You can also try with more than one element
    sample_dataframe = preprocess.drop_unnecessary_columns(
        sample_dataframe, cols_to_drop
    )
    sample_columns = sample_dataframe.columns
    for col in cols_to_drop:
        assert not col in sample_columns
