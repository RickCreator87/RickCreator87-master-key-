
`bash
ngrok http 3000   # Node
ngrok http 8000   # Python
`

Ngrok will give you a URL like:

`text
https://randomstring.ngrok.io
`

Set your GitHub App’s Webhook URL to:

`text
https://randomstring.ngrok.io/github/webhook
