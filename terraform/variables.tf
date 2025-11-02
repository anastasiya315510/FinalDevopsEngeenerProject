variable "aws_region" {
  default = "us-east-2"
}

variable "ami_id" {
  description = "Ubuntu 22.04 AMI ID"
  default     = "ami-083b3f53cbda7e5a4"
}

variable "instance_type" {
  default = "t2.small"
}

variable "key_name" {
  description = "Existing AWS key pair for SSH"
}
