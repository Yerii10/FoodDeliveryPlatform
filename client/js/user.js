// client/js/user.js
const userId = localStorage.getItem("user_id");
const apiBase = "http://127.0.0.1:8000";

async function loadOrders() {
  try {
    const res = await fetch(`${apiBase}/order/user/${userId}`);
    const data = await res.json();
    console.log("订单数据:", data); // 调试输出
    renderOrders(data);
  } catch (err) {
    console.error("加载订单失败:", err);
  }
}

function renderOrders(orders) {
  const container = document.getElementById("orders");
  container.innerHTML = "";

  if (!orders || orders.length === 0) {
    container.innerHTML = "<p>暂无订单</p>";
    return;
  }

  orders.forEach(o => {
    const orderDiv = document.createElement("div");
    orderDiv.classList.add("order-card");

    // 拼接菜品详情
    const itemsHtml = o.items
      .map(i => `${i.name} × ${i.quantity}（￥${i.price}）`)
      .join("<br>");

    // 商家名称显示
    const merchantName = o.merchant_name ? o.merchant_name : "未命名商家";

    orderDiv.innerHTML = `
      <div class="order-header">
        <strong>订单号：</strong>${o.order_no}<br>
        <strong>商家：</strong>${merchantName}<br>
      </div>
      <div class="order-body">
        <p>${itemsHtml}</p>
        <p><strong>总价：</strong>￥${o.total_price.toFixed(2)}</p>
        <p><strong>状态：</strong>${o.status === "done" ? "✅ 已完成" : "⌛ 进行中"}</p>
      </div>
      <hr>
    `;
    container.appendChild(orderDiv);
  });
}

// 页面加载时执行
window.addEventListener("DOMContentLoaded", loadOrders);
