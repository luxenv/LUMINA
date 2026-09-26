const form = document.getElementById("form"), input = document.getElementById("input"), chat = document.getElementById("chat");
let sessionId = localStorage.getItem("lumina_session") || Date.now().toString();
localStorage.setItem("lumina_session", sessionId);

function add(text, cls) {
  const div = document.createElement("div");
  div.className = "msg " + cls;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

form.addEventListener("submit", async e => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  add("You: " + message, "user");
  input.value = "";
  const pending = add("Lumina-1 is thinking...", "ai");
  try {
    const r = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: message,
        session_id: sessionId,
        use_tools: true
      })
    });
    const data = await r.json();
    pending.textContent = "Lumina-1: " + (data.reply || data.error || "No response");
  } catch (err) {
    pending.textContent = "Connection error: " + err;
  }
});
