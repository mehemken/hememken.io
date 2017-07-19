title: Ansible basics with Linux and Windows
slug: intro-to-ansible
date: 18 July 2017
sortdate: 20170718
teaser: How to set up an EC2 cluster with ansible and some linux and windows machines.
twitter: #

# Summary

This post is a summary of the steps needed to set up and control a cluster of servers with Ansible. I'm making the assumption that you're not using your desktop machine as the control node, you will be using some remote server. Thus you'll need to install ansible there and copy the key you'll be using to that server.

Getting stuff to work for Linux nodes is very simple. They are controlled with SSH, and because we have an RSA key, we can just let Ansible deal with the SSH. Windows machines are not quite so simple. You will need to manually log in to each machine and run a script so Ansible can run powershell remotely on the machine. There are probably ways to automate this, but I've not had time to search for them yet.

By the end of this article you'll have seen all the necessary commands to have an Ansible control node, and various Linux/Windows nodes. I've kept explanatory text very thin, so this can be used as a quick-reference.

---

# Installation on host machine

You'll need a control node that runs Linux. I've been using an Ubuntu 16.04 control node and I've installed ansible like this.

    sudo apt-get install software-properties-common
    sudo apt-add-repository ppa:ansible/ansible
    sudo apt-get update
    sudo apt-get install ansible

## The key

Ansible controls remote nodes using SSH by default. Generate a new key and copy the private key to the control node. If you're using AWS (like I am), just create a new key and copy it to the control node. Copy the key to the host machine:

    scp -i /path/to/first/key.pem /path/to/second/key.pem user@hostmachine:/remote/path/to/second/key.pem

In this example, the first key is the one you're using to ssh into your control node. The second key is the key Ansible will use to manage worker nodes.

Ansible needs to know the path to the second key. Make sure you change the config file in `/etc/ansible/ansible.cfg`. 


---

# Windows

I'm not terribly stoked about this, but you have to manually log in to each Windows server to use it with ansible. Perhaps this isn't an issue if I use the AWS dynamic inventory scripts. Or maybe it's still an inconvenience. I don't know. More on that next time.

## Pywinrm

Ok first we need `pywinrm` on the control node. Ansible uses this to do remote powershell. If your control node doesn't have pip (AWS Ubuntu 16.04 had this issue) you'll need ot get pip first.

    sudo easy_install pip
    sudo pip install pywinrm

Some root level directories need to be changed so we need `sudo pip` rather than regular `pip`.

## Windows login info (AWS)

Now we need to RDP into our windows instances. First we get our passwords

    aws ec2 get-password-data \
        --instance-id i-23498752 \
        --priv-launch-key /path/to/key.pem

If you don't include the launch key the password data will be encrypted (aka useless).

## Remote desktop

Now we open up port 3389 for RDP (I assume you know how to do that with [AWS security goups][3]). Then we use a client such as [Remmina][4] (or equivalent) to log in to our instance(s). This is necessary to activate WinRM.

Copy the [ansible setup script][1] to a notepad file and save it to the desktop. Open an administrator powershell and drag the file to the shell. It should run. When it is done you can disconnect.

## Windows group_vars

We need to add the variables to the [windows inventory][2] so ansible knows what the passwords are. Copy the format in that there link.

And we're done.

    ansible windows-machine -m win_ping

---

# Useful bits of config

## Python on Ubuntu 16.04

Ansible is written in Python and runs modules that are also written in Python. The remote machine will need to have Python installed. Ubuntu 16.04 as it exists on EC2 only has `python3` by default. You should configure your host file to know this.

    [xenial:vars]
    ansible_python_interpreter=/usr/bin/python3

## Redhat on AWS

Redhat on EC2 has the user `ec2-user` by default. You must let the host file know this.

    [redhat:vars]
    ansible_user=ec2-user

## Ping all Windows machines

Perhaps there is a more elegant way to do this, but here's how to ping all machines even though they have unique passwords. 

We'll need to adjust our inventory.

    [first]
    ec2-first-windows-server.com

    [second]
    ec2-second-windows-server.com

    [windows:children]
    first
    second

---

# Conclusion

I've given a very brief overview of what to do to set up a cluster of servers you can control with Ansible. You've now seen everything it takes to set up a control node, various worker nodes and control them with Ansible. One major flaw here is that I've not shown how to automate the Windows worker nodes. Windows does not ship with remote powershell activated by default. That's why we have to manually log in and activate it with the powershell script. I'm sure there's a way, so if you know how to do that, please let me know!

---
[1]: https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1 "manual process"
[2]: http://docs.ansible.com/ansible/intro_windows.html#inventory "windows passwords"
[3]: http://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/authorizing-access-to-an-instance.html "AWS Windows Ingress Rules Docs"
[4]: https://www.remmina.org/wp/ "Remmina RDP client for Linux"
