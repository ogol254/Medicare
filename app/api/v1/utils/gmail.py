import os
import smtplib


def sendmail(to, message):
    gmail_user = "abram.mcogol@gmail.com"
    gmail_password = os.getenv('GMAIL_PASSWORD')

    sent_from = gmail_user
    to = ['abraham.ogol@andela.com']
    subject = 'OMG Super Important Message'
    body = "{}\n\n- Medicare".format(message)

    email_text = """\  
	From: %s  
	To: %s  
	Subject: %s

	%s
	""" % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        return "Email sent!"
    except:
        return "Something went wrong..."
