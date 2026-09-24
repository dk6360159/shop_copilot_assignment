

# Step 1
Open Docker Desktop

# Step 2
 cLone the github repo and opne in Vscode

 # step 3
 i have provided a file in mail from that file take gemini API key and put that key in .env.example file in last

 # Ste4

 In terminal 
 In Window run the command : docker compose up 

 # Step 5

 Open Postman 

 There are 4 endpoint to test

 # 1st endpoint Health Check

A get Query on :   http://0.0.0.0:8000/health

{{helping_screenshot\health_check.png}}
refer this image


# 2nd Endpont Inspect

Post Request 

url: http://0.0.0.0:8000 /inspect

{{helping_screenshot\inspect_endpoint.png}}

# 3rd Endpont Feedback

Post Request 

url: http://0.0.0.0:8000 /feedback

body: 
 {
      "transaction_id": "892de2d4-286e-4f63-9934-0cc610a8278e",
    "score": 0

}

{{helping_screenshot\feedback_endpoint.png}}

# 4th Endpont transactions details

Get Request 

url: http://0.0.0.0:8000 /transactions/{{transctionId}}

{{helping_screenshot\transaction_details.png}}

