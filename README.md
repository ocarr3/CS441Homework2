# CS441 Homework 2 Submission by Omar Carrillo
Welcome to my submission for Homework 2. Below I will layout the files in my program and their uses. Video link for demo: https://youtu.be/EzrW624_ZPo


# Configuration Files application.conf (src/main/resources) in ScalaPB and ScalaRESTful
It also allows for the passing of parameters that change the task's behavior:
- port: The port that the server listens on (used for ScalaPB client server)
- address: The address that ther server opens on (used for ScalaPB client server)
- lambdaAPI: The URI for the API gateway for the respective lambda function 

Logger in logback.xml used for logging in both programs

# Utility Objects HW1Utils (src/main/scala/HW1Utils)
Adding configruation files and my own logger meant that I had to create objects for fetching them just like is already done for LogFileGenerator. I needed to create a logger, obtain the reference for the config files and have an object fetch the paramters for the program as requested. 

The logger creation and obtaining the config reference is very similar the biggest difference in these files is using HW1Params. This returns a whole new set of parameters. 
An example of using the input directory for task 1 is: HW1Params.inputPathTask1.

# MapReduceProgtamTask(1-4) (src/main/scala/HW1Utils)
Each of the four tasks from the asssignment has their own Scala class with a unique Mapper and Reducer job associated to the task's goal. With Sort being another Mapper set to take MapReduceProgramTask2's output and sort it. 

# mainRun (src/main/scala/mainRun)
The main Scala object that creates instances of the MapReduceProgram tasks and runs their Map and Reduce job with the use of the logger to confirm succesful job completions.

# Running the program in mainRun -> main
The function takes in two command line arguments: first one as the input directory for the tasks and the second as the output directory.
If you would run with sbt it would look like this: sbt "run inputDirectory outputDirectory" (quotes inclduded). An example using content root inside the program:
> sbt "run src/main/resources/input src/main/resources/output"

Editing the run configurations for Intellij allows you to add command line arguments allowing you to run the program this way as well

Before running:
The input directory should exist with a text file suitable for Hadoop MapReduce jobs to input and run such as .txt or .log files
Log file should be of the format of log files generated by LogFileGenerator or unexpected outputs could occur.

There should be no matching output directory to the output directory the user inputs or writes in HW1Configs.conf, this will cause the map and reduce jobs not to run.

# Tests (src/main/test/Generation/MRLogic.scala)
Tests for logic used inside of the mappers for the MapReduceProgramTasks can be found here, various string parsing and Date manipulation. 
