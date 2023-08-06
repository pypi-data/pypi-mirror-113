# SDVI Decision Engine Rally Module

A collection of classes and functions for interacting with SDVI Rally APIs.

Refer to documentation found in your Rally Silo.

### v0.1.3 -- released 20 Jul 2021

#### Features

- Add `asset_name` argument to `jobs.get_job_report` method. This allows users to retrieve QC or analyze data from 
  arbitrary assets using the supplied provider type and label.

#### Fixes

### v0.1.2 -- released 22 June 2021

#### Features

- Add `files.write_files` method that offers parallel writing of files given a dict of URLs and content
- Add `files.read_files` method that offers parallel reading of files given a sequence of URLs
  **Caution should be used when reading multiple files**
- `files.list_files` now returns both files and (subdirectories) at the specified url.
- Add License-only deadline argument `step_deadline_lic_only` to `supplyChain.SupplyChainStep`
- `SupplyChainSplit` and `SupplyChainCancel` can now take a `SupplyChainSequence`

#### Fixes

- `SupplyChainStep` now correctly recognizes `provider_filter` values

### v0.1.1 -- released 16 Mar 2021

#### Features

- Initial Beta offering.
