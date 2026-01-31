import { S3Client, PutObjectCommand, DeleteObjectCommand, GetObjectCommand, ListObjectsV2Command, } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import dotenv from 'dotenv';
import { Hash } from "node:crypto";
dotenv.config();
const s3Client = new S3Client({ region: 'ap-south-1', credentials: { accessKeyId: process.env.access_key_id, secretAccessKey: process.env.secret_access_key } });
export async function getObject(fileName) {
    const command = new GetObjectCommand({
        Bucket: process.env.bucket_name,
        Key: fileName
    });
    const signedUrl = await getSignedUrl(s3Client, command, { expiresIn: 30 });
    console.log(signedUrl);
}
export async function putObject(fileName, cType) {
    const command = new PutObjectCommand({
        Bucket: process.env.bucket_name,
        ContentType: cType,
        Key: `user-uploads/${fileName}`
    });
    const signedUrl = await getSignedUrl(s3Client, command);
    console.log(signedUrl);
}
export async function listDir() {
    const command = new ListObjectsV2Command({
        Bucket: process.env.bucket_name
    });
    const files = await s3Client.send(command);
    console.log(files.Contents);
}
export async function deleteObject(fileName) {
    const command = new DeleteObjectCommand({
        Bucket: process.env.bucket_name,
        Key: fileName
    });
    await s3Client.send(command);
}
// getObject("user-uploads/test")
// putObject("test", "image/jpeg")
// listDir()
deleteObject("user-uploads/test");
//# sourceMappingURL=index.js.map