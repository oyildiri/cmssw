# Job Submission, Harvesting, and Plotting Guide

The workflow consists of four steps:

1. Configure the user-specific paths.
2. Define the runs to be executed.
3. Submit jobs to HTCondor and harvest the results.
4. Generate performance plots from the harvested output.

## 1. Run Definition

A **run** represents a particular test of a vertex reconstruction algorithm on a specified simulated dataset, with an optional parameter configuration.

Internally, each run is represented by:

```python
run = [inter, algo, group, type, param, tag, path]
```

The elements are defined as follows:

| Element | Description |
|---|---|
| `inter` | Identifier for the simulated particle interaction (dataset). |
| `algo` | Identifier for the vertex reconstruction algorithm being tested. |
| `group` | User-defined name used to organize related runs. |
| `type` | Specifies how the algorithm configuration is varied. |
| `param` | Value(s) of the parameter(s) specified by `type`. |
| `tag` | Automatically generated identifier for the run's output directory. |
| `path` | Automatically generated path to the run's output directory. |

The user specifies `inter`, `algo`, `group`, `type`, and, when necessary, `param`. The scripts determine `tag` and `path` automatically.

### 1.1. Particle interaction (`inter`)

The `inter` identifier selects the simulated dataset to be processed.

Each identifier corresponds to a text file containing paths to the simulation data. Each line in the file specifies one input data path.

For example, `TT` selects `TT.txt`, which contains the paths to simulation data for top–antitop quark production.

The following identifiers are currently supported:

| `inter` | Input file |
|---|---|
| `Hinv` | `Hinv.txt` |
| `QCD` | `QCD.txt` |
| `TTto2l2nu` | `TTto2l2nu.txt` |
| `TT` | `TT.txt` |
| `Upsilon` | `Upsilon.txt` |
| `Wprimetolnu` | `Wprimetolnu.txt` |
| `Wtolnu` | `Wtolnu.txt` |
| `Wtomunu` | `Wtomunu.txt` |
| `Zprimetoee` | `Zprimetoee.txt` |
| `Zprimetomm` | `Zprimetomm.txt` |
| `Ztoee` | `Ztoee.txt` |
| `Ztomm` | `Ztomm.txt` |
| `Ztott` | `Ztott.txt` |

These text files are located in the `test` directory, alongside the configuration, submission, harvesting, and plotting scripts.

### 1.2. Algorithm (`algo`)

The `algo` identifier selects the vertex reconstruction algorithm to be tested.

Each identifier corresponds to a Python configuration script.

| `algo` | Configuration script |
|---|---|
| `oldColdF` | `testCPU_PU200_oldAlgo.py` |
| `oldCnewF` | `testCPU_PU200_oldCnewF.py` |
| `newColdF` | `testCPU_PU200_newColdF.py` |
| `newCnewF` | `testCPU_PU200.py` |
| `new2CnewF` | `testCPU_PU200_tkwt0p25.py` |
| `4DinBlocks` | `PrimaryVertexProducer4D_inBlocks.py` |
| `4D` | `PrimaryVertexProducer4D.py` |

For the first five configurations, `C` and `F` refer to the clusterizer and fitter, respectively. The prefixes `old` and `new` distinguish different implementations.

### 1.3. Group (`group`)

The `group` is a user-defined name used to organize related runs.

For example, when testing the effect of different `mintrkweight` values, the group could be named:

```text
mintrkweight
```

Runs sharing the same dataset, algorithm, and group are stored together, allowing multiple parameter configurations to be compared easily.

### 1.4. Run type (`type`) and parameter (`param`)

The `type` determines how a run's algorithm configuration is specified. The corresponding parameter value is stored in `param`.

Three run types are currently supported:

| `type` | Description | `param` format |
|---|---|---|
| `I` | Run without specifying a varied parameter. | `None` |
| `P` | Specify a numerical parameter value. | `float` |
| `B2` | Specify two Boolean values. | `[bool, bool]` |

**Type `I` — Individual run**

Used when no parameter variation is specified.

```python
type = "I"
param = None
```

**Type `P` — Numerical parameter**

Used to specify a numerical value for a configurable algorithm parameter, such as `mintrkweight`.

```python
type = "P"
param = 0.25
```

Multiple runs can be created with different parameter values to study their effects on the reconstruction performance.

**Type `B2` — Two Boolean parameters**

Used when the configuration depends on two Boolean values.

For example, in the 4D reconstruction algorithm, these values can specify whether `inBlocks` is enabled in the first and second vertex reconstruction iterations.

```python
type = "B2"
param = [False, True]
```

In this example, `inBlocks` is disabled in the first iteration and enabled in the second.

### 1.5. Run tag (`tag`) and output path (`path`)

Each run is assigned a `tag` that determines the name of its output directory.

The directory name follows the convention:

```text
run_<tag>
```

The tag is generated automatically and should not be specified manually.

The naming convention depends on the run type:

- `I`: Sequential integer tags, such as `1`, `2`, `3`, etc.
- `P`: A tag of the form `p_<param_value>`, where `<param_value>` is the numerical parameter value.

The `path` is also generated automatically from the output directory structure described below.

## 2. Output Directory Structure

All run outputs are stored in the user's designated EOS location.

The directory structure is:

```text
<mainpath>/
└── OldNewCF/
    └── <inter>/
        └── <algo>/
            └── RUNS_<group>/
                ├── run_<tag1>/
                │   └── output.root
                ├── run_<tag2>/
                │   └── output.root
                └── ...
```

Here, `<mainpath>` is the user-configured base output directory.

For example, a run using the `TT` dataset, `newCnewF` algorithm, `mintrkweight` group, and parameter value `0.25` would have the following directory structure:

```text
<mainpath>/
└── OldNewCF/
    └── TT/
        └── newCnewF/
            └── RUNS_mintrkweight/
                └── run_p_0.25/
                    └── output.root
```

The harvested DQM file is also saved in the corresponding run directory.

## 3. Initial Configuration

Before using the submission, harvesting, or plotting scripts, open:

```text
jobScriptsConfig.py
```

Set the following variables:

| Variable | Description |
|---|---|
| `user` | Your CERN username. |
| `mainpath` | Absolute path to the base directory on EOS where `OldNewCF` will be created. |
| `workarea` | Absolute path to the `test` directory containing the configuration, submission, harvesting, and plotting scripts. |

These paths must be configured correctly before running any of the scripts.

## 4. Specifying Runs Using Runlists

A **runlist** is a text file used to specify one or more runs.

Each line represents a single run. Runlists can be passed to the submission, harvesting, and plotting scripts, making it possible to reuse the same set of run definitions throughout the workflow.

The syntax depends on the run type.

### 4.1. Type `I`

```text
<inter>/<algo>/<group>/I
```

Example:

```text
Hinv/oldCnewF/clust_test/I
```

This defines a run using the `Hinv` dataset and `oldCnewF` algorithm, belonging to the `clust_test` group, without a specified parameter variation.

### 4.2. Type `P`

```text
<inter>/<algo>/<group>/P/<param>
```

Example:

```text
TT/new2CnewF/mintrkweight/P/0.27
```

This defines a run using the `TT` dataset and `new2CnewF` algorithm, with a numerical parameter value of `0.27`.

### 4.3. Type `B2`

```text
<inter>/<algo>/<group>/B2/<bool1>/<bool2>
```

Example:

```text
QCD/4DinBlocks/inBlocksTest/B2/False/True
```

This defines a run using the `QCD` dataset and `4DinBlocks` algorithm, with `inBlocks` disabled in the first iteration and enabled in the second.

### 4.4. Example runlist

A runlist named `run_list.txt` could contain:

```text
TT/newCnewF/mintrkweight/P/0.1
TT/newCnewF/mintrkweight/P/0.2
TT/newCnewF/mintrkweight/P/0.3
TT/newCnewF/mintrkweight/P/0.4
TT/newCnewF/mintrkweight/P/0.5
```

This specifies five runs using the same dataset and algorithm, each with a different parameter value.

The same runlist can subsequently be used to submit jobs, harvest their outputs, and produce comparison plots.

## 5. Job Submission

The script `submitJobs_new.py` submits the specified runs as HTCondor jobs.

There are several ways to specify runs.

### 5.1. Submission using a runlist (recommended)

The most straightforward method is to provide a runlist:

```bash
python3 submitJobs_new.py --run_path_list run_list.txt
```

This submits all runs listed in `run_list.txt`.

Using a runlist is recommended when submitting multiple runs, particularly when their configurations differ.

### 5.2. Submitting a type `I` run using command-line arguments

A type `I` run can be submitted directly without creating a runlist:

```bash
python3 submitJobs_new.py --inter TT --algo newCnewF --group test2
```

When no parameter arguments are supplied, the run is automatically treated as type `I`.

### 5.3. Submitting type `P` runs with explicitly specified values

To submit several runs with selected numerical parameter values, use `--params`:

```bash
python3 submitJobs_new.py --inter TT --algo newCnewF --group mintrkweight --params 0.1 0.25 0.40 0.50
```

This creates four runs, one for each specified parameter value.

### 5.4. Submitting type `P` runs with equally spaced values

Alternatively, use `--param_min`, `--param_max`, and `--param_num` to generate an evenly spaced sequence of parameter values:

```bash
python3 submitJobs_new.py --inter TT --algo newCnewF --group mintrkweight --param_min 0.1 --param_max 0.5 --param_num 10
```

The arguments specify:

- `--param_min`: Minimum parameter value.
- `--param_max`: Maximum parameter value.
- `--param_num`: Number of parameter values to generate.

In this example, 10 equally spaced parameter values between `0.1` and `0.5` are used.

## 6. Harvesting DQM Output

After the submitted jobs have completed, their DQM output files must be merged for each run.

This is handled by:

```text
harvestJobs_new.py
```

The harvesting script accepts run specifications in the same way as the submission script.

For example, to harvest all runs in a runlist:

```bash
python3 harvestJobs_new.py --run_path_list run_list.txt
```

The merged DQM file is saved in the corresponding run directory, with a name following the convention:

```text
DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root
```
## 7. Plotting Performance Histograms

The script `perfOpt_hist.py` is used to generate performance histograms from the harvested DQM files.

Unlike the submission and harvesting scripts, runs must be specified using a runlist.

Example:

```bash
python3 perfOpt_hist.py --run_path_list run_list.txt --foldername plots --firstline 1 --lastline 10
```

The command-line arguments are:

| Argument | Description |
|---|---|
| `--run_path_list` | Path to the text file containing the run definitions. |
| `--foldername` | Name of the directory in which the generated plots will be saved. |
| `--firstline` | First line of the runlist to include in the plots. |
| `--lastline` | Last line of the runlist to include in the plots. |

The selected runs are plotted together on the same histograms, allowing direct comparisons between algorithm configurations or parameter values.

For example, when a runlist contains several `mintrkweight` configurations, the script can be used to compare their vertex reconstruction performance.

## 8. Complete Workflow Example

The following example illustrates a typical parameter scan of `mintrkweight` using the `TT` dataset and `newCnewF` algorithm.

**Step 1 — Configure the paths**

Set `user`, `mainpath`, and `workarea` in `jobScriptsConfig.py`.

**Step 2 — Create a runlist**

Create a text file named `run_list.txt`:

```text
TT/newCnewF/mintrkweight/P/0.1
TT/newCnewF/mintrkweight/P/0.2
TT/newCnewF/mintrkweight/P/0.3
TT/newCnewF/mintrkweight/P/0.4
TT/newCnewF/mintrkweight/P/0.5
```

**Step 3 — Submit the jobs**

```bash
python3 submitJobs_new.py --run_path_list run_list.txt
```

**Step 4 — Harvest the results**

Once all jobs have finished:

```bash
python3 harvestJobs_new.py --run_path_list run_list.txt
```

**Step 5 — Generate comparison plots**

```bash
python3 perfOpt_hist.py --run_path_list run_list.txt --foldername mintrkweight_plots --firstline 1 --lastline 5
```

This produces performance histograms comparing the five specified `mintrkweight` values.

The workflow can be repeated for other simulated datasets, reconstruction algorithms, or parameter configurations by changing the runlist entries.
