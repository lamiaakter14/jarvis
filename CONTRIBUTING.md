# Contributing to JARVIS

Thank you for your interest in contributing to JARVIS! This document provides guidelines and instructions for contributing.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**: `git clone https://github.com/lamiaakter14/jarvis.git`
3. **Create a branch**: `git checkout -b feature/your-feature-name`
4. **Make your changes**
5. **Test your changes**: `make test`
6. **Commit your changes**: `git commit -m "Description of changes"`
7. **Push to your fork**: `git push origin feature/your-feature-name`
8. **Create a Pull Request**

## Development Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker and Docker Compose
- PostgreSQL 15+
- Redis 7+

### Installation

```bash
# Install dependencies
make install-dev

# Start development environment
make dev

# Run tests
make test
```

## Code Style

We use automated tools to maintain code quality:

- **Python**: Black, Ruff, isort, MyPy
- **JavaScript/TypeScript**: ESLint, Prettier
- **Pre-commit hooks**: Automatically run on commit

Format your code:
```bash
make format
```

Check code quality:
```bash
make lint
make type-check
```

## Testing

- Write tests for all new features
- Maintain or improve test coverage
- Run tests before submitting PR

```bash
# Run all tests
make test

# Run with coverage
make test-coverage
```

## Commit Messages

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Build/tooling changes

Example: `feat: add WebSocket support for cognitive loop`

## Pull Request Process

1. Update documentation for any changed functionality
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers
6. Address review feedback
7. Wait for approval and merge

## Project Structure

```
jarvis/
├── apps/          # Applications (API, CLI, Web)
├── packages/      # Shared packages
├── infrastructure/# Infrastructure as Code
├── docs/          # Documentation
├── tests/         # Test suites
└── scripts/       # Utility scripts
```

## Areas for Contribution

- **Core Agents**: Improve agent intelligence
- **API**: Add new endpoints or features
- **UI/UX**: Enhance dashboard and visualizations
- **Documentation**: Improve guides and examples
- **Testing**: Increase test coverage
- **Performance**: Optimize bottlenecks
- **Infrastructure**: Improve deployment

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Join our community channels

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
