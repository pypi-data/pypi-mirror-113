# Copyright (c) 2020 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# DO NOT COMMIT THIS FILE

from shapelets.dsl.graph import NodeInputParamType, NodeReturnType


def abs(number: NodeInputParamType) -> NodeReturnType:
    """
    Returns the absolute value of any given number
    :param number: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def div(dividend: NodeInputParamType, divisor: NodeInputParamType) -> NodeReturnType:
    """
    Returns the result of executing a division between two numbers.
    :param dividend: DOUBLE
    :param divisor: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def fft(ts: NodeInputParamType) -> NodeReturnType:
    """
    Fast Fourier Transform (FFT). 
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def max(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns the largest of the two numbers.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def min(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns the smallest of the two numbers.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def paa(ts: NodeInputParamType, bins: NodeInputParamType) -> NodeReturnType:
    """
    Piecewise Aggregate Approximation (PAA).
    :param ts: SEQUENCE
    :param bins: INT
    :return output_0: SEQUENCE
    """
    pass


def pow(base: NodeInputParamType, exp: NodeInputParamType) -> NodeReturnType:
    """
    Returns base to the power exp.
    :param base: DOUBLE
    :param exp: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def plus(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns the sum of two numbers.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def minus(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns the difference of two numbers.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def times(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns the product of two expressions.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def zNorm(ts: NodeInputParamType) -> NodeReturnType:
    """
    Description coming soon
    :param ts: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def abs_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Returns a time series with absolute numeric value of each element.
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def div_ts(ts: NodeInputParamType, divisor: NodeInputParamType) -> NodeReturnType:
    """
    Divide each point of a time series by a divisor
    :param ts: SEQUENCE
    :param divisor: DOUBLE
    :return output_0: SEQUENCE
    """
    pass


def equals(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns a Boolean stating whether two expressions are equal.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: BOOLEAN
    """
    pass


def length(ts: NodeInputParamType) -> NodeReturnType:
    """
    Returns the length of a time series.
    :param ts: SEQUENCE
    :return output_0: LONG
    """
    pass


def map_ts(functor: NodeInputParamType, ts: NodeInputParamType) -> NodeReturnType:
    """
    Returns a new Sequence resulting from applying the lambda function to each element of the input Sequence
    :param functor: FUNCTION
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def pow_ts(ts: NodeInputParamType, exp: NodeInputParamType) -> NodeReturnType:
    """
    Returns a time series resulting from applying base to the power exp to each point of the given time series.
    :param ts: SEQUENCE
    :param exp: DOUBLE
    :return output: SEQUENCE
    """
    pass


def to_view(sequence_id: NodeInputParamType, index: NodeInputParamType,
            window_size: NodeInputParamType) -> NodeReturnType:
    """
    Returns a View from a given Sequence using the index and window size to calculate de View size. 
    :param sequence_id: STRING
    :param index: LONG
    :param window_size: LONG
    :return output_0: VIEW
    """
    pass


def plus_ts(ts: NodeInputParamType, value: NodeInputParamType) -> NodeReturnType:
    """
    Returns a time series resulting from the addition of a given value to each point of a time series.
    :param ts: SEQUENCE
    :param value: DOUBLE
    :return output_0: SEQUENCE
    """
    pass


def range_ts(n: NodeInputParamType) -> NodeReturnType:
    """
    Returns a Sequence with n values.
    :param n: LONG
    :return output: SEQUENCE
    """
    pass


def times_ts(ts: NodeInputParamType, value: NodeInputParamType) -> NodeReturnType:
    """
    Returns a time series resulting from the product of a given value to each point of a time series.
    :param ts: SEQUENCE
    :param value: DOUBLE
    :return output_0: SEQUENCE
    """
    pass


def to_match(sequence_id: NodeInputParamType, index: NodeInputParamType, window_size: NodeInputParamType,
             correlation: NodeInputParamType) -> NodeReturnType:
    """
    Returns a new Match from the input arguments
    :param sequence_id: STRING
    :param index: LONG
    :param window_size: LONG
    :param correlation: DOUBLE
    :return output_0: MATCH
    """
    pass


def minus_ts(ts: NodeInputParamType, number: NodeInputParamType) -> NodeReturnType:
    """
    Returns a time series resulting from subtracting each point of a time series by a given value.
    :param ts: SEQUENCE
    :param number: DOUBLE
    :return output_0: SEQUENCE
    """
    pass


def less_than(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns a Boolean stating whether one number is less than the other
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: BOOLEAN
    """
    pass


def reverseTS(ts: NodeInputParamType) -> NodeReturnType:
    """
    Description coming soon
    :param ts: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def remainder(dividend: NodeInputParamType, divisor: NodeInputParamType) -> NodeReturnType:
    """
    Returns the remainder of executing a division between two numbers.
    :param dividend: DOUBLE
    :param divisor: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def reduce_ts(functor: NodeInputParamType, ts: NodeInputParamType) -> NodeReturnType:
    """
    Returns the result as Double of reducing all elements from the input Sequence with the given lambda function
    :param functor: FUNCTION
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def to_double(num: NodeInputParamType) -> NodeReturnType:
    """
    Parses the given number as a Double number and returns the result.
    :param num: DOUBLE
    :return output_0: DOUBLE
    """
    pass


def div_ts_ts(ts_1: NodeInputParamType, ts_2: NodeInputParamType) -> NodeReturnType:
    """
    Division of two time series. Time series must have the same length
    :param ts_1: SEQUENCE
    :param ts_2: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def concat_ts(ts_1: NodeInputParamType, ts_2: NodeInputParamType) -> NodeReturnType:
    """
    Joins two time series along an existing axis.
    :param ts_1: SEQUENCE
    :param ts_2: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def filter_ts(functor: NodeInputParamType, ts: NodeInputParamType) -> NodeReturnType:
    """
    Returns a new Sequence resulting from applying the predicate function to each element of the input Sequence
    :param functor: FUNCTION
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def not_equals(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns a Boolean stating whether two number are not equal.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: BOOLEAN
    """
    pass


def uniques_ts(ts: NodeInputParamType, is_sorted: NodeInputParamType) -> NodeReturnType:
    """
    Finds unique values from an input time series
    :param ts: SEQUENCE
    :param is_sorted: BOOLEAN
    :return output_0: ND_ARRAY
    """
    pass


def trend_test(ts: NodeInputParamType) -> NodeReturnType:
    """
    Trend test for time series. Trends show the general tendency of the data to increase or decrease during a long period of time.
    :param ts: SEQUENCE
    :return output_0: BOOLEAN
    """
    pass


def abs_energy(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the sum over the square values of the given time series.
    :param ts: SEQUENCE
    :return output_0: DOUBLE
    """
    pass


def plus_ts_ts(ts_1: NodeInputParamType, ts_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns a time series resulting from the addition of the two given time series.
    :param ts_1: SEQUENCE
    :param ts_2: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def visvalingam(ts: NodeInputParamType, numPoints: NodeInputParamType) -> NodeReturnType:
    """
    Description coming soon
    :param ts: SEQUENCE
    :param numPoints: INT
    :return output_0: SEQUENCE
    """
    pass


def times_ts_ts(ts_1: NodeInputParamType, ts_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns a time series resulting from the product of the two given time series.
    :param ts_1: SEQUENCE
    :param ts_2: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def minus_ts_ts(ts_1: NodeInputParamType, ts_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns the difference of two time series.
    :param ts_1: SEQUENCE
    :param ts_2: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def splitEveryN(tss: NodeInputParamType, n: NodeInputParamType) -> NodeReturnType:
    """
    Description coming soon
    :param tss: SEQUENCE
    :param n: INT
    :return output_0: LIST:SEQUENCE
    """
    pass


def greater_than(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns a Boolean stating whether one number is greater than the other.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: BOOLEAN
    """
    pass


def adfuller_test(tss: NodeInputParamType) -> NodeReturnType:
    """
    Augmented Dickey-Fuller test
    :param tss: SEQUENCE
    :return output_0: BOOLEAN
    """
    pass


def contains_value(ts: NodeInputParamType, value: NodeInputParamType) -> NodeReturnType:
    """
    Returns a boolean based on whether a given value is contained within a time series.
    :param ts: SEQUENCE
    :param value: DOUBLE
    :return output_0: BOOLEAN
    """
    pass


def decompose_view(view: NodeInputParamType) -> NodeReturnType:
    """
    Returns the elements of the given View: sequence ID, index and end. 
    :param view: VIEW
    :return sequence_id: STRING
    :return index: LONG
    :return end: LONG
    """
    pass


def generateLevels(tss: NodeInputParamType, sizeInBytes: NodeInputParamType,
                   maxLevels: NodeInputParamType) -> NodeReturnType:
    """
    Description coming soon
    :param tss: SEQUENCE
    :param sizeInBytes: LONG
    :param maxLevels: INT
    :return output: LONG
    """
    pass


def get_row_single(ts: NodeInputParamType, at: NodeInputParamType) -> NodeReturnType:
    """
    Returns the index value from the given Sequence.
    :param ts: SEQUENCE
    :param at: LONG
    :return output_0: DOUBLE
    """
    pass


def ergodicity_test(ts: NodeInputParamType) -> NodeReturnType:
    """
    Ergodicity test
    :param ts: SEQUENCE
    :return output_0: BOOLEAN
    """
    pass


def abs_multiple_ts(ts_list: NodeInputParamType) -> NodeReturnType:
    """
    Returns an list of Sequences where with the absolute numeric value of each element of the given time series.
    :param ts_list: LIST:SEQUENCE
    :return output_0: LIST:SEQUENCE
    """
    pass


def zNormOutputList(tss: NodeInputParamType) -> NodeReturnType:
    """
    Description coming soon
    :param tss: SEQUENCE
    :return output: LIST:SEQUENCE
    """
    pass


def filter_nd_array(functor: NodeInputParamType, nd_array: NodeInputParamType) -> NodeReturnType:
    """
    Returns a new NDArray resulting from applying the predicate function to each element of the input NDArray
    :param functor: FUNCTION
    :param nd_array: ND_ARRAY
    :return output_0: ND_ARRAY
    """
    pass


def to_dense_regular(ts: NodeInputParamType) -> NodeReturnType:
    """
    Change time series density type to regular
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def seasonality_test(ts: NodeInputParamType) -> NodeReturnType:
    """
    Seasonality test for time series
    :param ts: SEQUENCE
    :return output_0: BOOLEAN
    """
    pass


def periodicity_test(ts: NodeInputParamType) -> NodeReturnType:
    """
    Periodicity tests for time series.
    :param ts: SEQUENCE
    :return output_0: ND_ARRAY
    """
    pass


def less_than_or_equals(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns a Boolean stating whether one number is less than or equal the other.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: BOOLEAN
    """
    pass


def auto_correlation_ts(ts: NodeInputParamType, maxLag: NodeInputParamType,
                        unbiased: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the autocorrelation of the specified lag for the given time series.
    :param ts: SEQUENCE
    :param maxLag: LONG
    :param unbiased: BOOLEAN
    :return output_0: ND_ARRAY
    """
    pass


def isax_representation(ts: NodeInputParamType, alphabet_size: NodeInputParamType) -> NodeReturnType:
    """
    iSAX Representation. This function should receive a time series which have suffered a z-normalization and a PAA to its z-normalization.
    :param ts: SEQUENCE
    :param alphabet_size: INT
    :return output_0: SEQUENCE
    """
    pass


def approximated_entropy(ts: NodeInputParamType, length: NodeInputParamType,
                         filtering_level: NodeInputParamType) -> NodeReturnType:
    """
    Calculates a vectorized Approximate entropy algorithm (https://en.wikipedia.org/wiki/Approximate_entropy)
    Requires a time series, the length of compared run of data and the filtering level (must be positive).
    :param ts: SEQUENCE
    :param length: INT
    :param filtering_level: FLOAT
    :return output_0: ND_ARRAY
    """
    pass


def max_min_normalization(ts: NodeInputParamType, high: NodeInputParamType, low: NodeInputParamType) -> NodeReturnType:
    """
    Normalizes the given time series according to its minimum and maximum value and adjusts each value within the range [low, high].
    :param ts: SEQUENCE
    :param high: DOUBLE
    :param low: DOUBLE
    :return output_0: SEQUENCE
    """
    pass


def mean_normalization_ts(ts: NodeInputParamType) -> NodeReturnType:
    """
    Normalizes the given time series according to its maximum-minimum value and its mean. 
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def visvalingamOutputList(tss: NodeInputParamType, numPoints: NodeInputParamType) -> NodeReturnType:
    """
    Description coming soon
    :param tss: SEQUENCE
    :param numPoints: INT
    :return output: LIST:SEQUENCE
    """
    pass


def greater_than_or_equals(num_1: NodeInputParamType, num_2: NodeInputParamType) -> NodeReturnType:
    """
    Returns a Boolean stating whether one number is greater than or equal the other.
    :param num_1: DOUBLE
    :param num_2: DOUBLE
    :return output_0: BOOLEAN
    """
    pass


def matrix_profile_self_join(ts: NodeInputParamType, subsequence_length: NodeInputParamType) -> NodeReturnType:
    """
    Calculate the matrix profile between the time series and itself using a subsequence length.
    :param ts: SEQUENCE
    :param subsequence_length: INT
    :return output_0: ND_ARRAY
    """
    pass


def filter_greater_than_value(max_value: NodeInputParamType, array: NodeInputParamType) -> NodeReturnType:
    """
    Returns an array with those values smaller than the given max value
    :param max_value: INT
    :param array: ND_ARRAY
    :return output_0: ND_ARRAY
    """
    pass


def longest_strike_above_mean(ts: NodeInputParamType) -> NodeReturnType:
    """
    Calculates the length of the longest consecutive subsequence in the time series that is bigger than the mean of the time series.
    :param ts: SEQUENCE
    :return output_0: INT
    """
    pass


def contains_value_multiple_ts(ts_list: NodeInputParamType, value: NodeInputParamType) -> NodeReturnType:
    """
    Returns a list of boolean based on whether a given value is contained within a list of time series.
    :param ts_list: LIST:SEQUENCE
    :param value: DOUBLE
    :return output_0: LIST:BOOLEAN
    """
    pass


def decimal_scaling_normalization(ts: NodeInputParamType) -> NodeReturnType:
    """
    Normalizes the given time series according to its maximum value and adjusts each value within the range (-1, 1).
    :param ts: SEQUENCE
    :return output_0: SEQUENCE
    """
    pass


def filter_greater_than_value_list(max_value: NodeInputParamType, values: NodeInputParamType) -> NodeReturnType:
    """
    Returns a list of integer with those values smaller than the given max value
    :param max_value: INT
    :param values: LIST:INT
    :return output_0: LIST:INT
    """
    pass


def mean_normalization_multiple_ts(ts_list: NodeInputParamType) -> NodeReturnType:
    """
    Normalizes the given list of time series according to the maximum-minimum value and mean of each time series. 
    :param ts_list: LIST:SEQUENCE
    :return output_0: LIST:SEQUENCE
    """
    pass


def max_min_normalization_multiple_ts(ts_list: NodeInputParamType, high: NodeInputParamType,
                                      low: NodeInputParamType) -> NodeReturnType:
    """
    Normalizes the given list of time series according to its minimum and maximum value and adjusts each value within the range [low, high].
    :param ts_list: LIST:SEQUENCE
    :param high: DOUBLE
    :param low: DOUBLE
    :return output_0: LIST:SEQUENCE
    """
    pass


def recommendMetadataFeatureSelection(ts: NodeInputParamType) -> NodeReturnType:
    """
    Description coming soon
    :param ts: ND_ARRAY
    :return output_0: ND_ARRAY
    """
    pass


def decimal_scaling_normalization_multiple_ts(ts_list: NodeInputParamType) -> NodeReturnType:
    """
    Normalizes the given list of time series according to its maximum value and adjusts each value within the range (-1, 1).
    :param ts_list: LIST:SEQUENCE
    :return output_0: LIST:SEQUENCE
    """
    pass
