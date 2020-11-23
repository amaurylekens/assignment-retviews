[![Build Status](https://travis-ci.com/amaurylekens/assignment-retviews.svg?branch=main)](https://travis-ci.org/amaurylekens/assignment-retviews)
[![codecov](https://codecov.io/gh/amaurylekens/assignment-retviews/branch/main/graph/badge.svg?token=K6OFEUA07Q)](https://codecov.io/gh/amaurylekens/assignment-retviews)


# assignment-retviews

## requirements

### Python packages

* pyspark
* pymongo
* cerberus

### Others

* pyspark
* mongodb

## Launch

For the two project, a version of mongodb must run locally. On ubuntu (18.0.4) we launch the database with the following command:

```bash
sudo service mongod start
```

You have too create a data directory and put the data files in it:

```bash
cd assignment-retviews
mkdir data
```

### Data processing

We launch the data processing app with:

```bash
python3 data_processing.py
```

### Basics stats

We launch the app calculating basic stats with:

```bash
python3 compute_stats.py
```

