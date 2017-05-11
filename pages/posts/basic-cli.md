title: The AWS CLI Intro
slug: basic-cli
date: 14 May 2017
sortdate: 20170514

##Getting started with the AWS CLI

Outline:

* Set up a new user
* Give ec2 and s3 permissions
* Create keys
* Spin up Amazon Linux AMI
* Create security group
* SSH into instance
* Create a bucket with the CLI

---

##Install the CLI

Prerequisite for this tutorial is [installing the AWS Command Line Interface][1].

[1]: http://docs.aws.amazon.com/cli/latest/userguide/installing.html "Installation instructions"

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

    ######
    # Extra credit...
    # How did you know what the arn
    # was for those policies??

    $ sudo apt-get install jq
    $ cat spam | jq '.'

    $ aws iam list-policies > foo
    $ cat foo | jq '.Policies[] | .Arn' | grep FullAccess > bar
    $ less bar  #use keys j and k to navigate up and down
