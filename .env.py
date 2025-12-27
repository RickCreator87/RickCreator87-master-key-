`env
PORT=3000           # or 8000 for Python

GITHUBAPPID=2498944
GITHUBPRIVATEKEY_BASE64=<<your base64-encoded private key here>>
GITHUBWEBHOOKSECRET=<<the webhook secret from the GitHub App>>

GITHUBCLIENTID=lv23il5SuXs68dmGM3jK
GITHUBCLIENTSECRET=<<if you generated one>>

DEEPSEEKAPIKEY=<<if using>>
OPENAIAPIKEY=<<if using>>
OLLAMA_HOST=http://localhost:11434
`

If you don’t have GITHUBPRIVATEKEY_BASE64 yet:

1. Take the .pem private key file you downloaded from GitHub  
2. Base64 encode it:

- Node (on your machine):

  `bash
  base64 -w0 path/to/private-key.pem
  `

- macOS:

  `bash
  base64 path/to/private-key.pem | tr -d '\n'
