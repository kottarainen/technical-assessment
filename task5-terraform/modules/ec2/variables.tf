variable "instance_name" {
  description = "Name of the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
}

variable "ebs_volume_size" {
  description = "Size of the root EBS volume in GB"
  type        = number
}

variable "allocate_eip" {
  description = "Whether to allocate an Elastic IP"
  type        = bool
}

variable "ssh_whitelist_cidrs" {
  description = "List of CIDR blocks allowed to SSH"
  type        = list(string)
}

variable "ami_id" {
  description = "AMI ID to use"
  type        = string
}

variable "subnet_id" {
  description = "Subnet where EC2 instance will be launched"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID for the security group"
  type        = string
}

variable "key_name" {
  description = "Name of the SSH key pair to use"
  type        = string
}
