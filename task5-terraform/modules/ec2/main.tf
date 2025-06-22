resource "aws_security_group" "ssh_sg" {
  name        = "${var.instance_name}-sg"
  description = "Allow SSH from whitelisted IPs"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.ssh_whitelist_cidrs
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "this" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_name
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.ssh_sg.id]
  tags = {
    Name = var.instance_name
  }

  root_block_device {
    volume_size = var.ebs_volume_size
    volume_type = "gp3"
  }
}

resource "aws_eip" "this" {
  count      = var.allocate_eip ? 1 : 0
  instance   = aws_instance.this.id
  domain     = "vpc"
  depends_on = [aws_instance.this]
}
