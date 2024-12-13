## Test suite developer notes

### Running the tests
Tests are run using the `pytest` command in the root of the project.

### Preparation of test zip files
The test zip files used in `test_read_zip.py` were generated 
by running the `generate_test_zip_files.py` script in the `tests` directory.
These files need to exist in the remote GitHub repository for the tests to pass.
If for some reason they go missing from the remote repository,
we can re-run the `generate_test_zip_files.py` script to re-generate them
and then push them to the remote repository.

```
python tests/generate_test_zip_files.py
```

### Test teardown
`conftest.py` contains the code to delete the files and directories 
created by the tests which need to be deleted at the end of the tests.
