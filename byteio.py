import io
import zipfile
import boto3

def upload_zip_to_s3(byte_string, bucket_name, object_name):
    # Create an in-memory buffer
    in_memory_zip = io.BytesIO()

    # Create a new ZIP file in the in-memory buffer
    with zipfile.ZipFile(in_memory_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Write the byte string as a file inside the ZIP
        zf.writestr("file_inside_zip.txt", byte_string)

    # Seek to the beginning of the in-memory buffer
    in_memory_zip.seek(0)

    # Create an S3 client
    s3_client = boto3.client('s3')

    # Upload the ZIP file to the specified S3 bucket
    s3_client.upload_fileobj(in_memory_zip, bucket_name, object_name)

# Example usage
byte_string = b"Hello, this is a byte string to be zipped."
bucket_name = 'your-s3-bucket-name'
object_name = 'your-zip-file.zip'

upload_zip_to_s3(byte_string, bucket_name, object_name)
