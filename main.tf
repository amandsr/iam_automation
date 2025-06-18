provider "aws" {
  region  = "us-east-1"
  profile = "prod"
}

variable "role_name" {
  type = string
}

variable "policy_name" {
  type = string
}

locals {
  assume_role_policy_json = var.assume_role_policy_file != "" ? file(var.assume_role_policy_file) : null
}

module "iam_policy" {
  source           = "../../modules/iam_policy"
  assume_role_policy_file = "${path.module}/assume_role_policy.json"
  policy_json_file        = "${path.module}/generated_policy.json"
  policy_name             = var.policy_name
  role_name               = var.role_name
}

