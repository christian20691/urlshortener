
# Welcome to your CDK Python project!

## URL Shortener CDK APP 

### Single stack application resources

**Lambdas:**.   
> - getshorturl. 
> - admin.   

**DynamoDB:**  
> - url-shortener table. 

**API Gateway**:  
> - /admin POST resource
> - /getshorturl POST resource 

### APIGW Test

**Admin**

  JSON Body : `{"url":"https://longurl.com/asd","shorturl":"https://lng.com"}`

**Getshorturl**

  JSON Body : `{"S": "https://longurl.com/asd"}`
