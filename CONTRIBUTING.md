# Contributing to Autopsy AI

First off, thank you for considering contributing to Autopsy AI!

## Coding Standards

### General Principles
- **Clean Code:** Write readable, self-documenting code.
- **DRY (Don't Repeat Yourself):** Abstract common logic into reusable components/functions.
- **Privacy First:** Never log sensitive user data. Always use secure methods for data handling.

### Python (Backend)
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines.
- Use type hints for all function signatures.
- Use `pytest` for unit and integration tests.
- Recommended IDE: VS Code with Pylance.

### JavaScript/React (Frontend)
- Use functional components and Hooks.
- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript).
- Use Prettier for code formatting.
- Components should be modular and reusable.

## Branching Strategy

We use a simplified version of [Gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow):

- **main:** Production-ready code.
- **develop:** Integration branch for features.
- **feature/feature-name:** New features or improvements.
- **bugfix/issue-name:** Bug fixes.
- **hotfix/issue-name:** Critical fixes for production.

### Workflow
1. Branch off `develop`.
2. Commit changes with clear, descriptive messages.
3. Open a Pull Request (PR) to `develop`.
4. PR must pass CI tests and receive at least one approval.
5. Merge PR into `develop`.

## GitHub Issue Breakdown

We use labels to categorize issues:
- `enhancement`: New features.
- `bug`: Something isn't working.
- `privacy`: Related to data privacy and security.
- `documentation`: Improvements to docs.
- `good first issue`: Beginner-friendly tasks.
