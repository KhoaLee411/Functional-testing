def drop_unnecessary_columns(df, cols_to_drop):
    # Drop columns which are excluded from
    # the training set
    df = df.drop(columns=cols_to_drop, errors="ignore")
    return df


def cast_to_string(df, cols_to_cast):
    for col in cols_to_cast:
        df[col] = df[col].astype(str)

    return df


def encode_cat_cols(df, label_encoders, cat_cols):
    for col in cat_cols:
        df[col] = label_encoders[col].transform(list(df[col].values))

    return df
