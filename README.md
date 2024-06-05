# timeseriestools
Python tools for time series analysis.

## Functions

* Functions in `dataflagging.py`:
    * `mask_largeunc()`: Identify data points with excessive uncertainties.
    * `mask_outliers()`: Identify outliers.
* Functions in `datasampling.py`:
    * `smart_binning():` Smart binning of unevenly sampled data.
    * `split_data():` Split time series data into segments at large time gags.

## License

timeseriestools is licensed under the BSD 3-Clause License - see the
[LICENSE](https://github.com/skiehl/timeseriestools/blob/main/LICENSE) file.
