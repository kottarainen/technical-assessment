terraform {
  backend "s3" {
    bucket         = "tf-state-prod"
    key            = "ec2/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "tf-locks-prod"
    encrypt        = true
  }
}
