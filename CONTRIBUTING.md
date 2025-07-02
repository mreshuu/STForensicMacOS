# Contributing to STForensicMacOS

Thank you for your interest in contributing to STForensicMacOS! This document explains how you can contribute to the project.

## 🚀 Getting Started

### Development Environment Setup

1. **Fork and clone the repository:**
```bash
git clone https://github.com/silexi/stforensicmacos.git
cd stforensicmacos
```

2. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Install development dependencies:**
```bash
pip install -r requirements-dev.txt  # If available
```

## 📝 Types of Contributions

### 🐛 Bug Reports
- Use GitHub Issues
- Use descriptive titles
- Include step-by-step reproduction instructions
- Explain expected vs actual behavior
- Include system information (macOS version, Python version)

### 💡 Feature Requests
- Explain the purpose of the feature
- Specify use cases
- Suggest implementation if possible

### 🔧 Code Contributions
- Use fork and pull request workflow
- Create feature branches
- Follow coding standards
- Add tests when possible

## 🏗️ Coding Standards

### Python Code Style
- Follow PEP 8 standards
- Use 4-space indentation
- 79 character line length
- Add docstrings
- Use type hints

### Commit Messages
- Be descriptive and concise
- Use English
- Follow conventional commits format:
  - `feat:` New feature
  - `fix:` Bug fix
  - `docs:` Documentation
  - `style:` Code style
  - `refactor:` Refactoring
  - `test:` Test addition/update
  - `chore:` Maintenance tasks

### Example Commit Messages
```
feat: Add memory dump functionality
fix: Resolve IPv6 address parsing issue
docs: Update README with installation instructions
style: Format code according to PEP 8
```

## 🧪 Testing

### Manual Testing
```bash
# Lite mode test
sudo python3 main.py --mode lite --output ./test_reports

# Specific module test
sudo python3 main.py --modules network --output ./test_reports

# HTML report test
sudo python3 main.py --mode lite --output ./test_reports --format html
```

### Automated Testing (Future)
```bash
# Unit tests
python -m pytest tests/

# Coverage report
python -m pytest --cov=src tests/
```

## 📋 Pull Request Process

1. **Create an issue** (if none exists)
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test your changes**
5. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: Add your feature description"
   ```
6. **Push your changes:**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

### Pull Request Checklist
- [ ] Code follows standards
- [ ] Tested
- [ ] Documentation updated
- [ ] Commit messages descriptive
- [ ] Issue reference added

## 🔒 Security

### Security Vulnerabilities
- Report security vulnerabilities directly to maintainers
- Don't create public issues
- Provide detailed information

### Security Principles
- Perform read-only operations only
- Protect user data
- Check root privileges
- Use hash verification

## 📚 Documentation

### Code Documentation
- Add docstrings for all functions
- Explain complex algorithms
- Include usage examples

### README Updates
- Add documentation for new features
- Update examples
- Add screenshots if needed

## 🎯 Contribution Areas

### Priority Areas
- [ ] PDF reporting
- [ ] CSV export
- [ ] GUI interface
- [ ] Docker support
- [ ] Increase test coverage
- [ ] Performance optimization

### Module Development
- Add new forensic modules
- Improve existing modules
- Enhance error handling

### Reporting
- Add new report formats
- Improve HTML reports
- Add graphs and visualizations

## 🤝 Communication

- **GitHub Issues:** [Issues](https://github.com/silexi/stforensicmacos/issues)
- **Discussions:** [Discussions](https://github.com/silexi/stforensicmacos/discussions)

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉 