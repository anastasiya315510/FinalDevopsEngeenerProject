terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.4.0"
}

provider "aws" {
  region = var.aws_region
}


# EC2 instance for k3s master node
resource "aws_instance" "k3s_master" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.main.id
  key_name      = var.key_name

  vpc_security_group_ids = [aws_security_group.k3s_sg.id]

  user_data = file("${path.module}/user_data.sh")

  tags = {
    Name = "k3s-master"
  }
}
