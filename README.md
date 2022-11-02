# CS441 Homework 2 Submission by Omar Carrillo
Welcome to my submission for Homework 2. Below I will layout the files in my program and their uses. Video link for demo: https://youtu.be/EzrW624_ZPo


# Configuration Files application.conf (src/main/resources) in ScalaPB and ScalaRESTful
It also allows for the passing of parameters that change the task's behavior:
- port: The port that the server listens on (used for ScalaPB client server)
- address: The address that ther server opens on (used for ScalaPB client server)
- lambdaAPI: The URI for the API gateway for the respective lambda function 

Logger in logback.xml used for logging in both programs

# Utility Objects HelperUtils (src/main/scala/HelperUtils)
Using the CreateLogger and ObtainConfig reference for grabbing configuarition values and logging program activities.

# ScalaPB gRPC Client Server (ScalaPB @ a457939) for checking if logs exist
Here I have the project for gRPC client server that uses ScalaPB and protobufs to communicate.
After cloning the project into Intellij everything should compile with no issue running 'sbt compile' after opening up the terminal.

(src/main/scala)

In this folder are the two main scala files relevant to running the project: lambdaQueryServer.scala and main.scala.
The client and server applications can be run in two different ways:

Method 1:
- Using two different terminals and sbt, by using the 'sbt run' command user is asked for to input the number option 1 or 2 after compiling. 1 being the option for the   server and 2 being the option for the client. 
- In the first terminal the user can just use 'sbt run' and select option 1 for the server to begin listening. Then in another terminal start the client with its         arguments. sbt will ask the user to start another server you can just enter y for yes. 
- An example of this would be sbt "run 17:00:00.000 01:00:00.000" and selecting option 2 this passes the time stamps to the client for it to send to the server the n   inside the server send the time stamps to the lambda function for it to check the interval 17:00:00.000 - 18:00:00.000. The return message from the log function can   be seen in a log messsage inside the terminal you invoked the client in.

Method 2: 
- When importing the project to Intellij a default run configuration should be created in lambdaQueryServer.scala at the beggining of the objects definition clicking on it will start the server inside the Run window.
- Then for the client to process is the same as above. Opening a terminal and running sbt "run (lower bound time stamp) (time stamp to add)" and selecting option 2 will run the client program and connect to the server if it is running. 

Some clarification for inputs and arguements just in case (relevent to both lambda function):
Both clients take in two arguments for their input when you run them, a simple way to write this in is sbt "run (lower time to begin at) (time to add to stop at)".
For example: sbt "run 05:30:00.000 00:30:00.000" will result in the lambda function searching with the interval 5:30:00.000 - 06:00:00.000.


# ScalaRESTful @ 4d0732c Scala client for sending RESTful requests to the lambda function
This a simple client that uses Requests to invoke the lambda function.

Running the program:

To run the program use the terminal window and sbt in this fashion: sbt "run (lower bound time stamp) (time stamp to add)" these two time stamps will be added to the payload in the lambda invocation and used for the binary search for the initial time stamp inside the files and searching log entries up to the end of the interval. The lambda function then hashes these srtings and adds them to an array for viewing inside the client.

# AWS Lambda Function lambda-time-bool-HelloWorldFunction-tb771VCpj6ps-199bd374-171c-4c75-bb63-c88664547bda (excuse the long name)
This is the lambda function that returns whether log files exist for the given interval inside the ScalaPB client and server porgram. Written in python it checks for 
the first and last entry of the logs to see if searching for logs with the other lambda function is even worth the effort. If the bool entry in its return is false the given interval is not an interval that exists within the boundaries of the logs within the S3 bucket.

# AWS Lambda function lambda-search-HelloWorldFunction-VGihJwpwtrGE-02134740-997f-4072-bf13-eb7bd3fba5aa
This lambda function searches the given time interval for log entries with a generated string that match the regex pattern. Also written in Python the function uses binary search to find the correct index for the starting interval within a created ordered hash table using the log entries ordered by datew. The generated strings of the log entries ares searched for a matching regex pattern. These string then are md5 hashed and grouped into an array and sent back in the function's return. Just as before it is important for the lambda function to have the correct permissions to access the S3 bucket.

S3_BUCKET and S3_PREFIX are two important variables that must be changed if one wanted to use the lambda function with another S3 bucket. Change the S3_BUCKET value to your buckets name and given the lambda function has the correct permissions to access the S3 bucket it should run. S3_PREFIX is a value one can use if they only want to work with files that start with a certain string in their name. For our purposes it was "Log" as all the log files began wit this and were the target files to be read in.

Also included are the .zip files for these lambda functions, with this one can upload to their own lambda functions and test them. Just ensure the functions have the proper access to S3 buckets.

Test configurations inside the AWS lambda code testing IDE look like this:
{
  "params": {
    "querystring": {
      "lower": "20:00:00.000",
      "upper": "01:00:00.000"
    }
  }
}


# Tests (src/test/scala/lambdaTimeIntervalPresentTests.scala) ScalaPB gRPC Client Server (ScalaPB @ a457939)
Tests for logic used inside of the lambda functions
# Resources
https://www.youtube.com/watch?v=DA3hlLxTl-8
https://scalapb.github.io/docs/grpc/
https://www.baeldung.com/scala/rest-with-requests-scala
https://www.gcptutorials.com/post/how-to-read-files-from-s3-using-python-aws-lambda
https://www.youtube.com/watch?v=uFsaiEhr1zs


