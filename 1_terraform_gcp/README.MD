1.3.1 Introduction Terraform: Concepts and Overview, a primer

Local application that communicates with providers (mostly cloud),
to setup up resources that can be grouped together as infrastructure for an organization.

Resources are provisioned through terraform files (.tf).  To provision each resource or
a group of resources, with provider, obvioudly there needs to be some some sort of
hieracrchical system of authentication.

Some commands:
init -  Get me the providers I need, once providers are defined
plan - what am I about to do. Will show you the resources that will be created.
apply -  do what is in ther tf files, go out and builf the infra.
destroy - tear all infra in .tf file dow.

1.3.2
1) Create a service account, (not a user account), this is not an account to login to,
must be sort of key access or an account to be able to attain services.
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
