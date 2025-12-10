export default {
  async fetch(request) {
    // Target Backend URL (Python Bot Webhook Endpoint)
    const pythonBotUrl = "https://my-python-bot.onrender.com/webhook";

    // 转发原始请求 (Request Forwarding / Reverse Proxy)
    const newRequest = new Request(pythonBotUrl, {
      method: request.method,
      headers: request.headers,
      body: request.body
    });

    // 发送到 Python 服务器 (Forward to Backend)
    const response = await fetch(newRequest);

    // 将响应返回给 Telegram (Return Response to Telegram)
    return new Response(await response.text(), {
      status: response.status,
      headers: response.headers
    });
  }
};
