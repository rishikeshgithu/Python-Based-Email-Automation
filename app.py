import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def get_user_input(prompt):
    return input(prompt).strip()

def send_email(sender_email, sender_password, receiver_email, subject, body, attachment_path):
    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Attach the file
    with open(attachment_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment_path)}')
        message.attach(part)

    # Connect to the SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

if __name__ == "__main__":
    # Get user input
    sender_email = get_user_input("Enter your Gmail address: ")
    sender_password = get_user_input("Enter your Gmail password: ")
    receiver_email = get_user_input("Enter the recipient's email address: ")

    # Specify the folder path where your files are stored
    folder_path = "/path/to/your/folder"

    # Get a list of files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    for file in files:
        file_path = os.path.join(folder_path, file)
        subject = f"Attachment: {file}"
        body = "Please find the attached file."

        # Send the email
        send_email(sender_email, sender_password, receiver_email, subject, body, file_path)

    print("Emails sent successfully!")
