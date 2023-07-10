import dd_content
import datetime
import smtplib
from email.message import EmailMessage
from dd_content import get_keys_passwords


class DailyDigestEmail:

    def __init__(self):
        self.recipients_list = [{'email': '', 'city': '', 'country': ''}, ]  # recipient_data

        self.sender_credentials = {'outlook': '', 'password': get_keys_passwords('ps_outlook'),
                                   'gmail': '', 'passwrd': get_keys_passwords('ps_gmail'),
                                   'outlook_server': 'smtp.office365.com', 'gmail_server': 'smtp.gmail.com', }

    @staticmethod
    def create_content(recipient_data):
        content = {'quote': {'include': True if dd_content.get_quote() else False,
                             'content': dd_content.get_quote()},
                   'weather': {'include': True if dd_content.get_weather(recipient_data['city']) else False,
                               'content': dd_content.get_weather(recipient_data['city'])},
                   'twitter': {'include': True if dd_content.get_trends(recipient_data['city'],
                                                                        recipient_data['country']) else False,
                               'content': dd_content.get_trends(recipient_data['city'],
                                                                recipient_data['country'])},
                   'wikipedia': {'include': True if dd_content.get_article() else False,
                                 'content': dd_content.get_article()}, }
        return content

    def send_email(self, sender, password, serv, recipient_data):
        # build an email message
        msg = EmailMessage()
        msg['Subject'] = f'Daily Digest - {datetime.date.today().strftime("%d %b %Y")}'

        # Add plaintext and HTML content
        msg_body_text = self.format_message_text(recipient_data)
        msg_body_html = self.format_message_html(recipient_data)
        msg.set_content(msg_body_text)
        msg.add_alternative(msg_body_html, subtype='html')

        try:
            with smtplib.SMTP(serv, 587) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(msg, from_addr=sender, to_addrs=recipient_data['email'])
        except Exception as e:
            print(e)

    def handle_email_type(self):
        for record in self.recipients_list:
            if '@outlook' in record['email']:
                self.send_email(sender=self.sender_credentials['outlook'],
                                password=self.sender_credentials['password'],
                                serv=self.sender_credentials['outlook_server'],
                                recipient_data=record)
            elif '@gmail' in record['email']:
                print(record)
                self.send_email(sender=self.sender_credentials['gmail'],
                                password=self.sender_credentials['passwrd'],
                                serv=self.sender_credentials['gmail_server'],
                                recipient_data=record)

    @staticmethod
    def format_random_quote(content):
        text = '*~*~*  Quote of the Day  *~*~*\n\n'
        if content['quote']['include'] and content['quote']['content']:
            text += f'"{content["quote"]["content"]["quote"]}" - {content["quote"]["content"]["author"]}\n\n'
        return text

    @staticmethod
    def format_weather_forecast(content):
        text = ''
        if content['weather']['include']:
            text += f'*~*~*  Forecast for {content["weather"]["content"]["city"]}, ' \
                    f'{content["weather"]["content"]["country"]}\n'
            if content['weather']['include'] and content['weather']['content']:
                for forecast in content['weather']['content']['periods']:
                    text += f'{forecast["timestamp"].strftime("%d %b %H:%M")} - ' \
                            f'{forecast["temp"]}\u00B0C | {forecast["description"]}\n'
                text += '\n'
        return text

    @staticmethod
    def format_twitter_trends(content):
        text = ''
        if content['twitter']['include']:
            text += f'*~*~*  Top Ten Twitter Trends in {content["twitter"]["content"][1]}  *~*~*\n\n'
            if content['twitter']['include'] and content['twitter']['content']:
                text += f'*~*~*  Top Ten Twitter Trends in {content["twitter"]["content"][1]}  *~*~*\n\n'
                for trend in content['twitter']['content'][0][0:10]:
                    text += f'{trend["name"]}\n'
                text += '\n'
        return text

    @staticmethod
    def format_wikipedia_article(content):
        text = '*~*~*  Daily Random Learning  *~*~*\n\n'
        if content['wikipedia']['include'] and content['wikipedia']['content']:
            text += f'{content["wikipedia"]["content"]["title"]}\n<{content["wikipedia"]["content"]["url"]}>' \
                    f'\n{content["wikipedia"]["content"]["extract"]}'
        return text

    def format_message_text(self, recipient_data):
        # Generate Plaintext:
        content = self.create_content(recipient_data)
        text = f'*~*~*~*~*  Daily Digest - {datetime.date.today().strftime("%d %b %Y")}  *~*~*~*~*\n\n'
        text += self.format_random_quote(content)
        text += self.format_weather_forecast(content)
        text += self.format_twitter_trends(content)
        text += self.format_wikipedia_article(content)
        return text

# Generate HTML:    #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

    def format_message_html(self, recipient_data):
        content = self.create_content(recipient_data)
        html = f"""
<html>
    <body>
    <center>
        <h1>Daily Digest - {datetime.date.today().strftime("%d %b %Y")}</h1>"""
        html += self.format_random_quote_html(content)
        html += self.format_weather_forecast_html(content)
        html += self.format_twitter_trends_html(content)
        html += self.format_wikipedia_article_html(content)
        html += """
    </center>
    </body>
</html>"""
        return html

    @staticmethod
    def format_random_quote_html(content):
        html = ''
        if content['quote']['include'] and content['quote']['content']:
            html += f"""
            <h2>Quote of the Day</h2>
            <i>"{content["quote"]["content"]["quote"]}" - {content["quote"]["content"]["author"]}</i>"""
        return html

    @staticmethod
    def format_weather_forecast_html(content):
        html = ''
        if content['weather']['include'] and content['weather']['content']:
            html += f"""
            <h2>Forecast for {content["weather"]["content"]["city"]}, {content["weather"]["content"]["country"]}</h2>
            <table>"""
            for forecast in content['weather']['content']['periods']:
                html += f"""
            <tr>
                <td>
                    {forecast["timestamp"].strftime("%d %b %H:%M")}
                </td>
                <td>
                    <img src="{forecast["icon"]}.png">
                </td>
                <td>
                    {forecast["temp"]}{chr(176)}C | {forecast["description"]}
                </td>
            </tr>"""
            html += f"""</table>"""
        return html

    @staticmethod
    def format_twitter_trends_html(content):
        html = ''
        if content['twitter']['include'] and content['twitter']['content']:
            html += f"""
            <h2>Top Ten Twitter Trends in {content["twitter"]["content"][1]}</h2>"""
            for trend in content['twitter']['content'][0][0:10]:
                html += f"""
            <b><a href="{trend["url"]}">{trend["name"]}</a></b><p>"""
        return html

    @staticmethod
    def format_wikipedia_article_html(content):
        html = ''
        if content['wikipedia']['include'] and content['wikipedia']['content']:
            html += f"""
            <h2>Daily Random Learning</h2>
            <h3><a href="{content["wikipedia"]["content"]["url"]}">{content["wikipedia"]["content"]["title"]}</a></h3>
            <table width="800">
                <tr>
                    <td>{content["wikipedia"]["content"]["extract"]}</td>
                </tr>
            </table>"""
        return html


if __name__ == '__main__':
    '''email_ = DailyDigestEmail()
    data = email_.recipients_list[0]
    print(data)
    mt = email_.format_message_text(data)
    mh = email_.format_message_html(data)
    message = email_.format_message()

    print('Plaintext email body is ...')
    print(message['text'])
    print('\n' + '_' * 222 + '\n')
    print('HTML email body is ...')
    print(message['html'])

    with open('message_text.txt', 'w', encoding='UTF-8') as file:
        file.write(mt)'''
    '''
    with open('message_html.html', 'w', encoding='UTF-8') as file:
        file.write(mh)
    
   print('Sending test email...')
    email_.handle_email_type()
'''