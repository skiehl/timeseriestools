# timeseriestools
Python tools for time series analysis.

## Functions

* Functions in `dataflagging.py`:
    * `smart_binning():` Smart binning of unevenly sampled data.
    * `split_data():` Split time series data into segments at large time gags.
* Functions in `datasampling.py`:
    * `mask_outliers()`: Identify outliers.
    * `mask_largeunc()`: Identify data points with excessive uncertainties.

## License

timeseriestools is licensed under the BSD 3-Clause License - see the
[LICENSE](https://github.com/skiehl/timeseriestools/blob/main/LICENSE) file.
