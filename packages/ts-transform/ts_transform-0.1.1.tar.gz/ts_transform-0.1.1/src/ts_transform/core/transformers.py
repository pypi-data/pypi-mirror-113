import sys

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class TimeSeriesTransform:
    def __init__(self, df: pd.DataFrame, target: list, n_in=5, n_out=5):
        """Index must be pandas datetime"""
        self.n_in = n_in
        self.n_out = n_out
        self.target = target  # must be an input feature
        self.features = list(df.columns)
        for t in self.target:
            if t not in self.features:
                raise (
                    TypeError(
                        f"""{t} not in {self.features}.
                        Target must be an input feature"""
                    )
                )

        if not isinstance(df.index, pd.DatetimeIndex):
            index_type = type(df.index)
            raise (
                TypeError(
                    f"""
            Index must be of pandas.DatetimeIndex.
            dataframe is of type: {index_type}
            """
                )
            )
        else:
            self.data = df.sort_index()

        self.timestep = abs(self.data.index[0] - self.data.index[1])

    def _validate_roll_self(self, verbose=False):
        """Ensures data rolled properly.
        Example, t-3 is actually t-3, and not t+3, for example.
        """
        # test that rolling happened appropriately...
        print(f"DATASET_TIMESTEP_VALUE: {self.timestep}")
        valids = []
        for idx, row in self.data.tail().iterrows():
            # idx is current time
            # validate n timesteps
            n = 3
            if self.data.shape[0] <= n:
                n = n - 1
            digits_n_in = len(str(self.n_in))
            for i in range(1, n + 1):
                _var = f"{self.target[-1]}(t-{abs(i):0{digits_n_in}d})"
                historical_rolled_value = row[_var]
                _var_time = idx - (self.timestep * i)
                _var_idx = self.data.index.get_loc(_var_time)
                _t0 = self.data.iloc[_var_idx, :][
                    f"{self.target[-1]}(t-{0:0{digits_n_in}d})"
                ]
                valids.append(_t0 == historical_rolled_value)
                if verbose:
                    print(f"{_var}")
                    print(f"{idx}: {historical_rolled_value}")
                    print(f"{_var_time}: {_t0}")
        if not all(valids):
            raise (TypeError("Rolling failed"))
        else:
            print("Validation successful")

    def min_max_scale(self):
        def helper(row):
            x = row.values.reshape(-1, 1)
            scaler = MinMaxScaler(feature_range=(0, 1))
            transformed = scaler.fit_transform(x)
            row_vals = transformed.reshape(row.shape)
            return pd.Series(row_vals, index=row.index)

        for feature in self.features:
            cols = self.feature_meta[feature]["features"]
            # determine if target in features
            if feature in self.target:
                print(f"{feature} is target feature")
                tgt_cols = [c for c in cols if "+" in c]
                df_subset = self.data[tgt_cols]
                self.data[tgt_cols] = df_subset.apply(helper, axis=1)
                cols = [c for c in cols if "+" not in c]
                print(f"reassigned historical features for {feature}")
            print(f"Scaling feature {feature}")
            df_subset = self.data[cols]
            self.data[cols] = df_subset.apply(helper, axis=1)

    def scale_to_t0(self):
        # scale all values as a percentage of t0
        for feature in self.features:
            t0_feature = f"{feature}(t00)"
            cols = self.feature_meta[feature]["features"]
            df_subset = self.data[cols]
            self.data[cols] = df_subset.div(df_subset[t0_feature], axis=0)

    # convert series to supervised
    def ts_to_supervised(
        self, target: list, train=True, dropnan: str = "all", verbose=True
    ):
        """Converts time series dataframe for input features and output features.
        Index must be time component.
        Args:
            df (pd.DataFrame): [description]
            target (list): List of column names to frame as output features.
            n_in (int, optional): Number of input timesteps to calculate. Defaults to 1.
            n_out (int, optional): Number of output timesteps to calculate. Defaults to 1.
            dropnan (bool, optional): [description]. Defaults to True.
            train (bool, optional): [description]. Defaults to True.

        Returns:
            [type]: [description]
        """
        df = self.data
        n_in = self.n_in
        if train:
            n_out = self.n_out
        else:
            n_out = 0

        input_features = self.features

        # create skeleton of output_df
        col_names_kv = self.create_col_names(
            n_in=n_in,
            n_out=n_out,
            features=input_features,
            output_features=target,
        )
        output_df = pd.DataFrame(
            index=df.index,
            columns=np.arange(
                0, len(input_features) * n_in + len(target) * n_out, 1
            ),
        )
        print("\nProcessing input sequences")
        _i = 0
        digits_n_in = len(str(n_in))
        digits_n_out = len(str(n_out))
        for i in range(-n_in + 1, 1, 1):
            _df = df.shift(-i)
            _df.columns = [
                f"{f}(t-{abs(i):0{digits_n_in}d})" for f in input_features
            ]
            for _col in _df.columns:
                col_num = col_names_kv[_col]
                output_df.iloc[:, col_num] = _df[_col].values

            if verbose:
                status = round(_i / n_in, 2)
                sys.stdout.write(f"\r Progress....{status}")
                sys.stdout.flush()
            _i += 1

        if train:
            # forecast sequence (t+1, ... t+n)
            print("\nProcessing output sequences")
            _i = 0
            for i in range(1, n_out + 1, 1):
                names = [f"{f}(t+{i:0{digits_n_out}d})" for f in target]
                _df = df[target].shift(-i)
                _df.columns = names
                for _col in _df.columns:
                    col_num = col_names_kv[_col]
                    output_df.iloc[:, col_num] = _df[_col].values

                status = round(_i / n_out, 2)
                # sys.stdout.write("\r Progress....{}".format(round(status,2)))
                # sys.stdout.flush()
                _i += 1

        # rename columns
        rev_col = {v: k for k, v in col_names_kv.items()}
        output_df.columns = [rev_col[x] for x in output_df.columns]
        # drop rows with NaN values
        if dropnan == "all":
            output_df.dropna(
                inplace=True,
            )
        elif dropnan == "historical":
            output_df.dropna(
                inplace=True,
                subset=[
                    x for x in output_df.columns if "t-" in x
                ],  # dont drop nan for target features
            )

        print(f"\nNumber of supervised records: {output_df.shape[0]}")

        self.data = output_df
        if train:
            self._validate_roll_self()

    def create_col_names(
        self, n_in: int, n_out: int, features: list, output_features: list
    ) -> list:
        """Creates sequence of names for all features.
        e.g. (t-10)price, (t-10)name, (t-9)price

        Args:
            n_in (int): [description]
            n_out (int): [description]
            features (list): [description]
            output_features (list): [description]

        Returns:
            list: [description]
        """
        feature_meta = {f: {"features": []} for f in features}

        digits_n_in = len(str(n_in))
        digits_n_out = len(str(n_out))

        input_names = []
        output_names = []
        for i in range(-n_in + 1, 1, 1):
            for f in features:
                ts_name = f"{f}(t-{abs(i):0{digits_n_in}d})"
                feature_meta[f]["features"].append(ts_name)
                # ts_names = [f"{f}(t{i:0{digits_n_in}d})" for f in features]
                input_names.append(ts_name)
        for o in range(1, n_out + 1, 1):
            for f in output_features:
                ts_name = f"{f}(t+{o:0{digits_n_out}d})"
                feature_meta[f]["features"].append(ts_name)
                # ts_name = [f"{f}(t+{o:0{digits_n_out}d})" for f in output_features]
                output_names.append(ts_name)
        all_names = input_names + output_names
        kv = {v: k for k, v in enumerate(all_names)}
        self.col_names = kv
        self.feature_meta = feature_meta
        self.target_features = output_names
        return kv

    def tensor_reshape(self):
        """[samples (observations), timesteps, features]"""
        x_train_shape = self.train_X.shape
        x_test_shape = self.test_X.shape
        y_train_shape = self.train_y.shape
        y_test_shape = self.test_y.shape

        self.train_X = self.train_X.values.reshape(
            (self.train_X.shape[0], self.n_in, len(self.features))
        )
        self.train_y = self.train_y.values.reshape(
            (self.train_y.shape[0], self.n_out, len(self.target))
        )
        self.test_X = self.test_X.values.reshape(
            (self.test_X.shape[0], self.n_in, len(self.features))
        )
        self.test_y = self.test_y.values.reshape(
            (self.test_y.shape[0], self.n_out, len(self.target))
        )
        print(f"train_X shape: {x_train_shape} -->  {self.train_X.shape}")
        print(f"test_X shape: {x_test_shape} -->  {self.test_X.shape}")
        print(f"train_y shape: {y_train_shape} -->  {self.train_y.shape}")
        print(f"test_y shape: {y_test_shape} -->  {self.test_y.shape}")

    def normalize_sequences(self):
        """min-max scale each feature-observation

        Returns:
            [type]: [description]
        """
        return ""

    def get_X_y_transformed(self):
        return self.train_X, self.train_y, self.test_X, self.test_y

    def tscv(self, train=0.95):
        # tscv - time series cross validation
        rows = self.data.shape[0]
        traincut = int(rows * train)

        train = self.data.values[:traincut, :]
        test = self.data.values[traincut:, :]
        # the outcome variable (y) will be in position [,-n_out:]
        # i.e. the outcome variable is on right end of the matrix
        self.train_X = tensor_shape(
            train[:, : -self.n_out], self.n_in, self.features
        )
        self.train_y = train[:, -self.n_out :]

        self.test_X = tensor_shape(
            test[:, : -self.n_out], self.n_in, self.features
        )
        self.test_y = test[:, -self.n_out :]

        del self.data

    def to_binary_clf(self, drop_regression_targets=True, fun=None):
        """Only works for single outcome variable. Defaults to the last outcome pred in list.
        fun = function to determine binary outcome variable
        """
        output_features = self.feature_meta[self.target[0]]["features"][
            -self.n_out :
        ]
        binary_target = output_features[-1]
        output_features.remove(binary_target)

        # drop all the output features except the one we are using for binary classification
        if len(output_features) > 1 and drop_regression_targets:
            self.data.drop(output_features, axis=1, inplace=True)
            print(f"DROPPED COLUMNS: {output_features}")

        digits_n_in = len(str(self.n_in))
        t0 = f"{self.target[-1]}(t-{0:0{digits_n_in}d})"
        # True if gain
        self.y_binary_clf = (
            (self.data[f"{binary_target}"] - self.data[t0]) > 0
        ).astype(int)
        self.binary_target = binary_target

    def X_y_split(self) -> tuple:
        """Forecasted features are 'y'. The rest are X.

        Return: (X, y)
        """
        columns = list(self.data.columns)
        y = []
        X = []
        for col in columns:
            if "t+" in col:
                y.append(col)
            else:
                X.append(col)

        return self.data[X], self.data[y]

    def train_test_split(self, n_test):
        X, y = self.X_y_split()

        self.train_X = X[:-n_test]
        self.train_y = y[:-n_test]

        self.test_X = X[-n_test:]
        self.test_y = y[-n_test:]


def tensor_shape(dataset, n_in, features):
    # Shape data for LSTM input
    """tensor should be (t-2)a, (t-2)b, (t-1)a, (t-1)b, etc.
    where a and b are features to properly reshape"""
    shaped = dataset.reshape(dataset.shape[0], n_in, len(features))
    return shaped
