# Ephys compression results

This capsule reproduces the results for the: "Compression strategies for large-scale electrophysiology data" paper.


### Installation

The capsule can be run using the `Dockerfile` in the `environment` folder.

### Data

The scripts in the `code` assume that the `ephys-compression-result` asset is available in the `data` folder, containing the data produced by the following scripts in the [ephys-compression](https://github.com/AllenNeuralDynamics/ephys-compression/tree/c89e8e481435f39e3bf041bfc0eaac5ef6d93900) repo:

- `data/results-lossless`: 
  - [benchmark-lossless.py](https://github.com/AllenNeuralDynamics/ephys-compression/blob/c89e8e481435f39e3bf041bfc0eaac5ef6d93900/scripts/benchmark-lossless.py)
  - [benchmark-lossless-delta.py](https://github.com/AllenNeuralDynamics/ephys-compression/blob/c89e8e481435f39e3bf041bfc0eaac5ef6d93900/scripts/benchmark-lossless-delta.py)
  - [benchmark-lossless-preprocessing.py](https://github.com/AllenNeuralDynamics/ephys-compression/blob/c89e8e481435f39e3bf041bfc0eaac5ef6d93900/scripts/benchmark-lossless-preprocessing.py)
- `data/results-lossy-exp`: [benchmark-lossy-exp.py](https://github.com/AllenNeuralDynamics/ephys-compression/blob/c89e8e481435f39e3bf041bfc0eaac5ef6d93900/scripts/benchmark-lossy-exp.py)
- `data/results-lossy-sim`: [benchmark-lossy-sim.py](https://github.com/AllenNeuralDynamics/ephys-compression/blob/c89e8e481435f39e3bf041bfc0eaac5ef6d93900/scripts/benchmark-lossy-sim.py)


### Code

In the `code` folder, there are 3 jupyter notebooks to reproduce all figures and results in the "Results" section of the paper:

- `code/lossless.ipynb`: reproduces lossless results (Figures 1-8, S1-S3)
- `code/lossy.ipynb`: reproduces lossy results (Figures 9-14, S4-S8)
- `code/lossy-figurl-visualizations.ipynb`: reproduces [Figurl](https://github.com/flatironinstitute/figurl) visualization web links of Appendix A

The notebooks can be run with the `code/run` bash script.

### Results

The `code/run` will generate html files for each notebook, a `figures` folder with PDF figures in the manuscript, and a 
`visualization_output.json` and `viz_latex.txt` with the Figurl links in JSON and LaTeX (as it appears in Appendix A) formats.

Note that the PDF figures have been manually modified (annotations, colors) for the final published version.
