# Fast Sketches

While implementing a paper, we had to create a new library for Count-Min Sketches and Count-Sketches, as current solutions were inadequate. C++ libraries are difficult to use, and Python packages tend to be slow. Thus, we wrote a Python package that contains Python bindings to a C++ library to calculate the predictions of the count-min sketch and count-sketches. This code is located in `fast_sketches.cpp`.

We include a Python Package that contains Python bindings to a C++ library to calculate the results of the count-min sketch and count-sketches.

NOTE: this only works on Mac in our current version.

First, you will need pybind11, so run

`pip install pybind11`

Then, run

`sh build.sh` to install the sketches library. This library implements two functions:

```
[numpy array of long longs] cm_sketch_preds(int nhashes, [numpy array of long longs] np_input, ll width, int seed)
```

takes as input a random seed, the number of hashes, the width of the sketch (or the number of cells in each row), and the frequencies of each key. Then, it outputs what a count-min sketch would give as predicted frequencies with that particular set of parameters.

For example,

```
[numpy array of long longs] count_sketch_preds(int nhashes, [numpy array of long longs] np_input, ll width, int seed)
```

performs the same function for the Count-Sketch.
