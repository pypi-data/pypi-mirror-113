# Fast Sketches

While implementing a paper, we had to create a new library for Count-Min Sketches and Count-Sketches, as current solutions were inadequate. C++ libraries are difficult to use, and Python packages tend to be slow. Thus, we wrote a Python package that contains Python bindings to a C++ library to calculate the predictions of the count-min sketch and count-sketches. This code is located in `fast_sketches.cpp`.

- [Fast Sketches](#fast-sketches)
  - [Installation](#installation)
  - [Usage](#usage)

## Installation

To install the package, one simply only needs to run

```
pip install fast_sketches
```

## Usage

```
[numpy array of long longs] cm_sketch_preds(int nhashes, [numpy array of long longs] np_input, ll width, int seed)
```

takes as input

1. **nhashes:** The number of hash functions used in the sketch
1. **np_input:** The numpy array containing the frequencies of each key (note that order doesn't matter)
1. **width:** The width of the sketch, or the number of entries in each row of the sketch
1. **seed:** A random seed.

Then, it outputs what a count-min sketch would give as predicted frequencies with that particular set of parameters, where the output prediction at index i corresponds to the key in np_input at index i. For example, if np_input was [3, 4, 5], the output might also be [3, 4, 5], but it could not be [4, 3, 5], by the conservative nature of the sketch.

```
[numpy array of doubles] count_sketch_preds(int nhashes, [numpy array of long longs] np_input, ll width, int seed)
```

performs the same function for the Count-Sketch, with parameters:

1. **nhashes:** The number of hash functions used in the sketch
1. **np_input:** The numpy array containing the frequencies of each key (note that order doesn't matter)
1. **width:** The width of the sketch, or the number of entries in each row of the sketch
1. **seed:** A random seed.

Note one key difference, however: the output is in **doubles**, because the count-sketch takes medians, which sometimes leads to half-integer outputs!
