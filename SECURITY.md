# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability in STForensicMacOS, please follow these steps:

### 1. **DO NOT** create a public GitHub issue
Security vulnerabilities should be reported privately to prevent potential exploitation.

### 2. **Email the maintainers**
Send a detailed email to the project maintainers with:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. **Response timeline**
- Initial response: Within 48 hours
- Status update: Within 7 days
- Resolution: As soon as possible

### 4. **Disclosure policy**
- Vulnerabilities will be disclosed after a fix is available
- Credit will be given to reporters (unless requested otherwise)
- CVE numbers will be requested for significant issues

## Security Features

### Built-in Security Measures

1. **Root Privilege Verification**
   - Checks for root/administrator privileges
   - Prevents unauthorized access

2. **Read-Only Operations**
   - All forensic operations are read-only
   - Original data is never modified

3. **Hash Verification**
   - SHA256 hashes for all generated reports
   - Ensures report integrity

4. **Data Integrity**
   - No data modification during analysis
   - Preserves original timestamps

5. **Error Handling**
   - Graceful error handling
   - No sensitive data exposure in error messages

### Security Best Practices

1. **Use in Controlled Environment**
   - Run in isolated environment
   - Use dedicated forensic workstations

2. **Network Security**
   - Disconnect from network during analysis
   - Use air-gapped systems when possible

3. **Access Control**
   - Limit access to forensic tools
   - Use strong authentication

4. **Data Protection**
   - Encrypt sensitive data
   - Secure storage of reports

## Security Considerations

### System Requirements
- Requires root privileges (by design)
- Should be run on dedicated forensic systems
- Network access should be controlled

### Data Handling
- All operations are read-only
- No data is transmitted externally
- Reports contain only analysis results

### Privacy
- Respects user privacy
- No personal data collection
- Configurable logging levels

## Security Updates

### Update Process
1. Security patches are released as hotfixes
2. Version numbers are incremented appropriately
3. Security advisories are published
4. Users are notified through GitHub releases

### Update Recommendations
- Keep the tool updated to latest version
- Monitor security advisories
- Apply patches promptly

## Contact Information

For security-related issues:
- **Email**: [Maintainer email]
- **GitHub**: [GitHub Issues (private)]
- **Response Time**: 24-48 hours

## Security Acknowledgments

We thank security researchers and contributors who help improve the security of STForensicMacOS through responsible disclosure.

---

**Note**: This tool is designed for educational and legal forensic analysis purposes only. Users are responsible for complying with local laws and regulations. 