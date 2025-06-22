terraform {
  backend "s3" {
    bucket         = "tf-state-edge"
    key            = "ec2/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "tf-locks-edge"
    encrypt        = true
  }
}
