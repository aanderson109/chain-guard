# chain guard
`chain-guard` is intended to be an easy-to-use assembly of other security tools to enhance the visibility product and application security engineers have into their software.

## Core Features
- **Vulnerability Scanning:** Implements tools like `pip-audit`, `Grype`, `Trivy` to scan dependencies or libraries for known vulnerabilities.

- **Signature Verification:** Uses `sigstore` to verify the integrity and provenance of the library or container images.

- **SBOM Generation & Analysis:** Generates an SBOM (using `Syft`) and analyzes it with `Trivy` or `Grype`.

- **Open-Source Activity Analysis** Uses `PyGithub`, `pypi-simple`, and `gitpython` to pull metrics related to open source repositories.

- **Audit Trail** Saves digests, scan results, and approvals in a database or a file for traceability. 

## Architecture
**Inputs**
- Library/package name or file path (e.g., `requests` for Python or `package.tar.gz`)
- Container image (optional, e.g., `docker.io/library/nginx:latest`)
- Dependency files (e.g., `requirements.txt`, `package.json`, `pom.xml`)

**Workflow**
1. Accept library or dependency file as input
2. Run scans and verifications using the tools
3. Reports results back

**Outputs**
- Scan results
    - Vulnerabilities grouped by severity
    - License issues
    - Signature verification results

- Formats
    - CLI output
    - JSON/HTML report
    - Exportable SBOMs

## Packaging and Distribution
`argparse` is used to provide a basic CLI and the entire tool is packaged into a dockerfile to try and alleviate dependency issues.

## Integration with Vulnerability Management & Product Security
`chain-guard` should provide engineers a more streamlined method for analyzing the potential vulnerabilities in projects from third-party sources.

**Workflow**
1. Input
    - Security engineer provides the package (file or name) to the tool.
    - Example: `requests`, `package.json`.
2. Automated Analysis
    - Run scans, SBOM analysis, license checks, and signature verification.
    - Generate a hash for the package and store it with the results.
3. Updated Risk Metrics
    - Present a **risk score** or **summary report** for the security team to review.
4. Audit Trail
    - Save hashes, scan results, and approvals in a database or a file for traceability.

**Command Line Interface:** Eventually, the goal is for a simplified CLI interface like is shown below.
```bash
chain-guard --scan [target] --save-hash
```
**Example CLI Output:** An easily readable output on the CLI would be preferred in the future.
```text
Scanning: [module]
-----------------------------------------
SHA-256 Hash: a6f32b1c57a8...
Signature: Verified (via sigstore)
Vulnerabilities:
  - CVE-2023-12345 (HIGH)
  - CVE-2023-54321 (LOW)
License: MIT
Approval Status: PENDING REVIEW
Report saved to: reports/[module].json
```
**Example JSON Report**
```json
{
  "package_name": "[module]",
  "file_name": "[module]",
  "hash": "a6f32b1c57a8...",
  "signature_verified": true,
  "vulnerabilities": [
    {"id": "CVE-2023-12345", "severity": "HIGH", "description": "Path traversal vulnerability."},
    {"id": "CVE-2023-54321", "severity": "LOW", "description": "Minor DoS issue."}
  ],
  "licenses": ["MIT"],
  "sbom": "reports/[module]-sbom.json",
  "approval_status": "PENDING REVIEW",
  "scan_date": "2024-12-02T12:00:00Z"
}
```



