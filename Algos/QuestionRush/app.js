// 初始化数据
let problems = [];
let points = 0;
let shopItems = [];

// 初始化加载
window.onload = () => {
    loadShopItems();
    loadFromLocalStorage();
};

// 加载商品数据
// 修改加载逻辑防止清空后数据丢失
function loadShopItems() {
    // 只有首次加载或清空后才会读取JSON
    if (shopItems.length === 0) {
      fetch('shop-items.json')
        .then(response => response.json())
        .then(data => {
          shopItems = data.map(item => ({
            ...item,
            redeemedCount: 0 // 强制重置兑换次数
          }));
          renderShop();
        });
    }
  }

// 文件读取
document.getElementById('csvFile').addEventListener('change', function(e) {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        // 在问题数据中添加收藏状态字段
        problems = parseCSV(e.target.result).map((p, idx) => ({
        id: idx,
        ...p,
        status: "未通过",
        color: "",
        favorite: false, // 新增收藏状态
        lastSolved: null
        }));
        saveToLocalStorage();
        renderTable(problems);
    };
    reader.readAsText(file);
});

// CSV解析
function parseCSV(csv) {
    return csv.split('\n').slice(1).map(row => {
        const [link, name, difficulty, type] = row.split(',');
        return {
            link: link?.trim() || '',
            name: name?.trim() || '未知题目',
            difficulty: parseInt(difficulty?.trim()) || 0,
            type: type?.trim() || '未分类'
        };
    }).filter(p => p.link);
}

// 新增当前显示数据引用
let currentDisplayData = [];

// 修正renderTable函数
function renderTable(data) {
    currentDisplayData = data; // 维护当前显示数据
    const showType = !document.getElementById('toggleType').classList.contains('active');
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = data.map(problem => `
        <tr data-id="${problem.id}" style="background-color: ${problem.color || 'transparent'}">
            <td>
                <i class="bi ${problem.favorite ? 'bi-star-fill text-warning' : 'bi-star'}" 
                   onclick="toggleFavorite(${problem.id})"
                   style="cursor: pointer"></i>
            </td>
            <td>
                <select class="color-select" 
                        onchange="updateColor(${problem.id}, this.value)"
                        style="background-color: ${problem.color || '#fff'}">
                    <option value="">无</option>
                    <option value="#ffcccc" ${problem.color === '#ffcccc' ? 'selected' : ''}>红</option>
                    <option value="#ccffcc" ${problem.color === '#ccffcc' ? 'selected' : ''}>绿</option>
                    <option value="#cce6ff" ${problem.color === '#cce6ff' ? 'selected' : ''}>蓝</option>
                </select>
            </td>
            <td>${problem.name}</td>
            <td><a href="${problem.link}" target="_blank">查看题目</a></td>
            <td>${problem.difficulty}</td>
            ${showType ? `<td>${problem.type}</td>` : '<td class="text-muted">[已隐藏]</td>'}
            <td>
                <select class="form-select" onchange="updateStatus(${problem.id}, this.value)">
                    <option value="未通过" ${problem.status === '未通过' ? 'selected' : ''}>未通过</option>
                    <option value="通过" ${problem.status === '通过' ? 'selected' : ''}>通过</option>
                    <option value="需复习" ${problem.status === '需复习' ? 'selected' : ''}>需复习</option>
                </select>
            </td>
        </tr>
    `).join('');
}

// 修改颜色更新函数
function updateColor(id, color) {
    const problem = problems.find(p => p.id === id);
    problem.color = color;
    
    // 立即更新行背景色
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (row) row.style.backgroundColor = color;
    
    saveToLocalStorage();
}

// 新增收藏切换函数
function toggleFavorite(id) {
    const problem = problems.find(p => p.id === id);
    problem.favorite = !problem.favorite;
    saveToLocalStorage();
    renderTable(currentDisplayData); // 保持当前显示数据不变
}

// 新增类型列切换函数
function toggleTypeColumn() {
    const button = document.getElementById('toggleType');
    button.classList.toggle('active');
    button.innerHTML = button.classList.contains('active') ? 
        '<i class="bi bi-eye"></i> 显示类型' : 
        '<i class="bi bi-eye-slash"></i> 隐藏类型';
    renderTable(currentDisplayData);
}

// 更新题目状态
function updateStatus(id, value) {
    const problem = problems.find(p => p.id === id);
    const prevStatus = problem.status;
    problem.status = value;

    // 积分逻辑
    if (prevStatus !== value) {
        points += value === '通过' ? 100 : -100;
        points = Math.max(points, 0);  // 积分不低于0
        updatePointsDisplay();
    }

    saveToLocalStorage();
}

// 重置积分
function resetPoints() {
    points = 0;
    updatePointsDisplay();
    saveToLocalStorage();
}

// 渲染商城
function renderShop() {
    const container = document.getElementById('shopItems');
    container.innerHTML = shopItems.map(item => `
      <div class="col-md-4">
        <div class="shop-card">
          <img src="${item.image}" class="img-fluid" alt="${item.name}">
          <h5>${item.name}</h5>
          <p class="text-muted">所需积分: ${item.cost}</p>
          <div class="d-flex justify-content-between">
            <span class="text-success">库存: ${item.stock}</span>
            <span class="text-primary">已兑换: ${item.redeemedCount}次</span>
          </div>
          <button 
            class="btn btn-primary redeem-btn" 
            onclick="redeemItem(${item.id})"
            ${points < item.cost || item.stock <= 0 ? 'disabled' : ''}
          >
            立即兑换
          </button>
        </div>
      </div>
    `).join('');
  }

// 商品兑换
function redeemItem(itemId) {
    const item = shopItems.find(i => i.id === itemId);
    if (!item || item.stock <= 0 || points < item.cost) return;
  
    // 更新数据
    points -= item.cost;
    item.stock--;
    item.redeemedCount++;  // 记录兑换次数
    
    updatePointsDisplay();
    renderShop();
    saveToLocalStorage();
  }

// 更新积分显示
function updatePointsDisplay() {
    document.getElementById('points').textContent = points;
}

// 本地存储
function saveToLocalStorage() {
    localStorage.setItem('lcData', JSON.stringify({
        problems,
        points,
        shopItems
    }));
}

function loadFromLocalStorage() {
    const saved = localStorage.getItem('lcData');
    if (saved) {
        const data = JSON.parse(saved);
        problems = data.problems || [];
        points = data.points || 0;
        shopItems = (data.shopItems || []).map(item => ({
            ...item,
            redeemedCount: item.redeemedCount || 0  // 确保旧数据兼容
          }));
        updatePointsDisplay();
        renderTable(problems);
        renderShop();
    }
}

// 重置所有商品的兑换记录
function resetRedemptions() {
    if (!confirm('确定要重置所有兑换记录吗？此操作不可逆！')) return;
    
    shopItems.forEach(item => {
      item.redeemedCount = 0;
    });
    
    saveToLocalStorage();
    renderShop();
  }
  

// 清空所有存档（危险操作！）
function clearAllData() {
    if (!confirm('⚠️ 这将永久删除所有数据！包括：\n\n• 已上传的题目列表\n• 积分记录\n• 商品兑换状态\n\n确定继续吗？')) return;
  
    // 清空本地存储
    localStorage.removeItem('lcData');
    
    // 重置内存数据
    problems = [];
    points = 0;
    shopItems = [];
    
    // 重新加载初始商品配置
    loadShopItems();
    
    // 更新界面
    updatePointsDisplay();
    renderTable([]);
    renderShop();
    
    // 清除文件输入
    document.getElementById('csvFile').value = '';
  }
  

// 随机题目
document.getElementById('randomBtn').addEventListener('click', function() {
    const count = Math.min(
        parseInt(document.getElementById('randomCount').value) || 1,
        problems.length
    );
    const shuffled = [...problems].sort(() => Math.random() - 0.5);
    renderTable(shuffled.slice(0, count));
});

// 排序功能
document.getElementById('sortOrder').addEventListener('change', function(e) {
    const sorted = [...problems].sort((a, b) => 
        e.target.value === 'asc' ? 
        a.difficulty - b.difficulty : 
        b.difficulty - a.difficulty
    );
    renderTable(sorted);
});
