Daily Digest
Functional possibilities of the application:
- generate a random inspirational quote;
- retrieve current weather forecast for specified location;
- retrieve current Twitter trends;
- retrieve a random Wikipedia article;
- format content into an email;
- send the email to specified recipients.

The application enables the admin to:
- configure which content sources to include in the email;
- add recipients;
- remove recipients;
- schedule recurring daily time to send emails;
- configure sender credentials.

To install the application, you should use poetry.lock file to set your environment and install all required packages

If you would like to install and try to use this app, you should know about specific requirements:
- you should have your own api keys for weather and Twitter parts of a program as I did not input my own;
- to send Outlook emails, you should enter your Outlook email address and a password of your email in the fields sender credentials;
- to send gmail emails, you should enter your gmail email address and a special code which you are getting after activation of the two-step verification for your gmail email address;
- an .exe file of the whole program will be added in a separate fork.

License: None

This project bases on one of the LinkedIn Learning projects with some changes that I added: 
- ability to send the Gmail emails;
- additional information about recipient locations to send different weather forecast and Twitter trends (according to their locations);
- parsers for getting information about recipients;
- another function to form quotes.

Future Enhancements

- **Timezone Support:** Add the ability to handle different timezones for sending emails to users worldwide. This feature will ensure that emails are delivered at the appropriate local time for each recipient.

- **Group Emailing:** Implement the option to create separate groups of users with similar email preferences, such as delivery time, motivational quotes, weather updates, etc.

- **User Interface:** Develop a graphical user interface (GUI) using a library like Tkinter to provide a more user-friendly and intuitive experience. The GUI can include forms for settings configuration, contact list display, and digest preview.

- **Expanded Content:** Consider adding additional content blocks to the daily digest, such as news headlines, quotes of the day, photos, tips, etc. Utilize popular APIs to fetch real-time data for each content block.
