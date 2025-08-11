# Security Policy

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

The Local Ollama RAG team takes security seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

1. **DO NOT** open a public GitHub issue for security vulnerabilities
2. Send an email to: [security@example.com] (replace with actual email)
3. Include as much detail as possible about the vulnerability

### What to Include

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment
- Any suggested fixes (if available)
- Your contact information for follow-up

### Response Timeline

- **Initial Response:** Within 48 hours of report
- **Assessment:** Within 7 days
- **Fix Timeline:** Varies by severity, but critical issues will be prioritized
- **Disclosure:** After fix is released and users have time to update

## Security Considerations

### Local-First Architecture

This project is designed for local operation, which provides inherent security benefits:

- **No External APIs:** All processing happens locally
- **Data Privacy:** Your documents never leave your machine
- **Network Isolation:** Works completely offline

### Potential Risk Areas

While the local-first design is security-focused, be aware of:

1. **Document Processing:** Malicious documents could potentially exploit parsing libraries
2. **Model Security:** Ensure your Ollama models are from trusted sources
3. **File System Access:** The tool requires read access to your documents and write access for indices
4. **Dependencies:** We regularly audit dependencies for known vulnerabilities

### Best Practices for Users

1. **Keep Updated:** Regularly update to the latest version
2. **Trusted Sources:** Only process documents from trusted sources
3. **Model Verification:** Use verified Ollama models
4. **Environment Isolation:** Consider running in containerized environments for sensitive use cases
5. **Backup Strategy:** Regularly backup your document indices

### Security Features

- **Dependency Scanning:** Automated vulnerability checks via GitHub Actions
- **Code Analysis:** Static analysis with CodeQL, Bandit, and Semgrep
- **Minimal Dependencies:** Reduced attack surface through minimal dependency tree
- **Local Operation:** No external network calls eliminate remote attack vectors

## Security Updates

Security updates are distributed through:

1. **GitHub Releases:** Tagged releases with security fixes
2. **PyPI:** Updated packages with security patches
3. **Security Advisories:** GitHub security advisories for critical issues

## Vulnerability Disclosure Policy

### Coordinated Disclosure

We follow responsible disclosure practices:

1. **Assessment Period:** Up to 90 days for initial assessment
2. **Fix Development:** Reasonable time for fix development
3. **User Notification:** Security advisory published with fix
4. **Credit:** Security researchers credited (unless anonymous requested)

### Severity Classification

- **Critical:** Remote code execution, data corruption
- **High:** Local privilege escalation, sensitive data exposure
- **Medium:** Information disclosure, denial of service
- **Low:** Minor security improvements

## Security Contact

For security-related questions or reports:
- Email: [security@example.com] (replace with actual email)
- GPG Key: [Link to public key if available]

## Acknowledgments

We thank the security research community for responsible disclosure and helping keep Local Ollama RAG secure.

---

*Last Updated: 2025-08-08*