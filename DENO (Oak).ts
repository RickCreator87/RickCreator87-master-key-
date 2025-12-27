import { Application, Router } from "https://deno.land/x/oak/mod.ts";
import { createHmac } from "https://deno.land/std/hash/mod.ts";

function verifySignature(secret, payload, signature) {
  const hmac = createHmac("sha256", secret);
  hmac.update(payload);
  const digest = "sha256=" + hmac.toString();
  return digest === signature;
}

const router = new Router();

router.post("/github/webhook", async (ctx) => {
  const body = await ctx.request.body({ type: "text" }).value;
  const signature = ctx.request.headers.get("x-hub-signature-256");
  const event = ctx.request.headers.get("x-github-event");
  const secret = Deno.env.get("GITHUBWEBHOOKSECRET");

  if (!verifySignature(secret, body, signature)) {
    ctx.response.status = 401;
    return;
  }

  ctx.response.body = "OK";
});

const app = new Application();
app.use(router.routes());
app.listen({ port: 3000 });
