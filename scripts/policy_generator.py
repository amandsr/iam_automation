import json
from pathlib import Path

def sanitize_resource(resource):
    if isinstance(resource, str):
        resource = resource.strip()
        # Remove extra surrounding quotes if present
        if resource.startswith('"') and resource.endswith('"'):
            resource = resource[1:-1]
    return resource

def build_policy(data):
    policy = {
        "Version": "2012-10-17",
        "Statement": []
    }

    for stmt in data.get("statements", []):
        statement = {
            "Effect": stmt.get("effect", "Allow"),
            "Action": stmt.get("actions", []),
            "Resource": stmt.get("resources", [])
        }

        # Sanitize Actions
        if isinstance(statement["Action"], list) and len(statement["Action"]) == 1:
            statement["Action"] = statement["Action"][0]

        # Sanitize Resources
        if isinstance(statement["Resource"], list):
            if len(statement["Resource"]) == 1:
                statement["Resource"] = sanitize_resource(statement["Resource"][0])
            else:
                statement["Resource"] = [sanitize_resource(r) for r in statement["Resource"]]

        if "condition" in stmt:
            statement["Condition"] = stmt["condition"]

        policy["Statement"].append(statement)

    return policy

def build_assume_role_policy(data):
    # Case 1: Full assume role policy object is provided
    if isinstance(data.get("assume_role_policy"), dict):
        return data["assume_role_policy"]

    # Case 2: Generate assume role policy from service name (if valid)
    assume_role_service = data.get("assume_role_policy")
    if assume_role_service and isinstance(assume_role_service, str) and assume_role_service.strip().lower() != "null":
        return {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": assume_role_service.strip()
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }

def main():
    input_path = Path("iam_policy_orchestration_full/inputs/user_input.json")
    output_dir = Path("iam_policy_orchestration_full/terraform/environments/")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return

    with input_path.open() as f:
        data = json.load(f)

    policy = build_policy(data)
    assume_role_policy = build_assume_role_policy(data)

    policy_path = output_dir / "generated_policy.json"
    with policy_path.open("w") as f:
        json.dump(policy, f, indent=2)

    assume_role_policy = build_assume_role_policy(data)
    if assume_role_policy:
        assume_role_policy_path = output_dir / "assume_role_policy.json"
        with assume_role_policy_path.open("w") as f:
            json.dump(assume_role_policy, f, indent=2)
        print(f"✅ Assume role policy generated at: {assume_role_policy_path}")
    else:
        print("ℹ️ No assume role policy generated (assume_role_policy was null or missing)")

    print(f"✅ IAM policy generated at: {policy_path}")

if __name__ == "__main__":
    main()
