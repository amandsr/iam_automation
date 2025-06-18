import json
import re
from collections import defaultdict
from pathlib import Path

def parse_input(text):
    data = {
        "role_name": "",
        "policy_name": "",
        "assume_role_policy": None,
        "statements": []
    }
    statements_temp = defaultdict(dict)

    lines = [line.strip() for line in text.strip().splitlines() if line.strip() and not line.startswith("#")]

    for line in lines:
        if ":" not in line:
            continue
        key, val = map(str.strip, line.split(":", 1))

        # Top-level metadata
        if key == "role_name":
            data["role_name"] = val
        elif key == "policy_name":
            data["policy_name"] = val
        elif key == "assume_role_policy":
            data["assume_role_policy"] = {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {
                        "Service": val
                    },
                    "Action": "sts:AssumeRole"
                }]
            }
        else:
            match = re.match(r"statement(\d+)\.(.+)", key)
            if not match:
                continue
            stmt_idx = int(match.group(1)) - 1
            prop = match.group(2)

            # Handle nested condition structure
            if prop.startswith("condition."):
                cond_path = prop.split(".")[1:]  # drop "condition"
                current = statements_temp[stmt_idx].setdefault("condition", {})
                for p in cond_path[:-1]:
                    current = current.setdefault(p, {})
                current[cond_path[-1]] = convert_value(val)
            elif prop in ("actions", "resources"):
                statements_temp[stmt_idx][prop] = [v.strip() for v in val.split(",")]
            else:
                statements_temp[stmt_idx][prop] = convert_value(val)

    # Convert dict to list
    for idx in sorted(statements_temp.keys()):
        data["statements"].append(statements_temp[idx])

    return data

def convert_value(val):
    if val.lower() == "true":
        return True
    elif val.lower() == "false":
        return False
    return val

def main():
    input_file = Path("iam_policy_orchestration_full/inputs/user_input.txt")
    output_file = Path("iam_policy_orchestration_full/inputs/user_input.json")

    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        return

    with open(input_file) as f:
        user_input_text = f.read()

    json_output = parse_input(user_input_text)

    with open(output_file, "w") as out:
        json.dump(json_output, out, indent=2)

    print(f"✅ Generated JSON written to: {output_file}")

if __name__ == "__main__":
    main()
