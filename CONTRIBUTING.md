# Contributing to RemotelyX Dashboard

Thank you for considering contributing to RemotelyX Dashboard! This document provides guidelines and information for contributors.

## 🚀 Quick Start for Contributors

### 1. Fork & Clone
```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/remotelyx-dashboard.git
cd remotelyx-dashboard
```

### 2. Set Up Development Environment

#### Option A: Using Docker (Recommended)
```bash
# Make the quick start script executable and run it
chmod +x quick-start.sh
./quick-start.sh
```

#### Option B: Manual Setup
```bash
# Backend setup
cd server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
./run_dev.sh

# Frontend setup (in a new terminal)
cd client
npm install
npm run dev
```

### 3. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

## 🎯 How to Contribute

### Reporting Issues
1. Check existing issues first
2. Use our issue templates
3. Provide clear reproduction steps
4. Include system information

### Submitting Changes
1. **Small changes**: Direct pull requests are welcome
2. **Large changes**: Open an issue first to discuss
3. **New features**: Create a feature request issue

### Pull Request Process
1. Ensure your code follows our style guidelines
2. Add tests for new functionality
3. Update documentation as needed
4. Ensure all tests pass
5. Request review from maintainers

## 🏗️ Development Guidelines

### Code Style

#### Python (Backend)
- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters (Black formatter)
- Use meaningful variable names

```python
# Good
async def get_user_jobs(user_id: str) -> List[Job]:
    """Retrieve all jobs for a specific user."""
    return await Job.find(Job.user_id == user_id).to_list()

# Avoid
def get_jobs(id):
    return Job.find(Job.user_id == id).to_list()
```

#### JavaScript/TypeScript (Frontend)
- Use TypeScript when possible
- Follow ESLint configuration
- Use meaningful component names
- Prefer functional components with hooks

### Database Guidelines
- Use proper indexes for queries
- Follow MongoDB best practices
- Include migration scripts for schema changes
- Test database operations

### API Guidelines
- Follow RESTful conventions
- Include proper HTTP status codes
- Validate input data with Pydantic
- Document endpoints with docstrings

```python
@router.post("/jobs", response_model=JobResponse, status_code=201)
async def create_job(job_data: JobCreate, current_user: User = Depends(get_current_user)):
    """Create a new job application entry."""
    # Implementation here
```

## 🧪 Testing

### Running Tests
```bash
# Backend tests
cd server
python -m pytest

# Frontend tests
cd client
npm run test

# API integration tests
./test_api.sh
```

### Test Guidelines
- Write tests for new features
- Maintain test coverage above 80%
- Use descriptive test names
- Test both success and error cases

### Example Test
```python
async def test_create_job_success():
    """Test successful job creation."""
    job_data = {
        "title": "Software Engineer",
        "company": "Tech Corp",
        "status": "applied"
    }
    response = await client.post("/api/v1/jobs", json=job_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Software Engineer"
```

## 📝 Documentation

### Code Documentation
- Document all public functions and classes
- Use clear, concise docstrings
- Include examples for complex functionality

### API Documentation
- Update OpenAPI/Swagger docs
- Include request/response examples
- Document error responses

### README Updates
- Update setup instructions if needed
- Add new features to feature list
- Update environment variables section

## 🔧 Project Structure

```
remotelyx-dashboard/
├── server/                 # FastAPI backend
│   ├── app/
│   │   ├── controllers/    # API route handlers
│   │   ├── models/        # Database models (Beanie)
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── utils/         # Helper functions
│   ├── tests/            # Backend tests
│   └── migrations/       # Database migrations
├── client/               # Frontend application
├── docker-compose.yml    # Development environment
└── docs/                # Additional documentation
```

## 🏷️ Commit Messages

Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(auth): add JWT token refresh endpoint
fix(jobs): resolve duplicate job creation issue
docs(api): update authentication documentation
```

## 🚨 Issues and Bugs

### Before Reporting
1. Search existing issues
2. Check if it's already fixed in latest version
3. Reproduce with minimal example

### Issue Template
```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11.0]
- Node.js: [e.g., 18.17.0]
- Browser: [if frontend issue]

## Additional Context
Any other relevant information
```

## 🌟 Feature Requests

We welcome feature requests! Please:
1. Search existing feature requests
2. Describe the problem it solves
3. Provide implementation suggestions
4. Consider the scope and complexity

## 📞 Getting Help

- **Documentation**: Check README.md first
- **Issues**: Search existing issues
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers for security issues

## 🎉 Recognition

Contributors will be:
- Listed in our CONTRIBUTORS.md file
- Mentioned in release notes for significant contributions
- Invited to maintainer team for consistent contributors

## 📋 Checklist for Contributors

Before submitting a PR:
- [ ] Code follows style guidelines
- [ ] Tests are added and passing
- [ ] Documentation is updated
- [ ] Commit messages follow convention
- [ ] No merge conflicts
- [ ] PR description is clear

## 🤝 Code of Conduct

Please be respectful and inclusive. We want this project to be welcoming for everyone.

---

Thank you for contributing to RemotelyX Dashboard! 🚀
