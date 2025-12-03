# Contributing

<cite>
**Referenced Files in This Document**   
- [CONTRIBUTING.md](file://CONTRIBUTING.md)
- [pyproject.toml](file://pyproject.toml)
- [Makefile](file://Makefile)
- [embedchain/pyproject.toml](file://embedchain/pyproject.toml)
- [embedchain/Makefile](file://embedchain/Makefile)
- [embedchain/CONTRIBUTING.md](file://embedchain/CONTRIBUTING.md)
- [embedchain/tests/conftest.py](file://embedchain/tests/conftest.py)
- [embedchain/tests/test_app.py](file://embedchain/tests/test_app.py)
- [embedchain/tests/embedchain/test_embedchain.py](file://embedchain/tests/embedchain/test_embedchain.py)
</cite>

## Table of Contents
1. [Development Setup](#development-setup)
2. [Code Style and Linting](#code-style-and-linting)
3. [Testing Guidelines](#testing-guidelines)
4. [Pull Request Process](#pull-request-process)
5. [Contribution Areas](#contribution-areas)
6. [Documentation Standards](#documentation-standards)
7. [Release Process](#release-process)
8. [First-Time Contributor Guidance](#first-time-contributor-guidance)

## Development Setup

To set up the development environment for contributing to mem0, follow these steps:

1. Fork and clone the repository
2. Install Hatch, the tool used for managing development environments:
   ```bash
   pip install hatch
   ```
3. Set up the development environment using Hatch:
   ```bash
   # Activate environment for specific Python version:
   hatch shell dev_py_3_9   # Python 3.9
   hatch shell dev_py_3_10  # Python 3.10  
   hatch shell dev_py_3_11  # Python 3.11
   hatch shell dev_py_3_12  # Python 3.12
   ```

The environment will automatically install all development dependencies. For the embedchain component, Poetry is used instead of Hatch:
```bash
cd embedchain
poetry install
```

Install pre-commit hooks to ensure code quality standards:
```bash
pre-commit install
```

**Section sources**
- [CONTRIBUTING.md](file://CONTRIBUTING.md#L19-L41)
- [pyproject.toml](file://pyproject.toml#L109-L147)
- [embedchain/pyproject.toml](file://embedchain/pyproject.toml#L146-L158)

## Code Style and Linting

The project follows specific code style guidelines enforced through automated tools. The code style is configured in the pyproject.toml files for both the main mem0 package and the embedchain subpackage.

For the main mem0 package, the project uses:
- Ruff for code formatting and linting
- Isort for import sorting
- Line length limit of 120 characters

The configuration can be found in the pyproject.toml file. To run the linters:
```bash
# Format code
make format

# Sort imports
make sort

# Run linting
make lint
```

For the embedchain package, additional tools are used:
- Black for code formatting
- Ruff for linting
- Isort for import sorting
- Line length limit of 120 characters

The Makefile provides convenient commands for running these tools across both packages.

**Section sources**
- [pyproject.toml](file://pyproject.toml#L166-L168)
- [embedchain/pyproject.toml](file://embedchain/pyproject.toml#L24-L68)
- [Makefile](file://Makefile#L18-L28)
- [embedchain/Makefile](file://embedchain/Makefile#L35-L37)

## Testing Guidelines

The project uses pytest for testing across multiple Python versions. Testing coverage is expected to be comprehensive, especially for new features and bug fixes.

To run tests for the main mem0 package:
```bash
# Run tests with default Python version
make test

# Test specific Python versions:
make test-py-3.9   # Python 3.9 environment
make test-py-3.10  # Python 3.10 environment
make test-py-3.11  # Python 3.11 environment
make test-py-3.12  # Python 3.12 environment
```

For the embedchain package, tests can be run using:
```bash
# Run all tests
make test

# Run specific test file
make test file=tests/test_factory.py

# Run with coverage
make coverage
```

Test files are organized in the tests directory, with subdirectories corresponding to the package structure. The conftest.py file contains shared fixtures used across multiple test files, including database cleanup and telemetry disabling.

All tests must pass across all supported Python versions before submitting a pull request. When adding new code, appropriate tests should be included to cover the functionality.

**Section sources**
- [CONTRIBUTING.md](file://CONTRIBUTING.md#L43-L61)
- [Makefile](file://Makefile#L42-L55)
- [embedchain/Makefile](file://embedchain/Makefile#L51-L56)
- [embedchain/tests/conftest.py](file://embedchain/tests/conftest.py#L8-L35)
- [embedchain/tests/test_app.py](file://embedchain/tests/test_app.py#L1-L112)
- [embedchain/tests/embedchain/test_embedchain.py](file://embedchain/tests/embedchain/test_embedchain.py#L1-L76)

## Pull Request Process

To contribute to the project, follow this pull request process:

1. Fork the repository and create a dedicated feature branch (e.g., `feature/f1`)
2. Make your changes and ensure they follow the code style guidelines
3. If you modified the code (new feature or bug-fix), add appropriate tests
4. Include proper documentation, docstrings, and examples to demonstrate the feature
5. Ensure that all tests pass across all supported Python versions
6. Submit a pull request through GitHub

The pull request should include:
- A clear description of the changes
- Reference to any related issues
- Explanation of the motivation for the change
- Any testing that was performed

The automated CI/CD pipeline will run the tests and linting checks on the pull request. All checks must pass before the pull request can be merged.

**Section sources**
- [CONTRIBUTING.md](file://CONTRIBUTING.md#L5-L16)

## Contribution Areas

The project welcomes contributions in the following areas:

1. **New Features**: Implementing new functionality that enhances the memory layer capabilities
2. **Bug Fixes**: Resolving reported issues and improving code reliability
3. **Documentation**: Improving documentation, adding examples, and clarifying usage
4. **Testing**: Adding new tests, improving test coverage, and fixing test issues
5. **Performance Optimization**: Identifying and resolving performance bottlenecks
6. **Integration Support**: Adding support for new vector databases, LLM providers, or other services

First-time contributors are encouraged to look for issues labeled as "good first issue" or "help wanted" in the GitHub repository.

**Section sources**
- [CONTRIBUTING.md](file://CONTRIBUTING.md#L3-L16)

## Documentation Standards

Documentation should be clear, comprehensive, and follow the project's style guidelines. When contributing documentation:

1. Use clear and concise language
2. Include relevant examples and code snippets
3. Follow the existing documentation structure
4. Ensure documentation is up-to-date with the code
5. Use consistent terminology throughout

For code documentation, include:
- Docstrings for all public functions, classes, and methods
- Type hints where appropriate
- Clear parameter and return value descriptions
- Examples of usage when applicable

The project documentation is organized in the docs directory, with separate sections for different aspects of the system.

**Section sources**
- [CONTRIBUTING.md](file://CONTRIBUTING.md#L12-L13)

## Release Process

The release process for the project involves the following steps:

1. Ensure all tests pass across all supported Python versions
2. Update the version number in pyproject.toml
3. Create a new git tag with the version number
4. Build the package using Hatch:
   ```bash
   hatch build
   ```
5. Publish the package to PyPI:
   ```bash
   hatch publish
   ```

For the embedchain package, Poetry is used for building and publishing:
```bash
# Build package
poetry build

# Publish package
poetry publish
```

The Makefile provides convenient commands for building and publishing the packages.

**Section sources**
- [Makefile](file://Makefile#L33-L37)
- [embedchain/Makefile](file://embedchain/Makefile#L45-L49)
- [pyproject.toml](file://pyproject.toml#L5-L7)

## First-Time Contributor Guidance

Welcome! We're excited to have you contribute to mem0. Here's how to get started:

1. **Set up your development environment** following the instructions in the Development Setup section
2. **Look for beginner-friendly issues** labeled as "good first issue" in the GitHub repository
3. **Join our community** on Discord to ask questions and get help from other contributors
4. **Follow the pull request process** outlined in this document
5. **Don't hesitate to ask questions** - we're here to help you succeed

Remember to:
- Start with small, focused contributions
- Write clear commit messages
- Include tests for your changes
- Follow the code style guidelines
- Be patient and persistent

We appreciate your interest in improving mem0 and look forward to your contributions!

**Section sources**
- [CONTRIBUTING.md](file://CONTRIBUTING.md#L3-L64)
- [README.md](file://README.md#L1-L169)