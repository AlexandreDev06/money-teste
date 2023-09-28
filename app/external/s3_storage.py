import boto3

from app.configs.settings import settings


class RemoteStorage:
    async def __aws_instance(self):
        return boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

    # Save the file in the storage
    async def save_base64(self, file_data: str, file_name: str):
        """Save the file in the S3 bucket"""
        s3_client = await self.__aws_instance()
        bucket = settings.aws_bucket_name

        try:
            s3_client.put_object(
                Bucket=bucket, Key=file_name, Body=file_data, ContentType="image/jpeg"
            )
        except Exception as exe:
            print(exe)
            return False

        return f"https://{bucket}.s3.amazonaws.com/{file_name}"

    async def generate_s3_presigned_link(
        self,
        file_name: str,
        expire_in_minutes: int = 60,
        content_type_header: str = "application/octet-stream",
    ):
        """Generate a presigned temporary S3 bucket link"""
        s3_client = await self.__aws_instance()

        try:
            link = s3_client.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": settings.aws_bucket_name,
                    "Key": file_name,
                    "ResponseContentType": content_type_header,
                },
                ExpiresIn=expire_in_minutes * 60,
            )
            return link
        except Exception as exe:
            print(exe)
            return None
