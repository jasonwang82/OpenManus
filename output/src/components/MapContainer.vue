<template>
  <div class="map-container">
    <div id="baiduMap" ref="mapRef" class="baidu-map"></div>
    <div v-if="!isMapLoaded" class="map-loading">
      <el-icon class="is-loading">
        <Loading />
      </el-icon>
      <p>地图加载中...</p>
    </div>
  </div>
</template>

<script>
import { Loading } from 'element-ui';

export default {
  name: 'MapContainer',
  components: {
    Loading
  },
  props: {
    spots: {
      type: Array,
      default: () => []
    },
    center: {
      type: Object,
      default: () => ({ lng: 116.397428, lat: 39.90923 })
    },
    zoom: {
      type: Number,
      default: 13
    },
    showRoute: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      map: null,
      markers: [],
      polylines: [],
      isMapLoaded: false
    };
  },
  watch: {
    spots: {
      handler(newSpots) {
        if (this.map && newSpots.length > 0) {
          this.clearMap();
          this.addMarkers();
          if (this.showRoute) {
            this.addRouteLines();
          }
        }
      },
      deep: true
    }
  },
  mounted() {
    this.initMap();
  },
  beforeDestroy() {
    this.clearMap();
  },
  methods: {
    initMap() {
      if (typeof BMap === 'undefined') {
        console.error('百度地图API未加载');
        return;
      }

      this.map = new BMap.Map(this.$refs.mapRef);
      this.map.centerAndZoom(
        new BMap.Point(this.center.lng, this.center.lat),
        this.zoom
      );
      this.map.enableScrollWheelZoom(true);
      this.map.addControl(new BMap.NavigationControl());
      this.map.addControl(new BMap.ScaleControl());

      // 创建自定义图标
      const icon = new BMap.Icon(
        'https://api.map.baidu.com/images/markers.png',
        new BMap.Size(23, 25),
        {
          offset: new BMap.Size(10, 25),
          imageSize: new BMap.Size(23, 25)
        }
      );

      this.isMapLoaded = true;

      if (this.spots.length > 0) {
        this.addMarkers();
        if (this.showRoute) {
          this.addRouteLines();
        }
      }

      this.$emit('map-ready', this.map);
    },
    addMarkers() {
      this.spots.forEach((spot, index) => {
        const point = new BMap.Point(spot.position.lng, spot.position.lat);

        // 创建自定义标注
        const marker = new BMap.Marker(point);

        // 创建信息窗口
        const infoWindow = new BMap.InfoWindow(
          this.createInfoWindowContent(spot, index + 1),
          {
            width: 300,
            height: 250,
            title: `<strong>${spot.name}</strong>`
          }
        );

        marker.addEventListener('click', () => {
          this.map.openInfoWindow(infoWindow, point);
          this.$emit('spot-click', spot);
        });

        this.map.addOverlay(marker);
        this.markers.push(marker);
      });
    },
    createInfoWindowContent(spot, index) {
      return `
        <div style="padding: 10px; line-height: 1.6;">
          <p style="color: #666; margin-bottom: 8px;"><strong>景点 ${index}</strong></p>
          <p style="margin: 5px 0;">📍 ${spot.address}</p>
          <p style="margin: 5px 0;">🕒 ${spot.openingHours}</p>
          <p style="margin: 5px 0;">💰 ${spot.ticket}</p>
          <p style="margin: 5px 0;">⏱️ 建议游玩：${spot.duration}</p>
          <p style="margin-top: 10px; font-size: 12px; color: #999;">${spot.description}</p>
        </div>
      `;
    },
    addRouteLines() {
      if (this.spots.length < 2) return;

      const points = this.spots.map(spot =>
        new BMap.Point(spot.position.lng, spot.position.lat)
      );

      const polyline = new BMap.Polyline(points, {
        strokeColor: '#1890ff',
        strokeWeight: 4,
        strokeOpacity: 0.7
      });

      this.map.addOverlay(polyline);
      this.polylines.push(polyline);

      // 调整视野以显示所有标记点和路线
      this.map.setViewport(points);
    },
    clearMap() {
      // 清除所有标记
      this.markers.forEach(marker => {
        this.map.removeOverlay(marker);
      });
      this.markers = [];

      // 清除所有路线
      this.polylines.forEach(polyline => {
        this.map.removeOverlay(polyline);
      });
      this.polylines = [];
    },
    focusOnSpot(spot) {
      const point = new BMap.Point(spot.position.lng, spot.position.lat);
      this.map.centerAndZoom(point, 16);
    }
  }
};
</script>

<style scoped lang="scss">
.map-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: #f5f7fa;
}

.baidu-map {
  width: 100%;
  height: 100%;
}

.map-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #1890ff;

  .el-icon {
    font-size: 48px;
    margin-bottom: 10px;
  }

  p {
    font-size: 14px;
    color: #666;
  }
}
</style>
