package main

import (
    "crypto/hmac"
    "crypto/sha256"
    "encoding/hex"
    "io/ioutil"
    "net/http"
    "os"
)

func verifySignature(secret, payload, signature string) bool {
    mac := hmac.New(sha256.New, []byte(secret))
    mac.Write([]byte(payload))
    expected := "sha256=" + hex.EncodeToString(mac.Sum(nil))
    return hmac.Equal([]byte(expected), []byte(signature))
}

func webhook(w http.ResponseWriter, r *http.Request) {
    signature := r.Header.Get("X-Hub-Signature-256")
    event := r.Header.Get("X-GitHub-Event")
    secret := os.Getenv("GITHUBWEBHOOKSECRET")

    body, _ := ioutil.ReadAll(r.Body)

    if !verifySignature(secret, string(body), signature) {
        w.WriteHeader(401)
        return
    }

    switch event {
    case "pull_request":
        w.Write([]byte("PR logic"))
    default:
        w.Write([]byte("OK"))
    }
}

func main() {
    http.HandleFunc("/github/webhook", webhook)
    http.ListenAndServe(":3000", nil)
}
