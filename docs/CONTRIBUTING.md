# Contributing to Aquarius

Thank you for your interest in contributing to Aquarius! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, background, or identity.

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers and help them get started
- Provide constructive feedback
- Focus on what is best for the project
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Personal attacks or trolling
- Publishing others' private information
- Any other conduct inappropriate in a professional setting

## Getting Started

### Prerequisites

Before contributing, ensure you have:
- The required programming language runtime/compiler installed
- The project's build tools installed
- Git configured on your machine
- A GitHub account

> **Note:** Specific version requirements will be documented once the technology stack is finalized.

### Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/aquarius.git
   cd aquarius
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/gernotstarke/aquarius.git
   ```
4. Create a branch for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### 1. Sync with Upstream

Before starting work, sync your fork with the upstream repository:

```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

### 2. Create a Feature Branch

Create a branch with a descriptive name:

```bash
git checkout -b feature/add-user-authentication
# or
git checkout -b fix/resolve-database-connection-issue
```

### 3. Make Your Changes

- Make small, focused changes
- Follow the coding standards (see below)
- Write or update tests as needed
- Update documentation if required

### 4. Test Your Changes

Run the test suite to ensure everything works:

```bash
# Command will depend on chosen technology stack
# Examples:
# npm test
# pytest
# go test ./...
# cargo test
```

### 5. Commit Your Changes

Follow our commit message guidelines (see below):

```bash
git add .
git commit -m "feat: add user authentication endpoint"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Coding Standards

### General Principles

- **KISS (Keep It Simple, Stupid):** Favor simple solutions over complex ones
- **DRY (Don't Repeat Yourself):** Avoid code duplication
- **YAGNI (You Aren't Gonna Need It):** Don't add functionality until needed
- **SOLID Principles:** Follow good design principles

### Code Style

Specific code style guidelines will be established once the technology stack is selected. General principles:

- Use consistent indentation (typically 2 or 4 spaces, no tabs)
- Maximum line length: **120 characters**
- Use **meaningful variable and function names**
- Keep functions/methods focused and small
- Comment complex logic, but prefer self-documenting code

### API Development Best Practices

- Keep API handlers/controllers thin - business logic belongs in services
- Use proper HTTP status codes
- Follow RESTful conventions
- Validate input at API boundaries
- Externalize configuration
- Handle errors consistently

### Project Structure

Structure will be defined based on chosen technology stack and framework conventions. Typical layers include:

```
src/
├── api/             # API handlers/controllers
├── services/        # Business logic
├── data/            # Data access layer
├── models/          # Domain entities/models
├── dto/             # Data transfer objects
├── middleware/      # Middleware/interceptors
└── config/          # Configuration
```

## Testing Guidelines

### Test Coverage

- Aim for **> 80%** code coverage
- All new features must include tests
- Bug fixes should include regression tests

### Types of Tests

1. **Unit Tests**
   - Test individual functions and modules
   - Use mocking for dependencies
   - Fast and isolated

2. **Integration Tests**
   - Test interactions between components
   - May use test containers or in-memory databases
   - Test actual integrations

3. **API Tests**
   - Test REST endpoints end-to-end
   - Validate request/response formats
   - Test error handling

### Test Naming Convention

Use descriptive test names that indicate:
- What is being tested
- The condition or scenario
- The expected behavior

Examples:
- `test_find_by_id_when_user_exists_returns_user`
- `should_return_404_when_resource_not_found`
- `findById_withValidId_returnsUser`

### Test Structure

Follow the Arrange-Act-Assert (AAA) pattern:

```
// Arrange: Set up test data and conditions
// Act: Execute the code being tested
// Assert: Verify the expected outcome
```

Specific testing frameworks and examples will be provided once the technology stack is selected.

## Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **style:** Code style changes (formatting, no code change)
- **refactor:** Code refactoring
- **test:** Adding or updating tests
- **chore:** Maintenance tasks

### Examples

```
feat(auth): add JWT authentication

Implement JWT-based authentication for API endpoints.
- Add JWT token generation
- Add token validation filter
- Update security configuration

Closes #123
```

```
fix(database): resolve connection pool exhaustion

Increase connection pool size and add proper connection release
in error scenarios.

Fixes #456
```

```
docs(api): update endpoint documentation

Add examples for all user management endpoints.
```

### Guidelines

- Use imperative mood ("add" not "added" or "adds")
- Don't capitalize first letter
- No period at the end of subject line
- Limit subject line to 50 characters
- Wrap body at 72 characters
- Separate subject from body with blank line
- Use body to explain what and why, not how

## Pull Request Process

### Before Submitting

1. ✅ Ensure all tests pass
2. ✅ Update documentation if needed
3. ✅ Add tests for new functionality
4. ✅ Follow coding standards
5. ✅ Rebase on latest main branch
6. ✅ Ensure commit messages follow guidelines

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Closes #(issue number)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
Describe testing performed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code follows style guidelines
- [ ] All tests pass
```

### Review Process

1. **Automated Checks:** CI pipeline must pass
2. **Code Review:** At least one approval required
3. **Testing:** Reviewer should test changes locally if significant
4. **Feedback:** Address review comments promptly
5. **Merge:** Once approved, maintainer will merge

### After Merge

1. Delete your feature branch
2. Sync your fork with upstream
3. Celebrate! 🎉

## Questions?

If you have questions or need help:
- Open an issue with the "question" label
- Reach out to maintainers
- Check existing documentation

Thank you for contributing to Aquarius! 🙏
