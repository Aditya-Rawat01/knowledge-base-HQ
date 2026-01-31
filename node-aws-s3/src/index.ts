import {
  S3Client,
  PutObjectCommand,
  DeleteObjectCommand,
  GetObjectCommand,
  ListObjectsV2Command,
} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

import dotenv from 'dotenv'
dotenv.config()
const s3Client = new S3Client({region: 'ap-south-1', credentials: {accessKeyId: process.env.access_key_id as string, secretAccessKey: process.env.secret_access_key as string} });


export async function getObject(fileName:string) {
    const command = new GetObjectCommand({
            Bucket: process.env.bucket_name as string,
            Key: fileName
        })
    
    const signedUrl = await getSignedUrl(s3Client, command, {expiresIn: 30})
    console.log(signedUrl)
}

export async function putObject(fileName:string,cType:string) {
    const command  = new PutObjectCommand({
            Bucket: process.env.bucket_name as string,
            ContentType: cType,
            Key: `user-uploads/${fileName}`
            
    })
    const signedUrl = await getSignedUrl(s3Client, command)
    console.log(signedUrl)
}

export async function listDir() {
    const command = new ListObjectsV2Command({
        Bucket: process.env.bucket_name as string
    })
    const files = await s3Client.send(command)
    console.log(files.Contents)

}

export async function deleteObject(fileName:string) {
    const command = new DeleteObjectCommand({
        Bucket: process.env.bucket_name as string,
        Key: fileName
    })

    await s3Client.send(command)
}
// getObject("user-uploads/test")
// putObject("test", "image/jpeg")
// listDir()
// deleteObject("user-uploads/test")