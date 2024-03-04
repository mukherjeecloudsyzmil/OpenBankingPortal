from flask import Flask, render_template, request, redirect, url_for
import boto3
import requests

app = Flask(__name__)

# AWS SNS configurations
AWS_REGION = 'ap-south-1'
TOPIC_ARN = 'arn:aws:sns:ap-south-1:186930598879:demosns'
sns_client = boto3.client('sns', region_name=AWS_REGION)

@app.route('/')
def index():
    success_message = request.args.get('success_message', '')  # Retrieve success message from URL parameters
    response = requests.get('https://source.unsplash.com/random/800x600/?banking,finance')
    background_image_url = response.url
    return render_template('index.html', background_image_url=background_image_url, success_message=success_message)

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    country_code = request.form['country_code']
    phone = request.form['phone']
    message = request.form['message']

    # Format the phone number with country code
    formatted_phone = f"{country_code}{phone}"

    # Publish the message to the SNS topic
    sns_client.publish(
        TopicArn=TOPIC_ARN,
        Subject='New Message from Customer',
        Message=f'Email: {email}\nPhone: {formatted_phone}\nMessage: {message}'
    )

    success_message = "Thank you for reaching out! Our support team is on it, and we'll get back to you shortly."
    return redirect(url_for('index', success_message=success_message))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
