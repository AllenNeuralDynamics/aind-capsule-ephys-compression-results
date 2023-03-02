# Ephys compression results

This capsule reproduces the results for the: "Compression strategies for large-scale electrophysiology data" paper.

### Data

The `code/run` script produces figures and html pages to reproduce the "Results" section of the paper.
The scripts assume that the `ephys-compression-result` asset is available in the `data` folder, containing the data produced by the following capsules:

- `data\results-lossless`: [ephys-lossless-compression-benchmark](...)
- `data\results-lossy-exp`: [ephys-lossy-compression-exp-benchmark](...)
- `data\results-lossy-sim`: [ephys-lossy-compression-sim-benchmark](...)
