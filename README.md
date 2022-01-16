# Lakformation

This is an attempt to set up a governed table in cloudguru.
It did not work because cloudguru put a service control policy denial on lakeformation resources.

## Attempt

The dir `terraform_cloud_user` holds the terraform for running as the `cloud_user` and the dir
`terraform_data_engineer` should be run as `data_engineer` user.  The idea behind the separate users
is to use the `data_engineer` user with specific iam permissions, since the denial was thought to be
based on permissions given to `cloud_user` out of the box.

### Steps

- run `just terraform_apply_cloud_user` and then in the console retrieve the security credentials.  Add the credentials to a profile called `data_engineer` in `~/.aws/credentials`
- run `just terraform_apply_data_engineer`

### aws profiles

You will need to have a `cloud_user` profile in your `~/.aws/credentials` and then add a `data_engineer` profile.

## Justfile

To make shell commands to run, you will use `just` rather than `make`.  You can install `just` through
`brew install just`.
