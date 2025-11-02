terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.4.0"
}

# -----------------------------
# Provider
# -----------------------------
provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

# -----------------------------
# Variables
# -----------------------------

variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "vpc_id" {}             # VPC ID
variable "subnet_id" {}          # Subnet ID
variable "security_group_id" {}  # Security Group ID

# -----------------------------
# EC2 instance for k3s master node
# -----------------------------
resource "aws_instance" "k3s_master" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnet_id
  key_name      = var.key_name

  vpc_security_group_ids = [var.security_group_id]

  # user_data.sh should install k3s automatically
  user_data = file("${path.module}/user_data.sh")

  tags = {
    Name = "k3s-master"
  }
}

# -----------------------------
# Outputs
# -----------------------------

output "instance_private_ip" {
  value = aws_instance.k3s_master.private_ip
}
# -----------------------------
# Generate kubeconfig for EKS
# -----------------------------
