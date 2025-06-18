import json
from pathlib import Path

input_txt = Path("inputs/user_input.txt")
output_tfvars = Path("terraform/environments/auto_inputs.tfvars.json")

# Keys to extract for Terraform
terraform_keys = ["role_name", "policy_name"]
vars_dict = {}

with input_txt.open() as f:
    for line in f:
        if ":" not in line:
            continue
        key, value = line.strip().split(":", 1)
        key = key.strip()
        value = value.strip()

        if key in terraform_keys:
            vars_dict[key] = value

# Ensure output directory exists
output_tfvars.parent.mkdir(parents=True, exist_ok=True)

# Write Terraform variables to tfvars.json
with output_tfvars.open("w") as f:
    json.dump(vars_dict, f, indent=2)

print(f"✅ Terraform tfvars written to: {output_tfvars}")
