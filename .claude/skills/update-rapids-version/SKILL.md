---
name: update-rapids-version
description: Updates python code (e.g. internal api calls) so that tests pass after running in conda environment with updated rapids version.  
---

You will be running in an already activated conda environment with the update rapids dependencies.

Make necessary code changes in the `python` directory tree to get the following test script to complete without error:

```bash
cd python && CUDA_VISIBLE_DEVICES=0 bash run_test.sh
```

1.  Fix any formatting errors reported by the script.
2.  Fix any type-checking errors reported.
3.  Fix all other pytest errors reported.   
    - Note that pytest phase runs through all tests before reporting any errors.   This can take a while.
    - Most failures will be due to changes to internal apis in cuML that we rely on.


Iterate on 1., 2., and 3. until script succeeeds.   The script can take a while to complete.

For 3., when working on individual tests, especially if only a few are failing, it is faster to run only these tests via pytest directly, followed by a final full run.

You may search the source code in the directory `../cuml` for relevant internal api changes.  The branch for the desired version is checked out.
