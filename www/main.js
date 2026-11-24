// Eel Integration for Jarvis Desktop

eel.expose(hideLoader);
function hideLoader() {
    const el = document.getElementById('loader');
    if (el) el.classList.add('hidden');
    const fa = document.getElementById('faceAuth');
    if (fa) fa.classList.remove('hidden');
}

eel.expose(hideFaceAuth);
function hideFaceAuth() {
    const fa = document.getElementById('faceAuth');
    if (fa) fa.classList.add('hidden');
}

eel.expose(hideFaceAuthSuccess);
function hideFaceAuthSuccess() {
    const el = document.getElementById('faceAuthSuccess');
    if (el) {
        el.classList.remove('hidden');
        setTimeout(() => el.classList.add('hidden'), 3000);
    }
}

eel.expose(hideStart);
function hideStart() {
    const status = document.getElementById('sys-status');
    if (status) {
        status.innerText = "ONLINE (READY)";
        status.className = "status-online";
    }
}

eel.expose(DisplayMessage);
function DisplayMessage(text) {
    const el = document.getElementById('chatMessage');
    if (el) el.innerText = text;
}

eel.expose(receiverText);
function receiverText(text) {
    console.log("Jarvis speaking:", text);
}

eel.expose(ShowHood);
function ShowHood() {
    console.log("HUD ready");
}

function sendCommand() {
    const inp = document.getElementById('userInput');
    if (!inp || !inp.value.trim()) return;
    const cmd = inp.value.trim();
    DisplayMessage("Processing directive: " + cmd);
    inp.value = "";
    
    // Call Python backend if available
    try {
        if (typeof eel !== 'undefined' && eel.allCommands) {
            eel.allCommands(cmd);
        }
    } catch (e) {
        console.log("Eel call:", e);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById('userInput');
    if (input) {
        input.addEventListener("keypress", (e) => {
            if (e.key === "Enter") sendCommand();
        });
    }
    
    // Trigger init on load
    try {
        if (typeof eel !== 'undefined' && eel.init) {
            eel.init();
        }
    } catch (e) {
        console.log("Init:", e);
    }
});
