title: Getting started w/ AWS CLI
slug: getting-started-cli-boto3
date: 13 May 2017
sortdate: 20170513

[1]: http://docs.aws.amazon.com/cli/latest/userguide/installing.html "Installing the AWS CLI"
[2]: http://docs.aws.amazon.com/cli/latest/userguide/cli-command-completion.html "AWS CLI autocompletion guide"
[3]: http://docs.aws.amazon.com/cli/latest/userguide/cli-command-completion.html#cli-command-completion-completer "Locate the AWS Completer"
[4]: https://aws.amazon.com/documentation/cloudformation/ "CloudFormation Docs"
[5]: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#aws-resource-ec2-instance-syntax "EC2 Syntax"
[6]: https://gist.github.com/mehemken/f9e2c5285f91f2afe7cba5fd49d85893 "TaaG"

This post is in progress...

You can find the complete CloudFormation [template as a gist][6] on my GitHub page.

##Installing the AWS CLI

First and foremost, I recommend the [AWS CLI Installation Instructions][1] provided by Amazon. They are pretty straightforward (if you're on linux). I can only vouch for the Linux version of this as I have not tried it on Windows.

If you are working on a Windows system you won't be able to follow along in this tutorial. I recommend you spin up a VM or dual boot your computer. Or better yet, spin up an EC2 instance and connect to it. I recommend using the Amazon Linux AMI as it comes with the AWS CLI preinstalled [citation needed]. If you have Ubuntu and Python 2.6.5+ or Python 3.3+ installation is as easy as

    $ pip install --upgrade --user awscli

For more info on the flags there see the [AWS Docs][1] on it. After you've installed it you may need to add the tool to your PATH. The default directory where the CLI is installed is `~/.local/bin`, but double check first.

    $ ls ~/.local/bin
    aws                 aws_zsh_completer.sh  ...
    aws_bash_completer  jp.py                 ...
    ...
    $ export PATH=~/.local/bin:$PATH

If you don't see the `aws` binary in that directory, you'll have to do some troubleshooting. See the [docs][1]. Another thing you might find useful is [autocompletion][2]. This should be as easy as adding a line to your terminal emulator's rc file.

If you don't know what terminal you have, you're most likely using bash. In your favorite editor open `~/.bashrc`. For those new to a Linux environment, it is a hidden file so you may not be able to see it by default in your file finder. There should be an option somewhere to reveal it. Add this to the end of the file

    complete -C '<installation directory>/aws_completer' aws

Where `<installation directory>` is [the directory where pip installed the AWS CLI][3]. I happen to be using the zsh completer and I didn't run into any issues with the instructions on the AWS [autocompletion Docs][2].

---

##First steps with the cli

One of the simplest things you can do is create a key pair. For those completely new to AWS, key pairs are used to connect to an EC2 instance securely. The CLI has a command for this.

    aws ec2 create-key-pair \
        --key-name MyKeyPair \
        --query 'KeyMaterial' \
        --output text > MyKeyPair.pem

It looks like there are a lot of flags here. They are all necessary. The `create-key-pair` command creates the key and keeps it somewhere you can access it from your AWS account. The `--key-name` is required so you can identify the key. The command will return a few different parts of the key including the fingerprint and name etc. in json format. You don't need all that. You just need the KeyMaterial, hence the `--query` flag.finally, you need to store the key on your machine so you can use it to log in to your instance. The `--output` flag ensures you receive the KeyMaterial in the proper format. Finally, if you're not familiar with bash, this line

    ... > MyKeyPair.pem

just takes the output of the previous command and creates a new file with the content. This way, you have a key ready to use.

Funny enough,

    $ aws ec2 instance create   # This doesn't exist

You need a little more information. A great way to provide this information is in a json document.

    // automate-things.json
    {
        "Resources" : {
            "HelloT2micro" : {
                "Type" : "AWS::EC2::Instance",
                "Properties" : {
                    "InstanceType" : "t2.micro",
                    "ImageId" : "ami-4836a428",
                    "KeyName": "MyKeyPair",
                    "Tags" : [ {"Key":"Name", "Value":"El Duderino"} ]
                }
            }
        }
    }

These are some of the options you can set when you're using the AWS gui. Now you can say goodbye to slow page loads and mouse clicks on menus. To start your instance

    $ aws cloudformation deploy \
        --template-file automate-things.json \
        --stack-name ec2only

If all goes well, you should be able to go to your AWS console's CloudFormation panel and see the resource spin up.

If you try to connect to it you'll notice you don't have access.

    $ ssh -i MyKeyPair.pem ec2-user@<public ip address>

And that's because you have the key pair, but no security group. But that's easy to add. Note that we create the security group and update the EC2 instance definition.

    // automation-things.json
    {
        "Resources" : {
            "HelloT2micro" : {
                "Type" : "AWS::EC2::Instance",
                "Properties" : {
                    "InstanceType" : "t2.micro",
                    "ImageId" : "ami-4836a428",
                    "SecurityGroups": [ "the-money-sg" ],
                    "KeyName": "MyKeyPair",
                    "Tags" : [ {"Key":"Name", "Value":"El Duderino"} ]
                }
            },
            "HelloSecurityGroup": {
                "Type": "AWS::EC2::SecurityGroup",
                "Properties": {
                    "GroupName": "the-money-sg",
                    "GroupDescription": "Equal access for all",
                    "SecurityGroupIngress": [ {
                        "IpProtocol": "tcp",
                        "FromPort": "22",
                        "ToPort": "22",
                        "CidrIp": "0.0.0.0/0"
                    } ]
                }
            }
        }
    }

Now, without tearing down the old instance, we use the same deploy command

    $ aws cloudformation deploy \
        --template-file automate-things.json \
        --stack-name ec2only

You will see in the CloudFormation console that the stack is updating.

    $ ssh -i bar.pem ec2-user@35.167.202.35
    ... # skipped a few lines

           __|  __|_  )
           _|  (     /   Amazon Linux AMI
          ___|\___|___|

    https://aws.amazon.com/amazon-linux-ami/2017.03-release-notes/
    6 package(s) needed for security, out of 6 available
    Run "sudo yum update" to apply all updates.
    [ec2-user@ip-172-31-21-130 ~]$

And you can connect to the instance. That's an easy demo, but I promised a little IAM so I'll add a bucket to show this.

    // automate-things.json
    {
        "Resources" : {
            "HelloT2micro" : {
                "Type" : "AWS::EC2::Instance",
                "Properties" : {
                    "InstanceType" : "t2.micro",
                    "ImageId" : "ami-4836a428",
                    "SecurityGroups": [ "the-money-sg" ],
                    "KeyName": "MyKeyPair",
                    "Tags" : [ {"Key":"Name", "Value":"El Duderino"} ]
                }
            },
            "HelloSecurityGroup": {
                "Type": "AWS::EC2::SecurityGroup",
                "Properties": {
                    "GroupName": "the-money-sg",
                    "GroupDescription": "Equal access for all",
                    "SecurityGroupIngress": [ {
                        "IpProtocol": "tcp",
                        "FromPort": "22",
                        "ToPort": "22",
                        "CidrIp": "0.0.0.0/0"
                    } ]
                }
            },
            "HelloBucket" : {
                "Type" : "AWS::S3::Bucket",
                "Properties": {
                    "BucketName": "treehorn12345"
                }
            }
        }
    }

Run the same deploy command as above.

Ok so we have a bucket and an EC2 instance. You'll notice that if you log in to the EC2 instance you can't see anything in the bucket. 

    [ec2-user@ip-172-31-21-130 ~]$ aws s3 ls
    Unable to locate credentials. You can configure credentials by running "aws configure".

That is a good thing. If someone hacks into the instance you don't want them to also have access to your data.

Ok, so how do we manage these permissions? Should we add a user? or a group? No! IAM has this thing called roles. And the way they work is like hats. The role can be assumed by any user or group or, in this case, a resource. You can easily have a resource assume a role when it needs extra permissions and revoke the role once it's done. Ok enough theory let's see something happen.

We'll need to create the role. In this case we'll just add it to our template.

    // automate-things.json
    {
        "Resources" : {
            "HelloT2micro" : {
                "Type" : "AWS::EC2::Instance",
                "Properties" : {
                    "InstanceType" : "t2.micro",
                    "ImageId" : "ami-4836a428",
                    "SecurityGroups": [ "the-money-sg" ],
                    "KeyName": "MyKeyPair",
                    "Tags" : [ {"Key":"Name", "Value":"El Duderino"} ]
                }
            },
            "HelloSecurityGroup": {
                "Type": "AWS::EC2::SecurityGroup",
                "Properties": {
                    "GroupName": "the-money-sg",
                    "GroupDescription": "Equal access for all",
                    "SecurityGroupIngress": [ {
                        "IpProtocol": "tcp",
                        "FromPort": "22",
                        "ToPort": "22",
                        "CidrIp": "0.0.0.0/0"
                    } ]
                }
            },
            "HelloBucket" : {
                "Type" : "AWS::S3::Bucket",
                "Properties": {
                    "BucketName": "treehorn12345"
                }
            },
            "HelloIAM" : {
                "Type" : "AWS::IAM::Role",
                "Properties": {
                    "AssumeRolePolicyDocument": {
                        "Statement": [ {
                            "Effect": "Allow",
                            "Principal": {
                                "Service": [ "ec2.amazonaws.com" ]
                            },
                            "Action": [ "sts:AssumeRole" ]
                        } ]
                    },
                    "Path": "/",
                    "Policies": [ {
                        "PolicyName": "lebowski",
                        "PolicyDocument": {
                            "Statement": [ {
                                "Effect": "Allow",
                                "Action": [
                                    "s3:ListAllMyBuckets",
                                    "s3:ListBucket"
                                ],
                                "Resource": "*"
                            } ]
                        }
                    } ]
                }
            }
        }
    }

We have added an IAM role that says,

* The principal must be an EC2 instance
* The policies allowed are the listing of buckets

But you will get an error when you try to deploy. You need to adjust your deploy command to this

    $ aws cloudformation deploy \
        --template-file automate-things.json \
        --stack-name ec2only \
        --capabilities CAPABILITY_IAM

Ok we're done, let's run it. You can try the `aws s3 ls` command to list all the buckets, but you will get the same `Unable to find credentials` message as before because we are missing one last thing.

The way AWS is designed, we need two IAM components in order to assign permissions to an EC2 instance. The `AWS::IAM::Role` is the first, but we also need the `AWS::IAM::InstanceProfile`. And this is really useful, because it allows you to update the roles without having to create a whole new instance.

A little tangent here. When we update our instance with the `aws cloudformation deploy` command, AWS does not go in and install stuff. It creates a whole new instance and deletes the old one. All of this is invisible to you as a user as it happens in the background.

But not all updates to your stack warrant a new instance. For example, when we added the S3 bucket, AWS did not have to do it. When we added the security group, we also added the key. This was new for the instance so AWS created a new one. You can see each step with a simple command

    $ aws cloudformation describe-stack 
        --stackname ec2only > foo
    $ less foo

So when we add the `AWS::IAM::InstanceProfile` we also update the instance to know that it should look for its IAM permissions in that InstanceProfile.

    // automate-things.json
    {
        "Resources" : {
            "HelloT2micro" : {
                "Type" : "AWS::EC2::Instance",
                "Properties" : {
                    "InstanceType" : "t2.micro",
                    "ImageId" : "ami-4836a428",
                    "SecurityGroups": [ "the-money-sg" ],
                    "IamInstanceProfile": "HelloInstanceProfile",
                    "KeyName": "MyKeyPair",
                    "Tags" : [ {"Key":"Name", "Value":"El Duderino"} ]
                }
            },
            "HelloSecurityGroup": {
                "Type": "AWS::EC2::SecurityGroup",
                "Properties": {
                    "GroupName": "the-money-sg",
                    "GroupDescription": "Equal access for all",
                    "SecurityGroupIngress": [ {
                        "IpProtocol": "tcp",
                        "FromPort": "22",
                        "ToPort": "22",
                        "CidrIp": "0.0.0.0/0"
                    } ]
                }
            },
            "HelloBucket" : {
                "Type" : "AWS::S3::Bucket",
                "Properties": {
                    "BucketName": "treehorn12345"
                }
            },
            "HelloIAM" : {
                "Type" : "AWS::IAM::Role",
                "Properties": {
                    "AssumeRolePolicyDocument": {
                        "Statement": [ {
                            "Effect": "Allow",
                            "Principal": {
                                "Service": [ "ec2.amazonaws.com" ]
                            },
                            "Action": [ "sts:AssumeRole" ]
                        } ]
                    },
                    "Path": "/",
                    "Policies": [ {
                        "PolicyName": "lebowski",
                        "PolicyDocument": {
                            "Statement": [ {
                                "Effect": "Allow",
                                "Action": [
                                    "s3:ListAllMyBuckets",
                                    "s3:ListBucket"
                                ],
                                "Resource": "*"
                            } ]
                        }
                    } ]
                }
            },
            "HelloInstanceProfile": {
                "Type": "AWS::IAM::InstanceProfile",
                "Properties": {
                    "Roles": [ {
                        "Ref": "HelloIAM"
                    } ],
                    "InstanceProfileName": "HIPname"
                }
            }
        }
    }

Now when you run this you can log in to your EC2, you can see your bucket and your EC2 can see your bucket.

    $ aws s3 ls
    # list of buckets

This concludes our demo for today.
