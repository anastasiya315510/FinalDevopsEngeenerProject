output "instance_public_ip" {
  value = aws_instance.k3s_master.public_ip
}

output "vpc_id" {
  value = aws_vpc.main.id
}

