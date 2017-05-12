title: The AWS CLI Intro
slug: basic-cli
date: 13 May 2017
sortdate: 20170513
teaser: Learn to use the AWS CLI to set up users and buckets.

##Getting started with the AWS CLI

Outline:

* Set up a new user (gui)
* Spin up Amazon Linux AMI
* SSH into instance
* Set up a new user (CLI)
* Create a bucket with the CLI
* Clean up

In this article you will set up a new user with limited privilages. Why? So you're not always usint the root user with full privilages.

First we will set up a new user using the AWS gui. We'll assign the right permissions so this new user can use the CLI. Then we'll use the new user to do the same thing.

---

##Install the CLI

If you'd like to skip straight to the CLI part, you can just [install the AWS Command Line Interface][1] on your machine.

---

##Set up a new user in the GUI

1. First go to the IAM section of AWS and click on "Add user".
2. Enter a name. For this tutorial I'll use the name "new_user".
3. Check the boxes for "Programatic access" and "AWS Management Console access".
4. For **Console password** pick "Custom password" and remember it. We'll need it for the rest of this tutorial.
5. For this tutorial it's easier if you do not check the **Require password reset** box.
6. Click **Next permissions**
7. Click **Create group**. We'll use "new_group" for the name.
8. In the search box type in "ec2full". You should see the "AmazonEC2FullAccess" policy appear. Check the box.
9. In the search box type in "s3full". You should see the "AmazonS3FullAccess" policy appear. Check the box.
10. Click **Create group**. The "new_group" should be selected.
11. Click **Next: Review**
12. Create the user.
13. **IMPORTANT:** Download the access keys using the **Download .csv** button.
14. Save the sign-in link that appears in the green *Success* box.

If you do not download the access keys when prompted, you will not have programatic access for this user. The keys will never be displayed again. If you forgot to download them, just delete the user and start over.

---

##Spin up an Amazon Linux AMI

Why Amazon Linux? Because it comes with the AWS CLI preinstalled. If you've never done this before, there are a few points to be aware of in this process.

The first is that AWS separates the EC2 resource from the definition of web traffic. This means you will have to set up two things

* EC2
* Security Group

The security group will allow you to define an SSH rule. Without this rule you won't be able to log in to your instance and have access to the shell.

The second point is that you are going to need `.pem` (or `.ppk` for Windows users) keys to access your instance. These will be available for download only once and if you forget to download them you will have delete your instance and spin up a new one. This will happen just before you click the final create button.

To set up your instance follow this [10 min][2] tutorial. If you're on Windows I recommend you connect to your instance [like so][3]. If you're on linux

    ssh -i <path to MyNewKey.pem> ec2-user@<public ip>

---

##Configure your CLI

The first thing you will need to do once you're logged in to the instance is to set up your CLI with the new user's credentials.

    $ aws configure

You will need the access keys you downloaded as a `.csv` file earlier. **Make sure you enter the same region you're using in the console.** My default was `us-west-2`. More info on configuring your cli [here][4].

Now we'll set up a new user with the CLI.

---

##Set up a new user with the CLI

    $ aws iam create-group --group-name bowling

    $ aws iam attach-group-policy
        --group-name bowling
        --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess

    $ aws iam attach-group-policy
        --group-name bowling
        --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

    $ aws iam create-user --user-name dude

    $ aws iam add-user-to-group --user-name dude --group-name bowling

    $ aws iam get-group --group-name bowling

    $ aws iam list-attached-group-policies --group-name bowling

    $ aws iam create-login-profile --user-name dude --password weakpassword1

    $ aws iam create-access-key --user-name dude > spam

You might be asking, where did you get the arn for the permissions? And what the heck is an [arn][5] anyway?

    $ sudo apt-get install jq
    $ cat spam | jq '.'

    $ aws iam list-policies > foo
    $ cat foo | jq '.Policies[] | .Arn' | grep FullAccess > bar

Using [jq][6] is outside the scope of this tutorial. But it is amazing.

---

##Set up a bucket

Content coming soon.

---

##Conclusion

We've set up a user in two different ways. I'd argue that the CLI version was much more pleasant because menus and buttons were completely absent. If you'd like to explore the CLI more just add the `help` option to the command you'd like to use. For example if you want to explore what the CLI can do with EC2, you can use `aws ec2 help`. You can navigate the resulting menu using the keys `j` and `k` and search the document usint `/<search term>`. For those unfamiliar with this, it's like using [less][7].

---

[1]: http://docs.aws.amazon.com/cli/latest/userguide/installing.html "Installation instructions"
[2]: https://aws.amazon.com/getting-started/tutorials/launch-a-virtual-machine/
[3]: http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html
[4]: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
[5]: http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
[6]: https://stedolan.github.io/jq/ "sed for json"
[7]: https://linux.die.net/man/1/less
