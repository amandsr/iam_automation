import boto3
import json
from pathlib import Path

def get_iam_client(profile_name=None):
    if profile_name:
        session = boto3.Session(profile_name=profile_name)
        return session.client("iam"), session
    else:
        session = boto3.Session()
        return session.client("iam"), session

def get_account_id(session):
    sts = session.client("sts")
    identity = sts.get_caller_identity()
    return identity["Account"]

def role_exists(iam_client, role_name):
    try:
        iam_client.get_role(RoleName=role_name)
        return True
    except iam_client.exceptions.NoSuchEntityException:
        return False

def main():
    profile_name = "prod"  # Replace with your profile or None
    iam, session = get_iam_client(profile_name)

    input_file = Path("iam_policy_orchestration_full/inputs/user_input.json")
    with input_file.open() as f:
        data = json.load(f)

    role_name = data["role_name"]
    policy_name = data["policy_name"]

    account_id = get_account_id(session)

    if role_exists(iam, role_name):
        print(f"✅ Role '{role_name}' exists in AWS.")
        print("Run the following commands to import into Terraform:\n")
        print(f"terraform import aws_iam_role.this {role_name}")
        print(f"terraform import aws_iam_policy.this arn:aws:iam::{account_id}:policy/{policy_name}")
        print(f"terraform import aws_iam_role_policy_attachment.this {role_name}/{policy_name}\n")
    else:
        print(f"🔧 Role '{role_name}' does not exist yet. Terraform will create it.")

if __name__ == "__main__":
    main()
