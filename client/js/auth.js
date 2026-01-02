const API = "http://127.0.0.1:8000";

function saveSession(data) {
  localStorage.setItem("token", data.token);
  localStorage.setItem("user_id", data.user_id);
  localStorage.setItem("role", data.role);
  localStorage.setItem("username", data.username || "");
  if (data.shop_name) localStorage.setItem("shop_name", data.shop_name);
  if (typeof data.balance === "number") localStorage.setItem("balance", data.balance);
}

async function login() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  const res = await fetch(`${API}/auth/login`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  if (data.error) {
    alert(data.error);
    return;
  }

  saveSession(data);

  // ✅ 登录后根据角色跳转
  if (data.role === "merchant") {
    location.href = "merchant/dashboard.html";
  } else if (data.role === "courier") {
    location.href = "courier/available.html";
  } else {
    location.href = "user/home.html";
  }
}

async function register() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const role = document.getElementById("role").value;
  const shop_name = document.getElementById("shop_name").value.trim();

  const res = await fetch(`${API}/auth/register`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ username, password, role, shop_name })
  });

  const data = await res.json();
  if (data.error) {
    alert(data.error);
    return;
  }

  alert("注册成功，请登录");
  location.href = "login.html";
}

function requireLogin(expectRole) {
  const uid = localStorage.getItem("user_id");
  const role = localStorage.getItem("role");
  if (!uid) {
    location.href = "../login.html";
    return null;
  }
  if (expectRole && role !== expectRole) {
    alert("权限不足，跳转到登录");
    location.href = "../login.html";
    return null;
  }
  return { uid: Number(uid), role };
}

async function refreshBalance() {
  const uid = localStorage.getItem("user_id");
  if (!uid) return;
  const res = await fetch(`${API}/user/${uid}/balance`);
  const data = await res.json();
  if (!data.error) {
    localStorage.setItem("balance", data.balance);
    const b = document.getElementById("balance");
    if (b) b.innerText = data.balance.toFixed(2);
  }
}
