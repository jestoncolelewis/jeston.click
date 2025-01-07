terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.54.1"
    }
  }
}
provider "aws" {
  region = var.aws_region
}
provider "aws" {
  alias = "acm_provide"
  region = "us-east-1"
}