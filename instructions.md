1. Empty requests.txt. Run get request URLS, set the root value to whatever the previous degree was
2. Set degree correctly inside main.py, create file called {timecontrol}-{degree}.txt
3. Run again changing IS_FAILURES = True, to redo failed requests

TODO:

Create folders numbered 1, 2, 3 ect depending on what degree it is.
No files should be overriden, there should be one parameter to switch which degree
The script should read from the previous csv to get root players
When computing failures we should load from existing file as a set, so we don't get dupilcates
Make csv pipe seperated

Check AWS console for pricing



IMPORTANT:

increase concurrency to possibly 1000

remove the fair play check from within the lambda function - move it to the main.py
That way we can store a list of fair play abusers and accumulate it to save on requests and especially cloud function time - although will this be too slow without paralysation

write test file to randomly check elements and check if they have actually one that game