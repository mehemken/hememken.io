title: Create an AWS KeyPair with the CLI
slug: create-keys-aws
date: 15 June 2017
sortdate: 20170615
teaser: The command needs a few flags. Refresh your memory here.
twitter: https://twitter.com/mehemken/status/875352479449444354

##Key Pairs in the CLI

The source of this post is [the AWS docs][1]. The reason you need the flags here is that you can create the key pair in the CLI, but if you don't download the key material, you won't have the key on your local machine.

    :::bash
    aws ec2 create-key-pair \
        --key-name KeyFooBar \
        --query 'KeyMaterial' \
        --output text \
        > KeyFooBar.pem
    chmod 400 KeyFooBar.pem

And that's it folks!

[1]: http://docs.aws.amazon.com/cli/latest/userguide/cli-ec2-keypairs.html "Using Key Pairs"
