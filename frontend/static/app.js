// Beginner-friendly front-end script:
// - Uses fetch() to call backend API endpoints
// - Stores a very simple "session token" in localStorage (learning mode)

function setMessage(el, text, isOk) {
  if (!el) return;
  el.textContent = text || "";
  el.classList.remove("ok", "err");
  if (text) el.classList.add(isOk ? "ok" : "err");
}

function getToken() {
  return localStorage.getItem("bank_token") || "";
}

function setToken(token) {
  localStorage.setItem("bank_token", token);
}

function clearToken() {
  localStorage.removeItem("bank_token");
}

async function api(path, options = {}) {
  const headers = options.headers || {};
  headers["Content-Type"] = "application/json";

  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(path, { ...options, headers });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = data.error || `Request failed (${res.status})`;
    const error = new Error(msg);
    error.status = res.status; // Attach status code to error
    throw error;
  }
  return data;
}

function onLoginPage() {
  const form = document.getElementById("loginForm");
  const msg = document.getElementById("message");
  if (!form) return false;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    setMessage(msg, "", true);
    const formData = new FormData(form);
    const payload = {
      username: formData.get("username"),
      password: formData.get("password"),
    };

    try {
      const data = await api("/api/login", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setToken(data.token);
      window.location.href = "/app/dashboard";
    } catch (err) {
      setMessage(msg, err.message, false);
    }
  });

  return true;
}

function onRegisterPage() {
  const form = document.getElementById("registerForm");
  const msg = document.getElementById("message");
  if (!form) return false;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    setMessage(msg, "", true);

    const formData = new FormData(form);
    const payload = {
      username: formData.get("username"),
      password: formData.get("password"),
      account_type: formData.get("account_type"),
    };

    try {
      await api("/api/register", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setMessage(msg, "Account created. You can login now.", true);
      setTimeout(() => (window.location.href = "/app/login"), 700);
    } catch (err) {
      setMessage(msg, err.message, false);
    }
  });

  return true;
}

function onDashboardPage() {
  const welcomeText = document.getElementById("welcomeText");
  const accountType = document.getElementById("accountType");
  const balance = document.getElementById("balance");

  const refreshBtn = document.getElementById("refreshBtn");
  const logoutBtn = document.getElementById("logoutBtn");

  const depositForm = document.getElementById("depositForm");
  const withdrawForm = document.getElementById("withdrawForm");
  const depositMessage = document.getElementById("depositMessage");
  const withdrawMessage = document.getElementById("withdrawMessage");

  const loadTxBtn = document.getElementById("loadTxBtn");
  const txMessage = document.getElementById("txMessage");
  const txTableBody = document.getElementById("txTableBody");

  if (!welcomeText) return false;

  async function loadSummary() {
    setMessage(txMessage, "", true);
    try {
      const data = await api("/api/me", { method: "GET" });
      welcomeText.textContent = `Welcome, ${data.username}`;
      accountType.textContent = data.account_type;
      balance.textContent = `${data.balance}`;
    } catch (err) {
      // Only logout on authentication errors (401), not other errors
      if (err.status === 401) {
        clearToken();
        window.location.href = "/app/login";
      } else {
        // For other errors, just show the message but don't logout
        setMessage(txMessage, `Error loading account: ${err.message}`, false);
        console.error('Error loading summary:', err);
      }
    }
  }

  logoutBtn?.addEventListener("click", () => {
    clearToken();
    window.location.href = "/app/login";
  });

  refreshBtn?.addEventListener("click", loadSummary);

  depositForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    setMessage(depositMessage, "", true);
    const amount = Number(new FormData(depositForm).get("amount"));

    try {
      const data = await api("/api/deposit", {
        method: "POST",
        body: JSON.stringify({ amount }),
      });
      setMessage(depositMessage, `Deposit successful. New balance: ${data.balance}`, true);
      await loadSummary();
    } catch (err) {
      setMessage(depositMessage, err.message, false);
    }
  });

  withdrawForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    setMessage(withdrawMessage, "", true);
    const amount = Number(new FormData(withdrawForm).get("amount"));

    try {
      const data = await api("/api/withdraw", {
        method: "POST",
        body: JSON.stringify({ amount }),
      });
      setMessage(withdrawMessage, `Withdraw successful. New balance: ${data.balance}`, true);
      await loadSummary();
    } catch (err) {
      setMessage(withdrawMessage, err.message, false);
    }
  });

  loadTxBtn?.addEventListener("click", async () => {
    setMessage(txMessage, "", true);
    txTableBody.innerHTML = "";

    try {
      const data = await api("/api/transactions", { method: "GET" });
      const items = data.transactions || [];

      if (items.length === 0) {
        setMessage(txMessage, "No transactions yet.", true);
        return;
      }

      for (const tx of items) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${tx.timestamp}</td>
          <td>${tx.type}</td>
          <td>${tx.amount}</td>
          <td>${tx.note || ""}</td>
        `;
        txTableBody.appendChild(tr);
      }
    } catch (err) {
      setMessage(txMessage, err.message, false);
    }
  });

  loadSummary();
  return true;
}

// Password visibility toggle (works on both login and register pages)
function initPasswordToggle() {
  const passwordInput = document.getElementById("passwordInput");
  const passwordToggle = document.getElementById("passwordToggle");
  
  if (passwordInput && passwordToggle) {
    passwordToggle.addEventListener("click", () => {
      const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
      passwordInput.setAttribute("type", type);
      
      // Update eye icon (simple toggle)
      const eyeIcon = passwordToggle.querySelector(".eye-icon");
      if (eyeIcon) {
        eyeIcon.textContent = type === "password" ? "👁️" : "👁️‍🗨️";
      }
    });
  }
}

// Initialize password toggle
initPasswordToggle();

// Detect which page we are on:
onLoginPage() || onRegisterPage() || onDashboardPage();

