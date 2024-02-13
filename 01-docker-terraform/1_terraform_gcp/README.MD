1.3.1 Introduction Terraform: Concepts and Overview, a primer

Local application that communicates with providers (mostly cloud),
to setup up resources that can be grouped together as infrastructure for an organization.

Resources are provisioned through terraform files (.tf).  To provision each resource or
a group of resources, with provider, obviously there needs to be some some sort of
hieracrchical system of authentication.


Some commands:
init -  Get me the providers I need, once providers are defined
plan - what am I about to do. Will show you the resources that will be created.
apply -  do what is in ther tf files, go out and builf the infra.
destroy - tear all infra in .tf file dow.
terraform fmt -  format your tf file so indents are alligned

1.3.2 Terraform Basics: Simple one file Terraform Deployment
1) Create a service account, (not a user account), this is not a login account,
its an account to be able to attain services usually automated thru a secret key.
--> Nav menu
    --> IAM & Admin (giving broad rights, 2x admin, doesnt mean its needed)
        --> Service accounts
            Service account details
            --> Name the service: Terraform runner
            Grant this service account access to project
            -->Role(s):
            Cloud Storage/Storage Admin (to create a bucket)
            Big Query/Big Query Admin (BQ dataset)
            Compute Engine/Compute Admin
        --> Service accounts
            Manage keys
            --> Add key --> Create New Key --> JSON key
            (Key ID under associated Service A/C)

2) terraform init
Will bring up all the api info to be able to talk run commands to setup
resources on gcp.
You will see a .terraform folder and terraform.lock.hcl file

a) Use provider (in our case) gcp configs from Hashicorp website:
terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "5.15.0"
    }
  }
}

provider "google" {
  # Configuration options
  credentials = ${GOOGLE_CREDENTIALS}
  project     = "proven-catcher-411305"
  region      = "us-central1"
}

b) Resource (storage bucket):
For the name uniqueness of a storage bucket u can use a combo of project name
and description.
resource "google_storage_bucket" "gcp-data-lake-bucket" {
  name          = "auto-expiring-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

c) terraform plan
Shows you what resources main.tf is about to provision.

d) terraform apply
Applies the the main.tf provosioning and saves the state in a
terraform.tf.state file

e) terraform destory
Destroys all that was provisioned in the terraform.tfstate file and creates
as back of the lineage of all provision resources terraform.tfstate.backup

