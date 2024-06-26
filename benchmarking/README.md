# Benchmarking

This instrument provides two python scripts which are designed to simplify CCD (Code Clone Detection) algorithms performance and recall evaluation.

## benchmarking.py

This is a low-level tool which is capable of running a single benchmark against specific algorithm.

```shell
$ python benchmarking.py --help
usage: benchmarking [-h] -a {nicad} [-c COUNT] -m {direct,cross} [-o MUTATED_FOLDER_PATH] -s MUTATIONS_SPECIFICATION [-i ITERATIONS_COUNT] folder_path

Code clones benchmarking tool

positional arguments:
  folder_path

options:
  -h, --help            show this help message and exit
  -a {nicad}, --algorithm {nicad}
  -c COUNT, --count COUNT
  -m {direct,cross}, --mode {direct,cross}
  -o MUTATED_FOLDER_PATH, --mutated-folder-path MUTATED_FOLDER_PATH
  -s MUTATIONS_SPECIFICATION, --mutations-specification MUTATIONS_SPECIFICATION
  -i ITERATIONS_COUNT, --iterations-count ITERATIONS_COUNT
```

For instance, to benchmark `NiCaD` against clones generated by `any:10` mutation specification one can run

```shell
python benchmark --algorithm nicad -m direct -o mutated -s "any:10"
```

Setting `mode` to `cross` will invoke recall evaluation across mutated clones; setting to `direct` will force checking original files against mutated files.

## pipeline.py

This is a high-level benchmarking pipelining tool which is designed to automate comparison different benchmark invocations.

```shell
$ python pipeline.py --help
usage: pipeline [-h] -c CONFIGURATION

Code clones benchmarking pipeline running tool

options:
  -h, --help            show this help message and exit
  -c CONFIGURATION, --configuration CONFIGURATION
```

You should take a look at `pipelines/nicad-baseline` for the reference `configuration` file format.

## Notes

These tools were tested against CPython 3.11.1, although other versions are highly likely to be working too
