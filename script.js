const form=document.getElementById("chatForm");
const input=document.getElementById("messageInput");
const messages=document.getElementById("messages");
const clearButton=document.getElementById("clearChat");

function addMessage(text,type){
  const message=document.createElement("div");
  message.className=`message ${type}`;
  const avatar=document.createElement("div");
  avatar.className="avatar";
  avatar.textContent=type==="assistant"?"L":"Y";
  const bubble=document.createElement("div");
  bubble.className="bubble";
  bubble.textContent=text;
  message.append(avatar,bubble);
  messages.appendChild(message);
  messages.scrollTop=messages.scrollHeight;
}

function prototypeResponse(text){
  const lower=text.toLowerCase();
  if(lower.includes("hello")||lower.includes("hi")) return "Hello! Lumina-1 is still being built. This interface is the first step.";
  if(lower.includes("who are you")||lower.includes("what are you")) return "I'm Lumina-1, a project designed to explore how a language model can be built from the ground up.";
  if(lower.includes("milestone")) return "Milestone 1 is the foundation: HTML, CSS, JavaScript, Python, and Git.";
  return "I received your message. A real language model will replace this prototype response in a future milestone.";
}

form.addEventListener("submit",e=>{
  e.preventDefault();
  const text=input.value.trim();
  if(!text)return;
  addMessage(text,"user");
  input.value="";
  setTimeout(()=>addMessage(prototypeResponse(text),"assistant"),350);
});

clearButton.addEventListener("click",()=>{
  messages.innerHTML="";
  addMessage("Chat cleared. Lumina-1 is ready.","assistant");
});
