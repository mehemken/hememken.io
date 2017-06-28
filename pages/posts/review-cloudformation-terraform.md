title: Review of CloudFormation and Terraform
slug: review-cloudformation-terraform
date: 20 June 2017
sortdate: 20170620
teaser: In the context of building a sandbox infrastructure for learning Ansible.
twitter: https://twitter.com/mehemken/status/877258370981412868

# Article: Review

I used CloudFormation and Terraform to create a sandbox environment for learning Ansible. At the time of this writing I am learning both tools, so it is not an expert opinion. I have used CloudFormation in production, but not Terraform.

CloudFormation is a service that helps you model and set up your AWS resources so that you can spend less time managing those resources and more time focusing on you applications. Terraform is a tool for building, changing, and versioning infrastructure safely and efficiently. Both tools use configuration files to describe components required by your infrastructure.

## Pictures

I enjoyed using both tools. I found it very useful that CloudFormation templates can be used to generate a descriptive diagram of your infrastructure. Working with a client or manager, they will inevitably ask "is it done yet?" and you can show them a diagram to show your progress. No such tool exists for Terraform.

[CloudFormation diagram][2] << Picture!

That image was generated with a tool in the AWS management console. It is free and easy to use. It accepts both JSON and YAML format config files. You can even use it to turn a JSON config into YAML and vice versa. 

Terraform has a `graph` command ([docs][3]) which also generates an image (with the help of the 3rd party [graphviz tool][7]). However, the purpose of that is not to show a visual description of your infrastructure. It is generates a visual representation of an execution plan. You wouldn't show it to a client. It is ugly.

[Terraform diagram][4] << Picture!

## Template language

CloudFormation templates are written in JSON or YAML. JSON would make it easy to generate a template with a script. YAML is very human writeable. Terraform can be written in JSON and a custom templating language called HCL. HashiCorp recommends you use HCL. You cannot write a Terraform template in YAML unfortunately.

## Flow control

The really nice thing about Terraform is that you have features that approximate flow control. You don't exactly have a for loop or if statements, but really you do. You have the "meta-parameter" `count`. For more on this check out the [excelent post][5] by Yevgeniy Brikman. This means that a Terraform template will be [DRY][6].

## Examples

> [CloudFormation example][8]  
> [Terraform example][9]

I've taken the time to write a sandbox infrastructure in both CloudFomration YAML and Terraform HCL. It describes an internet connected VPC with a public subnet. In the subnet we have some ubuntu/redhat/windows servers. The Terraform template is 113 lines and the CloudFormation template is 186 lines.

This is a tiny project and the difference in length of the templates is already really noticable. Not to mention, the HCL is full of lines that have a single curly brace. YAML is very dense. Furthermore, the CloudFormation template only describes five servers. The HCL allows me to change a single number to describe as many servers as I want. Not only that, I've configured it so that I'll always have an equal proportion of ubuntu/redhat/windows servers (given the number of servers is a multiple of three). I don't need to change the output configuration or anything.

## Conclusion

Both tools are great. I'd rather use these than manually click through the console UI. It is a very nice UI and sometimes I do fall back for little things. But when designing and creating infrastructure, this is the way to go. I really wish though, that CloudFormation had flow control. And I wish Terraform had a nice visualization tool.

The CloudFormation problem can be fixed by frameworks such as [troposphere][10] and [cloudformation-ruby-dsl][11]. (I have not vetted those tools, it's just a google search). They don't look like they've fully matured but I'm just guessing.

Hopefully there are tools to visualize Terraform templates. Cloudcraft has it on its radar, but nothing shows they're actually working on it. It is in their [roadmap][12]. If they implement this it would be really good for Terraform. Cloudcraft diagrams are even better than the CloudFormation ones. They are marketing collateral qualitiy pictures.

These are both young tools and they will be improving a lot I'm sure.

[1]: https://www.terraform.io/downloads.html
[2]: /static/images/articles/review-cloudformation-terraform/cf-diagram.png "Pretty picture"
[3]: https://www.terraform.io/docs/commands/graph.html "Command: graph"
[4]: /static/images/articles/review-cloudformation-terraform/tf-diagram.png "Ugly picture"
[5]: https://blog.gruntwork.io/terraform-tips-tricks-loops-if-statements-and-gotchas-f739bbae55f9 "And this is why Terraform is awesome"
[6]: https://en.wikipedia.org/wiki/Don%27t_repeat_yourself "Don't repeat yourself."
[7]: http://www.graphviz.org/ "Graph visualization software"
[8]: https://github.com/mehemken/article-cloudformation-terraform/blob/master/cf-template.yaml "CloudFormation example"
[9]: https://github.com/mehemken/article-cloudformation-terraform/blob/master/tf-template.tf "Terraform example"
[10]: https://github.com/cloudtools/troposphere "troposphere"
[11]: https://github.com/bazaarvoice/cloudformation-ruby-dsl "cloudformation-ruby-dsl"
[12]: https://trello.com/c/rsDCPHDz/65-add-export-import-from-terraform-template "Cloudcraft roadmap"
