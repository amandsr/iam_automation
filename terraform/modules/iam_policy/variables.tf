variable "assume_role_policy_file" {
  description = "Path to the assume role policy JSON file"
  type        = string
  default     = ""
}

variable "policy_json_file" {
  description = "Path to the generated IAM policy JSON file"
  type        = string
}

variable "policy_name" {
  type = string
}

variable "role_name" {
  type = string
}