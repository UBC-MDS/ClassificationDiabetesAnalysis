# Contributing to the Diabetes Predictor project

We welcome any input, feedback, bug reports, and contributions via [Diabetes Predictor Py GitHub Repository](https://github.com/UBC-MDS/diabetes_predictor_py). Your participation helps improve this project and ensures its continued success.

All contributions, suggestions, and feedback are accepted under the [Project's license](./LICENSE.md). By contributing, you represent that you own or have the authority to submit the contribution under the [Project's license](./LICENSE.md). All feedback, suggestions, or contributions are not confidential. The project abides by the [UBC-MDS Code of Conduct](https://ubc-mds.github.io/resources_pages/code_of_conduct/).

## How To Contribute Code to Diabetes Predictor Py

### Setting Up Your Environment

To contribute, you must first be invited by the administrators of the [UBC-MDS GitHub organization](https://github.com/UBC-MDS). Once you have access:

1. **Clone the Repository**  
   Fork the `diabetes_predictor_py` repository on GitHub, then clone your fork to your local machine. For more details on forking, see the [GitHub Documentation](https://help.github.com/en/articles/fork-a-repo).

   ```bash
   git clone https://github.com/YOUR-USERNAME/diabetes_predictor_py.git
   ```

2. **Set Up Your Environment**  
   The project includes both `conda-lock.yml` and `environment.yml` files for managing dependencies. Use `conda` to set up your environment:

   ```bash
   conda env create -f environment.yml
   conda activate diabetes_predictor_py
   ```

   Alternatively, use `conda-lock` if required for environment replication:

   ```bash
   conda-lock install --name diabetes_predictor_py
   ```

3. **Sync Your Fork**  
   To keep your fork up-to-date with changes in the main repository, use the [fetch upstream button on GitHub](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork).

### Creating a Branch

Before making changes, create a new branch for your work:

```bash
git switch -c <your-branch-name>
```

With this branch checked out, make the desired changes to the project.

### Creating a Pull Request

When you're ready to submit your changes:

1. **Commit Your Changes**  
   Add and commit your changes to the new branch:

   ```bash
   git add <modified-files>
   git commit -m "Descriptive message about your changes"
   git push origin <your-branch-name>
   ```

2. **Submit a Pull Request**  
   Go to the GitHub repository page and create a pull request (PR) from your branch to the main repository. Follow these steps:
   - Provide a clear description of the changes you made and their purpose.
   - Tag an administrator as a reviewer to ensure your PR is reviewed promptly.

   For detailed instructions, refer to [Creating a Pull Request](https://help.github.com/en/articles/creating-a-pull-request).

3. **Communicate in the Pull Request**  
   Use the PR discussion thread to communicate with reviewers and collaborators. Respond to feedback and push updates to your branch as needed.

### Getting Your PR Merged

After submitting your Pull Request (PR), reviewers may provide feedback or request changes. Make the necessary updates in your branch and push the changes to automatically update the PR. Once your PR is approved, you will be able to merge it into the main branch.

## Additional Notes

- Please follow existing code style and conventions in the project.
- Update relevant documentation (if applicable) as part of your PR.
- Ensure new features are thoroughly tested and maintain existing functionality.

Thank you for contributing to Diabetes Predictor Py! Your efforts help make this project better for everyone :) 
