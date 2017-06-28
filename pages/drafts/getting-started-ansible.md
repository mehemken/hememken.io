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

    :::bash
    # continuing...
    mkdir work
    exit
    scp -i /path/to/key.pem \
        /path/to/key.pem \
        ubuntu@aws.control.node.publicdns.com:/home/ubuntu/work

Then you need to edit the `/etc/ansible/ansible.cfg` file to let it know where you are keeping your key. You will need the location for this edit. The line containing `private_key_file = /path/to/file` should be uncommented and the correct file path should be used. In this case it should be

    private_key_file = /home/ubuntu/work/key.pem

We will now run into errors if we try to `ansible ubuntu -m ping`. The AWS Ubuntu 16.04 ami does not come with python 2 by default. It comes with python 3. Disaster? Nope. The default user for a RedHat ami in AWS is `ec2-user`. Ansible does not know this out of the box. Now disaster? Nope. If our original host file looks like this

    [ubuntu]
    public_dns.of.ubuntu.machine_1.com
    public_dns.of.ubuntu.machine_2.com

    [redhat]
    public_dns.of.redhat.machine_1.com
    public_dns.of.redhat.machine_2.com
    public_dns.of.redhat.machine_3.com

    [windows]
    public_dns.of.windows.machine_1.com
    public_dns.of.windows.machine_2.com

We just need to add some vars.

    [ubuntu:vars]
    ansible_python_interpreter=/usr/bin/python3

    [redhat:vars]
    ansible_user=ec2-user

This is the manual way to set up your host file. There is also something called dynamic inventory. It will pull a list of resources from somewhere and create your inventory from it as it grows and shrinks.

More on that another time. For now you can try to ping your linux hosts.

    ansible ubuntu -m ping
    ansible redhat -m ping
    ansible linux -m ping

The first command only hits the ubuntu servers, the second just the redhats and if we add one more thing to our inventory, we'll hit all our linuxes.

    [linux:children]
    ubuntu
    redhat

More on Windows in a future post.

## Windows

For Windows to work with Ansible, we have to log in to each server and activate WinRM manually. I'm curious to see if this can be automated. Ok first we need `pywinrm`. But for some reason the control node doesn't have pip.

    sudo easy_install pip
    sudo pip install pywinrm

Some root level directories need to be changed so we need `sudo pip` rather than regular `pip`.

Now we need to RDP into our windows instances. First we get our passwords

    aws ec2 get-password-data \
        --instance-id i-23498752 \
        --priv-launch-key /path/to/key.pem

If you don't include the launch key the password data will be encrypted. Now we open up port 3389 for RDP. Then we use a client such as Remmina to log in to our instance(s). This is necessary to activate WinRM.

Copy the [ansible setup script][1] to a notepad file and save it to the desktop. Open an administrator powershell and drag the file to the shell. It should run. When it is done you can disconnect.

We'll need to adjust our inventory.

    [first]
    ec2-first-windows-server.com

    [second]
    ec2-second-windows-server.com

    [windows:children]
    first
    second

Perhaps there is a more elegant way to do this, but it's the first way I've found to ping all machines even though they have unique passwords. We need to add the variables to the [windows inventory][2] so ansible knows what the passwords are. Copy the format in that there link.

And we're done.

    ansible windows -m win_ping

---
[1]: https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1 "manual process"
[2]: http://docs.ansible.com/ansible/intro_windows.html#inventory "windows passwords"
