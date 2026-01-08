// 全局变量
let map = null;
let markers = [];
let polyline = null;
let currentDay = 1;

// 三日旅游路线数据
const itineraryData = {
  1: {
    title: "第一天 - 皇城根下",
    spots: [
      {
        name: "天安门广场",
        lat: 39.9054,
        lng: 116.3976,
        description: "天安门广场是世界上最大的城市广场之一，位于北京市中心。广场周围有国家博物馆、人民大会堂等重要建筑。这里是中华人民共和国的象征，也是北京最著名的地标之一。",
        openTime: "全天开放",
        price: "免费",
        duration: "1-2小时",
        brief: "世界上最大的城市广场之一"
      },
      {
        name: "故宫博物院",
        lat: 39.9163,
        lng: 116.3972,
        description: "故宫是中国明清两代的皇家宫殿，旧称紫禁城，是世界上保存最完整的木质结构古建筑群。故宫收藏有大量珍贵文物，是了解中国古代宫廷文化的最佳场所。",
        openTime: "8:30-17:00（4-10月），8:30-16:30（11-3月）",
        price: "60元",
        duration: "3-4小时",
        brief: "明清皇家宫殿，世界文化遗产"
      },
      {
        name: "景山公园",
        lat: 39.9249,
        lng: 116.3964,
        description: "景山公园位于故宫北面，是北京中轴线上的制高点。登上万春亭可俯瞰整个故宫和北京城全景，是拍摄故宫全景的最佳位置。",
        openTime: "6:00-21:00",
        price: "10元",
        duration: "1-2小时",
        brief: "俯瞰故宫全景的最佳位置"
      }
    ]
  },
  2: {
    title: "第二天 - 长城雄风",
    spots: [
      {
        name: "八达岭长城",
        lat: 40.3600,
        lng: 116.0200,
        description: "八达岭长城是明长城中保存最好、最具代表性的一段。这里是长城向游客开放最早的地段，长城雄伟壮观，景色宜人，是体验'不到长城非好汉'的绝佳地点。",
        openTime: "6:00-19:00（4-10月），6:30-18:00（11-3月）",
        price: "40元",
        duration: "3-4小时",
        brief: "最具代表性的长城段落"
      },
      {
        name: "慕田峪长城",
        lat: 40.4320,
        lng: 116.5660,
        description: "慕田峪长城是明代开国大将徐达指挥修建的，这里植被覆盖率高，景色秀丽。相比八达岭，慕田峪游客较少，游览体验更佳，还设有滑道等娱乐项目。",
        openTime: "8:00-17:30",
        price: "45元",
        duration: "3-4小时",
        brief: "景色秀丽，游客相对较少"
      },
      {
        name: "明十三陵",
        lat: 40.2915,
        lng: 116.2300,
        description: "明十三陵是明朝迁都北京后13位皇帝陵墓的总称，其中定陵和长陵已对外开放。这里埋葬着明朝的13位皇帝，规模宏大，建筑精美，是了解明代陵寝文化的重要场所。",
        openTime: "8:00-17:30",
        price: "定陵50元，长陵35元",
        duration: "2-3小时",
        brief: "明朝13位皇帝陵墓群"
      }
    ]
  },
  3: {
    title: "第三天 - 皇家园林",
    spots: [
      {
        name: "颐和园",
        lat: 39.9999,
        lng: 116.2756,
        description: "颐和园是中国现存规模最大、保存最完整的皇家园林，被誉为'皇家园林博物馆'。园内以昆明湖、万寿山为基址，汇聚了江南园林的精华，景色秀美，建筑精美。",
        openTime: "6:30-18:00（4-10月），7:00-17:00（11-3月）",
        price: "30元",
        duration: "4-5小时",
        brief: "中国规模最大的皇家园林"
      },
      {
        name: "圆明园遗址公园",
        lat: 40.0077,
        lng: 116.2972,
        description: "圆明园是清代著名的皇家园林，曾被誉为'万园之园'。1860年被英法联军焚毁，现作为遗址公园对外开放。虽然大部分建筑已被毁，但仍有大量遗迹可寻，是了解中国近代历史的重要场所。",
        openTime: "7:00-19:30（4-10月），7:00-18:30（11-3月）",
        price: "10元",
        duration: "2-3小时",
        brief: "曾经的'万园之园'遗址"
      },
      {
        name: "天坛公园",
        lat: 39.8822,
        lng: 116.4066,
        description: "天坛是明清两代皇帝祭天、祈谷的场所，是中国古代建筑艺术的杰作。祈年殿、回音壁、圜丘坛等建筑体现了中国古代'天人合一'的哲学思想，是世界文化遗产。",
        openTime: "6:00-22:00（4-10月），6:30-21:00（11-3月）",
        price: "15元",
        duration: "2-3小时",
        brief: "明清皇帝祭天祈谷场所"
      }
    ]
  }
};

// 初始化地图
function initMap() {
  // 检查腾讯地图API是否加载
  if (typeof TMap === 'undefined') {
    console.warn('腾讯地图API未加载，可能API密钥无效');
    // 显示友好的提示信息
    const mapContainer = document.getElementById('map');
    if (mapContainer) {
      mapContainer.innerHTML = `
        <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center; color: white; border-radius: 8px;">
          <h3 style="color: white; margin-bottom: 15px; font-size: 1.5em;">🗺️ 地图组件</h3>
          <p style="color: rgba(255,255,255,0.9); margin-bottom: 10px; font-size: 1.1em;">腾讯地图正在加载...</p>
          <p style="color: rgba(255,255,255,0.7); font-size: 0.9em; margin-top: 10px;">如果地图未显示，请检查API密钥配置</p>
          <div style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.2); border-radius: 5px; max-width: 400px;">
            <p style="font-size: 0.85em; line-height: 1.6;">
              💡 提示：访问 <a href="https://lbs.qq.com/" target="_blank" style="color: #ffd700; text-decoration: underline;">腾讯地图开放平台</a> 申请API密钥
            </p>
          </div>
        </div>
      `;
    }
    return false;
  }

  try {
    // 初始化腾讯地图
    map = new TMap.Map('map', {
      center: new TMap.LatLng(39.9042, 116.4074), // 北京中心坐标
      zoom: 11,
      mapTypeId: TMap.MapTypeId.ROADMAP,
      viewMode: '2D'
    });

    console.log('✅ 腾讯地图初始化成功');
    return true;
  } catch (error) {
    console.error('❌ 地图初始化失败:', error);
    // 显示错误提示
    const mapContainer = document.getElementById('map');
    if (mapContainer) {
      mapContainer.innerHTML = `
        <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%; background: #f5f5f5; padding: 20px; text-align: center; border-radius: 8px;">
          <h3 style="color: #c41e3a; margin-bottom: 15px;">🗺️ 地图加载失败</h3>
          <p style="color: #666; margin-bottom: 15px;">请检查腾讯地图API密钥是否正确配置</p>
          <div style="background: #fff; padding: 15px; border-radius: 5px; margin-top: 15px; max-width: 400px;">
            <p style="color: #999; font-size: 0.9em; line-height: 1.6;">
              💡 解决方案：<br>
              1. 访问 <a href="https://lbs.qq.com/" target="_blank" style="color: #007bff;">腾讯地图开放平台</a> 申请API密钥<br>
              2. 在 index.html 中替换 API 密钥<br>
              3. 刷新页面重新加载地图
            </p>
          </div>
        </div>
      `;
    }
    return false;
  }
}

// 清除地图标记
function clearMarkers() {
  if (markers.length > 0) {
    markers.forEach(marker => {
      marker.setMap(null);
    });
    markers = [];
  }

  if (polyline) {
    polyline.setMap(null);
    polyline = null;
  }
}

// 添加景点标记
function addMarkers(spots) {
  if (!map) return;

  const path = [];

  spots.forEach((spot, index) => {
    const position = new TMap.LatLng(spot.lat, spot.lng);

    // 创建标记
    const marker = new TMap.MultiMarker({
      map: map,
      styles: {
        'marker': new TMap.MarkerStyle({
          width: 25,
          height: 35,
          anchor: { x: 12, y: 35 },
          src: `data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg" width="25" height="35" viewBox="0 0 25 35"><path fill="%23c41e3a" d="M12.5 0C5.6 0 0 5.6 0 12.5c0 8.75 12.5 22.5 12.5 22.5S25 21.25 25 12.5C25 5.6 19.4 0 12.5 0z"/><circle fill="white" cx="12.5" cy="12.5" r="4"/></svg>`
        })
      },
      geometries: [{
        id: `marker_${index}`,
        styleId: 'marker',
        position: position,
        properties: {
          title: spot.name
        }
      }]
    });

    markers.push(marker);
    path.push(position);

    // 添加点击事件
    marker.on('click', () => {
      showSpotDetail(spot);
      highlightSpotItem(index);
    });
  });

  // 绘制路线
  if (path.length > 1) {
    polyline = new TMap.MultiPolyline({
      map: map,
      styles: {
        'line': new TMap.PolylineStyle({
          color: '#c41e3a',
          width: 4,
          borderWidth: 2,
          borderColor: '#ffffff'
        })
      },
      geometries: [{
        styleId: 'line',
        paths: path
      }]
    });
  }

  // 调整地图视野
  if (path.length > 0) {
    map.fitBounds(path, {
      padding: 50
    });
  }
}

// 显示景点列表
function renderSpotsList(spots) {
  const container = document.getElementById('spotsContainer');
  if (!container) return;

  container.innerHTML = '';

  spots.forEach((spot, index) => {
    const item = document.createElement('div');
    item.className = 'spot-item';
    item.dataset.index = index;

    item.innerHTML = `
      <div class="spot-name">${index + 1}. ${spot.name}</div>
      <div class="spot-brief">${spot.brief}</div>
    `;

    item.addEventListener('click', () => {
      showSpotDetail(spot);
      highlightSpotItem(index);
      centerMapOnSpot(spot);
    });

    container.appendChild(item);
  });
}

// 高亮选中的景点
function highlightSpotItem(index) {
  const items = document.querySelectorAll('.spot-item');
  items.forEach((item, i) => {
    if (i === index) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });
}

// 将地图中心定位到景点
function centerMapOnSpot(spot) {
  if (!map) return;

  const position = new TMap.LatLng(spot.lat, spot.lng);
  map.setCenter(position);
  map.setZoom(15);
}

// 显示景点详情
function showSpotDetail(spot) {
  const detailSection = document.getElementById('detailSection');
  const detailTitle = document.getElementById('detailTitle');
  const detailDescription = document.getElementById('detailDescription');
  const detailOpenTime = document.getElementById('detailOpenTime');
  const detailPrice = document.getElementById('detailPrice');
  const detailDuration = document.getElementById('detailDuration');

  if (detailTitle) detailTitle.textContent = spot.name;
  if (detailDescription) detailDescription.textContent = spot.description;
  if (detailOpenTime) detailOpenTime.textContent = spot.openTime;
  if (detailPrice) detailPrice.textContent = spot.price;
  if (detailDuration) detailDuration.textContent = spot.duration;

  if (detailSection) {
    detailSection.style.display = 'block';
    // 滚动到详情区域
    detailSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

// 加载指定日期的路线
function loadItinerary(day) {
  currentDay = day;
  const data = itineraryData[day];

  if (!data) {
    console.error('未找到第' + day + '天的路线数据');
    return;
  }

  // 清除之前的标记
  clearMarkers();

  // 渲染景点列表
  renderSpotsList(data.spots);

  // 添加地图标记
  addMarkers(data.spots);

  console.log('已加载第' + day + '天路线:', data.title);
}

// 初始化页面
function initPage() {
  console.log('初始化页面...');

  // 初始化地图
  const mapInitialized = initMap();
  if (!mapInitialized) {
    console.warn('地图初始化失败，将只显示景点列表');
  }

  // 加载第一天的路线
  loadItinerary(1);

  // 绑定日期切换按钮事件
  const dayButtons = document.querySelectorAll('.day-btn');
  dayButtons.forEach(button => {
    button.addEventListener('click', function() {
      const day = parseInt(this.dataset.day);

      // 更新按钮状态
      dayButtons.forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');

      // 加载对应日期的路线
      loadItinerary(day);
    });
  });

  // 绑定详情关闭按钮事件
  const closeDetailBtn = document.getElementById('closeDetail');
  if (closeDetailBtn) {
    closeDetailBtn.addEventListener('click', () => {
      const detailSection = document.getElementById('detailSection');
      if (detailSection) {
        detailSection.style.display = 'none';
      }
    });
  }

  console.log('页面初始化完成');
}

// 页面加载完成后初始化
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initPage);
} else {
  initPage();
}
