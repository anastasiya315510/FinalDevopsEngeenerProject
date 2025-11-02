output "instance_public_ip" {
  value = aws_instance.k3s_master.public_ip
}

output "vpc_id" {
  value = aws_vpc.main.id
}
output "cluster_name" {
  description = "The EKS cluster name"
  value       = module.eks.cluster_name
}

output "kubeconfig" {
  description = "Kubeconfig for the EKS cluster"
  value       = module.eks.kubeconfig
}
