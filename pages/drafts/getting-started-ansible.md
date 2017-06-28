title: Getting Started with Ansible on AWS
slug: getting-started-ansible
date: 21 June 2017
sortdate: 20170621
teaser: Deploy a sandbox environment to AWS in order to learn how to set up an Ansible system.
twitter: #

## The sandbox

I've created a sandbox environment to learn Ansible on. Many tutorials out there will deploy a server for you that's already set up and ready to go. Not here. This sandbox will start you with the stock AWS Ubuntu 16.04 image for your control node and several Ubuntu/Redhat/Windows machines. Nothing will be preinstalled on them. We'll have to set up the control node ourselves. By the end of this tutorial you will have installed Ansible and issued some `ping` commands.

## Install Terraform

Simple. Just a `wget` and `unzip`, then `ln -s` the binary to your `~/bin` and you're off. See the HashiCorp site for details.

## Network

The servers are all within the same AWS Security Group. I've opened ports 80, 443, 22 and 5986. Port 80 is necessary for `sudo apt-get update`, 443 for the ansible ppa, 22 for shell access and 5986 for Windows remote access.

## Run the sandbox

`terraform apply`

## Set up the control node

Install ansible (as of June 21, 2017):

    :::bash
    sudo apt-get install software-properties-common
    sudo apt-add-repository ppa:ansible/ansible
    sudo apt-get update
    sudo apt-get install ansible

The control node will need the ssh key to access the rest of the nodes. Copy it from your local machine to the control node.

   scp -i /path/to/key.pem /path/to/key.pem ubuntu@aws.control.node.publicip.com
