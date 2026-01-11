# 🍔 Food Delivery Platform — 三端一体化智能点餐平台

**Food Delivery Platform** 是一个基于 **FastAPI + HTML/CSS/JavaScript** 的三端协同点餐系统，面向多角色业务场景，支持 **用户端（顾客）**、**商家端（餐厅）**、**配送员端（骑手）** 三方协作，实现从点单、备餐、配送到收货的完整闭环流程。  
系统采用 **模块化设计、分层结构、接口驱动开发模式**，具备良好的 **可维护性、可扩展性与用户体验**。

---

## 🏗️ 系统结构概览
```plaintext
FoodDeliveryPlatform/
│
├── .venv/                          # 虚拟环境目录（Python 依赖环境）
│
├── client/                         # 前端层（多端页面）
│   ├── courier/                    # 配送员端界面
│   │   ├── available.html          # 可接订单页面
│   │   └── myorders.html           # 我的订单页面
│   │
│   ├── css/                        # 全局样式目录
│   │   └── style.css               # 主样式文件
│   │
│   ├── js/                         # 各端逻辑脚本
│   │   ├── auth.js                 # 登录注册逻辑
│   │   ├── courier.js              # 配送员端逻辑
│   │   ├── merchant.js             # 商家端逻辑
│   │   └── user.js                 # 用户端逻辑
│   │
│   ├── merchant/                   # 商家端界面
│   │   ├── dashboard.html          # 商家后台首页
│   │   └── orders.html             # 订单管理页面
│   │
│   ├── user/                       # 用户端界面
│   │   ├── home.html               # 用户首页（推荐餐品）
│   │   ├── menu.html               # 菜单浏览页面
│   │   ├── orders.html             # 用户订单页面
│
├── login.html                      # 登录页
├── register.html                   # 注册页
│
├── server/                         # 后端层（FastAPI 服务端）
│   ├── pycache/                    # 缓存文件夹
│   │
│   ├── routers/                    # 路由层（接口模块）
│   │   ├── pycache/
│   │   ├── auth.py                 # 登录注册接口
│   │   ├── couriers.py             # 配送员端接口
│   │   ├── merchants.py            # 商家端接口
│   │   ├── orders.py               # 订单接口
│   │   └── users.py                # 用户端接口
│   │
│   ├── utils/                      # 工具层（辅助模块）
│   │   ├── pycache/
│   │   ├── auth.py                 # JWT、密码加密验证
│   ├── init.py
│   ├── database.py                 # 数据库连接配置
│   ├── main.py                     # FastAPI 启动入口
│   ├── models.py                   # ORM 模型定义
│   ├── schemas.py                  # Pydantic 数据校验模型
│
├── food_order.db                   # SQLite 数据库文件
├── requirements.txt                # Python 依赖列表

```

---

## ⚙️ 技术架构

| 模块 | 技术栈 |
|------|---------|
| 前端 | HTML5 / CSS3 / 原生 JavaScript |
| 后端 | FastAPI + Uvicorn |
| 数据层 | SQLite + SQLAlchemy |
| 鉴权机制 | JWT（JSON Web Token） |
| 密码安全 | passlib + bcrypt |
| API 文档 | FastAPI 自动生成 Swagger UI |
| 环境要求 | Python ≥ 3.10 |

系统采用 **RESTful API 架构**，通过前后端分离实现多端交互；  
所有接口均具备鉴权机制，确保 **数据安全与多角色隔离**。

---

## 🧩 三端核心功能

### 👤 用户端（User）
- 账号注册与登录验证  
- 浏览餐厅与菜品列表  
- 添加菜品至购物车并下单  
- 查看订单状态（待接单 → 制作中 → 配送中 → 已完成）  
- 实时余额更新与历史订单查询  

### 🏪 商家端（Merchant）
- 注册登录并填写店铺信息  
- 上架、修改、删除菜品（含图片链接与描述）  
- 查看待处理订单并标记“制作中”或“完成”  
- 订单收入结算与销售记录展示  

### 🚴 配送员端（Courier）
- 注册登录并接入配送系统  
- 查看所有可接订单  
- 接单后标记状态为“配送中”  
- 完成配送后标记为“已送达”  
- 查看个人接单记录与完成率  

---

## 🚀 本地运行指南

以下步骤适用于任何支持 Python 3.10+ 的系统，请按顺序执行以确保完整运行。

### 1️⃣ 克隆项目仓库

```bash
git clone https://github.com/Yerii10/FoodDeliveryPlatform.git
cd FoodDeliveryPlatform
```

### 2️⃣ 创建并激活虚拟环境

#### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ 安装项目依赖
```bash
pip install -r requirements.txt
```

如需使用国内源：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 4️⃣ 启动后端服务（FastAPI）
```bash
uvicorn server.main:app --reload
```

控制台输出如下即表示启动成功：
```
Uvicorn running on http://127.0.0.1:8000
```

访问自动生成的 API 文档：  
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 5️⃣ 启动前端服务（Live Server）

在 VS Code 中打开项目，定位到：
```
client/login.html
```

右键选择 **“Open with Live Server”**  
若未安装插件，可在 VS Code 扩展市场搜索安装。

默认端口通常为：
```
http://127.0.0.1:5500
```
（建议用三个不同的浏览器打开，分别表示用户端，商家端，配送端）

---

## 🔑 登录与业务流程演示

### ① 注册阶段
- 用户注册时选择「客户」  
- 商家注册时选择「商家」并填写店铺名  
- 配送员注册时选择「配送员」  

### ② 登录后自动跳转对应端口

| 角色 | 页面功能 |
|------|-----------|
| 用户端 | 浏览商家、下单、查看余额与订单状态 |
| 商家端 | 管理菜品、接单、标记完成 |
| 配送端 | 接单、配送、完成标记 |

### ③ 订单全流程
用户下单 → 商家接单 → 商家完成 → 配送员接单 → 配送完成 → 用户确认收货  

---

## 🧠 系统运行逻辑说明

### 🖥 前端层（client）
负责多角色页面展示与交互逻辑，  
所有数据通过 `fetch()` 与后端通信，界面独立互不干扰。

### ⚙️ 后端层（server）
由 **FastAPI** 提供服务，所有路由模块化管理，  
使用 **SQLAlchemy** 进行 ORM 数据操作。

### 💾 数据层（database + models）
默认使用 **SQLite**，可轻松切换至 **MySQL / PostgreSQL**。  
核心表结构包括：用户表、菜品表、订单表等。

---

## 🌟 项目特性总结

- 🧩 **三端融合架构**：用户、商家、配送端统一系统中协作  
- 🧱 **模块化后端结构**：路由、数据库、模型层清晰分离  
- 📘 **接口即文档**：FastAPI 自动生成 Swagger 文档  
- 📱 **多设备访问**：支持电脑与移动端浏览器  
- 🔄 **全流程状态追踪**：订单从下单到送达全程状态可视化  
