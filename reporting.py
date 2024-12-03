import json

def consolidate_reports(pip_audit_report, grype_report, trivy_report):
    combined = {
        "pip_audit": json.loads(pip_audit_report),
        "grype": json.loads(grype_report),
        "trivy": json.loads(trivy_report),
    }
    with open("report.json", "w") as f:
        json.dump(combined, f, indent=4)
    return combined

