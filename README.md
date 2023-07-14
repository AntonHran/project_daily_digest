Daily Digest
Functional possibilities of the application:
- generate a random inspirational quote;
- retrieve current weather forecast for specified location;
- retrieve current Twitter trends;
- retrieve a random Wikipedia article;
- format contant into an email;
- send the email to specified recipients.

The application enables the admin to:
- configure which content sources to include in the email;
- add recipients;
- remove recipients;
- schedule recurring daily time to send emails;
- configure sender credentials.

To install the application you should use poetry.lock file to set your envirement ad install all required packages

If you would like to install and try to use this app you should know about specific requirements:
- you should have your own api keys for weather and Twitter parts of a program as I did not input my own;
- to send outlook emails you should enter your outlook email address and a password of your email in the fields sender credentials;
- to send gmail emails you should enter your gmail email address and a special code which you are get after activation of the two-step verification for your gmail emailaddress;
- an .exe file of the whole program will be added in a separete fork.

License: None

This project bases on one of the LinkedIn Learning projects with some changes that were added by me: 
- ability to send the Gmail emails;
- additional information about recipients locations to send different wweather forecast and Twitter trends (according to ther locations);
- parsers for getting information about recipients.

From time to time I comeback to this project to add some new content or improve the existence one but not always push that change(-s) to this repository...
