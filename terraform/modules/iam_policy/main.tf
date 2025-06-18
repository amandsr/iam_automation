resource "aws_iam_role" "this" {
  name               = var.role_name
  assume_role_policy  = file(var.assume_role_policy_file)
}

resource "aws_iam_policy" "this" {
  name   = var.policy_name
  policy = file(var.policy_json_file)
}

resource "aws_iam_role_policy_attachment" "this" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.this.arn
}
