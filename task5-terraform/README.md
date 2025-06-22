# Task 5: Infrastructure Provisioning

This Terraform configuration provisions EC2 instances across multiple AWS environments (edge, stable, production).

---

## Scenario

A system must provision EC2 machines in multiple AWS accounts: `edge`, `stable`, and `production`. Each instance must be configured using inputs.

- The module must be invoked via:
  ```hcl
  module "my_instance" {
    # params...
  }

## Features

- Reusable module under modules/ec2
- Parameterized inputs for customization
- Automated tagging for environment tracking
- State stored in S3 per environment
- State locking using DynamoDB tables
- Fully environment-isolated deployments

## Module Inputs

| Variable              | Type           | Description                                                    |
|-----------------------|----------------|----------------------------------------------------------------|
| `instance_name`       | `string`       | Name tag and identifier for the EC2 instance                   |
| `instance_type`       | `string`       | EC2 instance type (e.g., `t3.micro`)                           |
| `ebs_volume_size`     | `number`       | Size (in GB) of the root EBS volume                            |
| `allocate_eip`        | `bool`         | Whether to allocate and associate an Elastic IP                |
| `ssh_whitelist_cidrs` |  `list(string)`| List of CIDR blocks allowed to SSH into the instance           |
| `ami_id`              | `string`       | ID of the Amazon Machine Image used to launch the instance     |
| `subnet_id`           | `string`       | Subnet ID where the EC2 instance will be launched              |
| `vpc_id`              | `string`       | VPC ID where the security group will be created                |
| `key_name`            | `string`       | Name of the AWS key pair used for SSH access                   |
| `tags`                | `map(string)`  | Map of custom tags to assign to all created resources          |

## Remote state setup

A remote backend is used to store the Terraform state files in an S3 bucket and manage locking via DynamoDB. Each environment (`edge`, `stable`, `production`) has its own backend configuration.

## Usage

To launch an EC2 instance using this module in a specific environment, navigate to the corresponding environment folder and run standard Terraform commands.

Navigate to the desired environment directory:
cd environments/edge

Initialize the backend and install the module:
terraform init

Preview planned changes:
terraform plan -var-file="terraform.tfvars"

Apply the changes:
terraform apply -var-file="terraform.tfvars"

## Notes

- **Tags** such as `Environment`, `Project`, `Owner`, etc., can be added via the `tags` map in the module for better resource tracking and cost allocation.

- **Remote state resources** (`S3` buckets and `DynamoDB` tables) must be pre-created before running `terraform init` in each environment. The module setup assumes these already exist.

- **Use valid values** for the following parameters in each environment's `terraform.tfvars`:
  - `ami_id`: Ensure the AMI exists and is available in the region.
  - `subnet_id`: Should belong to the correct VPC.
  - `vpc_id`: Must match the subnet and be valid for the selected region.
