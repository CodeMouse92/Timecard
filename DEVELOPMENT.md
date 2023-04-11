# Developer Guide

## Development Conventions

To ensure code quality, rapid and productive code hand-offs, and minimal bikeshedding,
we use and enforce the following standards and conventions:

- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [PEP 8 Style Guide](https://pep8.org/) (according to [Black](https://black.readthedocs.io/en/stable/))

## Development Environment Setup

We use Python 3.6 and later. On macOS or Linux, this is already installed. For Windows, we strongly recommend
you use the Windows Subsystem for Linux (WSL).

Clone the repository and `cd` into it. Then run the following.

```bash
python3 -m venv venv
venv/bin/pip install --upgrade pip -r requirements.dev.txt
```

This virtual environment (in `venv`) will be used for running the code and testing.

For Windows, we also strongly recommend disabling `autocrlf` in Git, like this:

```bash
git config core.autocrlf false
```

### Commit Hooks

We use commit hooks to automatically run our linters and tests before your
code is pushed to the repository. This may feel like an unnecessary step
at first, but it actually saves you a lot of time waiting on the CI/CD to
check your code for easily corrected errors.

To enable commit hooks, run the following from the root of the repository:

```bash
git config core.hooksPath .githooks
```

That's all! Now, `git commit` and `git push` will run the appropriate hooks.
If you need to bypass these, you can pass the `--no-verify` flag.
However, please think twice before doing this. The CI/CD will still lint
and test your code on remote, and you'll have to either resolve or explicitly
silence any errors before your code can be merged to `main`.

### Commitizen

We enforce [**Conventional Commits**](https://www.conventionalcommits.org/en/v1.0.0/)
in this project.

In our commit hooks and our CI, we use a tool called Commitizen is used to
ensure all commit messages are complaint. **Do not disable this!** We use
Commitizen to automatically advance our semantic version, generate changelogs,
and generally ensure we have good communication surrounding our development.

## Linting

We use Tox to automate linting. In most cases, you can run `tox` to perform both linting and testing
(see next section), or only linting with `tox -e lint`.

### Black

Black automatically formats Python code according to the PEP 8 style guide. To format with Black,
run the following command:

```bash
black .
```

When run automatically as part of Tox or the CI, Black will merely fail if the formatting is
incorrect. It will not actually make changes. This is because the `--check` flag is being passed in
that situation. If it fails, run `black .` on the project.

Black has very few configurations you need to worry about. However, if you need
to change its settings, see the `[tool.black]` section in `pyproject.toml`.

### Flake8

Flake8 is our static analysis tool. It checks for common mistakes and some additional style errors in
the Python code. It also uses mccabe to check the complexity, flagging sections of code that are
too complicated.

While Flake8 is run automatically as part of Tox, you can manually invoke like this:

```bash
flake8 .
```

If you need to suppress a warning on a particular line, you can use the inline
comment `# noqa: E123`, where `E123` is the error code you want to suppress.
Flake8 error and warning messages will provide these.

If you need to modify Flake8's configuration, see the `[flake8]` section of
`setup.cfg`.

### isort

isort sorts the import statements in a manner that makes it easier to read through them. To arrange your
import statements, run the following command:

```bash
isort .
```

When run automatically as part of Tox or the CI, isort will merely fail if the formatting is
incorrect. It will not actually make changes. This is because the `--check` flag is being passed in
that situation. If it fails, run `isort .` on the project.

If you need to modify the configuration for isort, see the `[tool.isort]` section
of `pyproject.toml`.

### Bandit

Bandit monitors our code for possible security issues. It is run as part of Tox, but you can manually
invoke it like this:

```bash
bandit -c pyproject.toml -r src
```

If you need to suppress a warning on a particular line, you can use the inline
comment `# nosec: E123`, where `E123` is the error code you want to suppress.
Flake8 error and warning messages will provide these.

If you need to modify Bandit's configuration, see the `[tool.bandit]` section
of `pyproject.toml`.
