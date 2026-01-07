// js/courier.js
// 外卖员端通用逻辑：加载可接订单 / 我的配送订单

// === 加载可接订单 ===
async function loadAvailableOrders() {
  const res = await fetch(`${API}/courier/available`);
  const data = await res.json();
  const box = document.getElementById("orders");
  box.innerHTML = "";

  if (!data || data.length === 0) {
    box.innerHTML = "<p>暂无可接订单</p>";
    return;
  }

  data.forEach(o => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h3>订单号：${o.order_no}</h3>
      <div class="mt">商家：${o.merchant}</div>
      <div class="mt">金额：￥${o.total_price.toFixed(2)}</div>
      <div class="mt right">
        <button data-no="${o.order_no}" class="accept-btn">接单</button>
      </div>
    `;
    box.appendChild(card);
  });

  // 接单事件绑定
  document.querySelectorAll(".accept-btn").forEach(btn => {
    btn.onclick = async () => {
      const courierId = localStorage.getItem("user_id");
      const no = btn.dataset.no;

      const res = await fetch(`${API}/courier/accept/${no}/${courierId}`, {
        method: "PUT"
      });
      const data = await res.json();

      if (data.error) {
        alert(data.error);
      } else {
        alert("接单成功！");
        await loadAvailableOrders();
      }
    };
  });
}

// === 加载我的配送订单 ===
async function loadMyOrders() {
  const courierId = localStorage.getItem("user_id");
  const res = await fetch(`${API}/courier/my/${courierId}`);
  const data = await res.json();
  const box = document.getElementById("orders");
  box.innerHTML = "";

  if (!data || data.length === 0) {
    box.innerHTML = "<p>暂无配送订单</p>";
    return;
  }

  data.forEach(o => {
    const card = document.createElement("div");
    card.className = "card";

    const statusText =
      o.status === "done" ? "已完成" :
      o.status === "delivering" ? "配送中" : o.status;

    card.innerHTML = `
      <div class="flex" style="justify-content:space-between;">
        <h3>订单号：${o.order_no}</h3>
        <span class="badge">${statusText}</span>
      </div>
      <div class="mt">商家：${o.merchant}</div>
      <div class="mt">金额：￥${o.total_price.toFixed(2)}</div>
      <div class="mt right ${(o.status === 'done') ? 'hide' : ''}">
        <button data-no="${o.order_no}" class="deliver-btn">标记送达</button>
      </div>
    `;
    box.appendChild(card);
  });

  // 标记送达事件绑定
  document.querySelectorAll(".deliver-btn").forEach(btn => {
    btn.onclick = async () => {
      const no = btn.dataset.no;
      const res = await fetch(`${API}/courier/deliver/${no}`, { method: "PUT" });
      const data = await res.json();
      if (data.error) {
        alert(data.error);
      } else {
        alert("已标记送达！");
        await loadMyOrders();
      }
    };
  });
}
