from flask import Flask, render_template, request, redirect, url_for
import boto3, os

app = Flask(__name__)

S3_BUCKET = "your-bucket-name"
S3_REGION = "ap-south-1"

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=S3_REGION
)

@app.route('/')
def index():
    files = s3.list_objects_v2(Bucket=S3_BUCKET).get('Contents', [])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        s3.upload_fileobj(file, S3_BUCKET, file.filename)
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    url = s3.generate_presigned_url('get_object',
                                    Params={'Bucket': S3_BUCKET, 'Key': filename},
                                    ExpiresIn=300)
    return redirect(url)

if __name__ == '__main__':
    app.run(debug=True)


