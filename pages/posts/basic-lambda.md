title: Hello world with Lambda (Python 3.6)
slug: basic-lambda
date: 10 June 2017
sortdate: 20170610
teaser: Build a flask app with a button that triggers an AWS lambda function.
twitter: #

##Outline

This tutorial will walk through how to build a very simple web page that triggers a lambda function. The lambda function will return the string `'Hello from lambda'`. We will need to build the following components.

- AWS Lambda function
- AWS APIGateway API
- HTML form (w/ Flask Python 3.6)

Why Python 3.6? I needed an excuse to use the new [f-string][1] feature. The goal of this tutorial is not to walk through the UI in the AWS console. That has already [been][2] [done][3]. The goal here is to outline a basic setup for anyone who has never used AWS Lambda before. By the end of this tutorial you will know how each of these components fit together to create what I'm calling a lambda button. When you push the button, you get the text "Hello from lambda" printed on your screen.

---

##Components

We only have three components. I've only included the absolute bare minimum to make this work. From the user perspective, we start with a simple web page. It has a button that says 'Go!' on it. When you push the button, the text 'Hello from lambda' appears below the button.

###Flask HTML button

You can see all the code required for the Flask app in [a GitHub repo][4]. If you know how to `pip install` Flask and FlaskWTF you'll be able to run that code. Also make sure you're using Python 3.6.

The key logic of it is goes like this:

    :::python
    @app.route('/<value>', methods=('GET','POST'))
    def new(value):
        form = LambdaButton()
        if form.validate_on_submit():
            new_value = ping_lambda()
            return redirect(f'/{new_value}')  # AND THE CROWD GOES WILD!!
    return render_template('index.html', form=form, value=value)

You will notice that we have a `ping_lambda()` invocation there. That's where we call our lambda function. It looks like this:

    :::python
    import requests

    def ping_lambda():
        url = 'https://{api-id}.execute-api.{region-id}.amazonaws.com/{api-stage}/{api-resource}'
        response = requests.get(url)
        return response.text

The url is created by API Gateway.

###Lambda function

Next is the Lambda function. AWS provides very thorough tutorials on how to get started, so I'll leave their [UI documentation][2] to them. For this example you'll only need the absolute simplest code in your function.

    :::python
    def lambda_handler(event, context):
        return 'Hello from lambda'

That's it for the code. You really could use eithe Python 2.7 or 3.6 runtimes for this, it doesn't matter. My configuration is this.

- **Runtime**: Python 3.6
- **Handler**: lambda_function.lambda_handler
- **Role**: Choose an existing role
- **Existing role**: service-role/execute_my_lambda
- **Description**: says hello

I have no triggers, tags or monitoring.

###API Gateway

Why do we need this? Because Lambda only does code. It does not handle HTTP or web stuff by itself. Hence, we need to use the API Gateway service to expose the function so we can call the code whenever we want. Lambda experts will have a whole lot more to say on this matter.

Suffice it to say, in our example we only need two things:

* a Resource
* a `/GET` method

The resource is what API Gateway uses as a unit of work. A resource can be deployed, stopped etc. It can also have methods. A `/GET` method will create a way for the resource to point to our code in the Lambda function.

##Conclusion

When you click the button, the Flask app calls an AWS API. The API triggers the Lambda function, which returns the text 'Hello from lambda'. The API then delivers that text to the Flask app, which then displays it on your screen.

If something is unclear here, let me know on Twitter. I'm happy to explain in a bit more detail.

---

[1]: https://docs.python.org/3/reference/lexical_analysis.html#formatted-string-literals 'Python 3.6 f-strings'
[2]: http://docs.aws.amazon.com/lambda/latest/dg/get-started-create-function.html 'Create a hello world lambda function'
[3]: http://docs.aws.amazon.com/apigateway/latest/developerguide/create-api-resources-methods.html 'Create a simple API in API Gateway'
[4]: https://github.com/mehemken/lambda-button 'Flask lambda button'
