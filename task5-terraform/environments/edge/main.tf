provider "aws" {
  region = "eu-central-1"
}

module "ec2_instance" {
  source              = "../../modules/ec2"
  instance_name       = var.instance_name
  instance_type       = var.instance_type
  ebs_volume_size     = var.ebs_volume_size
  allocate_eip        = var.allocate_eip
  ssh_whitelist_cidrs = var.ssh_whitelist_cidrs
  ami_id              = var.ami_id
  subnet_id           = var.subnet_id
  vpc_id              = var.vpc_id
  key_name            = var.key_name
  tags = {
    Environment = "edge"
    Owner       = "DevOps"
    Project     = "EC2Provisioning" }
}

