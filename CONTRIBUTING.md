# Contributing to AI Research Analyzer

Thank you for your interest in contributing to **AI Research Analyzer**!
This project welcomes contributions from developers, researchers, and
enthusiasts who are interested in building scalable, AI-driven research
analysis tools.

This document outlines the guidelines and process for contributing
effectively to the project.

---

## Contribution Opportunities

Contributions are welcome in the following areas:
- **Code Enhancements**: Bug fixes, refactoring, performance improvements, and new features.
- **Documentation**: Improving README files, inline comments, or usage guides.
- **Testing**: Writing or improving test cases (planned for future versions).
- **Issues**: Reporting bugs or proposing feature ideas.
- **Community Support**: Helping other users through GitHub issues and discussions.

---

## Getting Started

### Prerequisites
- Python 3.8 or later
- Django 5.1.7
- Git and GitHub account
- Local project setup (see [README.md](README.md))

---

## Contribution Workflow

1. **Fork the Repository**
   - Fork the repository to your own GitHub account.
   - Clone your fork locally:
     ```bash
     git clone https://github.com/<your-username>/AI-Research-Analyzer.git
     cd AI-Research-Analyzer
     ```

2. **Set Up the Development Environment**
   - Follow the installation steps in the [README.md](README.md).
   - Verify the application runs locally:
     ```bash
     python manage.py runserver
     ```

3. **Create a Feature Branch**
   - Create a branch with a meaningful name:
     ```bash
     git checkout -b feat/short-description
     ```
   - Naming conventions:
     - `feat/` → new features
     - `fix/` → bug fixes
     - `docs/` → documentation updates

4. **Make Your Changes**
   - Follow **PEP 8** coding standards.
   - Write clean, readable, and well-documented code.
   - Ensure compatibility with the supported Python and Django versions.
   - Test changes locally before committing.

5. **Commit Your Changes**
   - Use clear and concise commit messages:
     ```bash
     git commit -m "Improve research summary generation logic"
     ```

6. **Push to Your Fork**
   ```bash
   git push origin feat/short-description
