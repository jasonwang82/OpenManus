<template>
  <div class="travel-guide">
    <div class="travel-guide__header">
      <h1 class="travel-guide__title">{{ travelData.title }}</h1>
      <p class="travel-guide__subtitle">{{ travelData.subtitle }}</p>
    </div>

    <div class="travel-guide__content">
      <!-- 左侧地图区域 -->
      <div class="travel-guide__map">
        <map-container
          ref="mapContainer"
          :spots="currentDaySpots"
          :show-route="showRoute"
          @spot-click="handleMapSpotClick"
          @map-ready="handleMapReady"
        />
      </div>

      <!-- 右侧路书列表 -->
      <div class="travel-guide__plans">
        <!-- 日期切换 -->
        <div class="travel-guide__tabs">
          <el-tabs v-model="activeDayIndex" type="card">
            <el-tab-pane
              v-for="day in travelData.days"
              :key="day.id"
              :label="day.date"
              :name="String(day.id)"
            >
              <template slot="label">
                <span class="day-tab-label">
                  <span class="day-tab__date">{{ day.date }}</span>
                  <span class="day-tab__title">{{ day.title.replace('第一天：', '').replace('第二天：', '').replace('第三天：', '') }}</span>
                </span>
              </template>
            </el-tab-pane>
          </el-tabs>
        </div>

        <!-- 当前日期的详细计划 -->
        <div class="travel-guide__plan-list">
          <day-plan
            :day="currentDay"
            :active-spot-id="activeSpotId"
            @spot-click="handlePlanSpotClick"
          />
        </div>

        <!-- 控制按钮 -->
        <div class="travel-guide__controls">
          <el-button-group>
            <el-button
              type="primary"
              icon="el-icon-map-location"
              @click="toggleRoute"
            >
              {{ showRoute ? '隐藏路线' : '显示路线' }}
            </el-button>
            <el-button
              type="success"
              icon="el-icon-full-screen"
              @click="fitView"
            >
              全景视图
            </el-button>
            <el-button
              type="warning"
              icon="el-icon-location"
              @click="navigateToFirst"
            >
              回到起点
            </el-button>
          </el-button-group>
        </div>

        <!-- 所有景点卡片网格 -->
        <div class="travel-guide__spots-grid">
          <h3 class="spots-grid__title">
            <el-icon><Grid /></el-icon>
            所有景点概览
          </h3>
          <el-row :gutter="20">
            <el-col
              v-for="(day, dayIndex) in travelData.days"
              :key="day.id"
              :span="12"
            >
              <div
                v-for="(spot, spotIndex) in day.spots"
                :key="spot.id"
                class="spot-card-wrapper"
              >
                <spot-card
                  :spot="spot"
                  :number="spotIndex + 1"
                  @click="handleSpotCardClick(spot, day.id)"
                />
              </div>
            </el-col>
          </el-row>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import travelData from '@/data/travelData';
import MapContainer from '@/components/MapContainer.vue';
import DayPlan from '@/components/DayPlan.vue';
import SpotCard from '@/components/SpotCard.vue';
import { Grid } from 'element-ui';

export default {
  name: 'TravelGuide',
  components: {
    MapContainer,
    DayPlan,
    SpotCard,
    Grid
  },
  data() {
    return {
      travelData,
      activeDayIndex: '1',
      activeSpotId: null,
      showRoute: true,
      map: null
    };
  },
  computed: {
    currentDay() {
      return this.travelData.days.find(day => day.id === parseInt(this.activeDayIndex));
    },
    currentDaySpots() {
      return this.currentDay ? this.currentDay.spots : [];
    }
  },
  methods: {
    handleMapReady(map) {
      this.map = map;
    },
    handleMapSpotClick(spot) {
      this.activeSpotId = spot.id;
      // 找到该景点所属的日期并切换
      const day = this.travelData.days.find(d =>
        d.spots.some(s => s.id === spot.id)
      );
      if (day) {
        this.activeDayIndex = String(day.id);
      }
    },
    handlePlanSpotClick(spot) {
      this.activeSpotId = spot.id;
      if (this.$refs.mapContainer) {
        this.$refs.mapContainer.focusOnSpot(spot);
      }
    },
    handleSpotCardClick(spot, dayId) {
      this.activeDayIndex = String(dayId);
      this.activeSpotId = spot.id;
      if (this.$refs.mapContainer) {
        this.$refs.mapContainer.focusOnSpot(spot);
      }
    },
    toggleRoute() {
      this.showRoute = !this.showRoute;
    },
    fitView() {
      if (this.$refs.mapContainer) {
        const points = this.currentDaySpots.map(spot =>
          new BMap.Point(spot.position.lng, spot.position.lat)
        );
        this.$refs.mapContainer.map.setViewport(points);
      }
    },
    navigateToFirst() {
      if (this.currentDaySpots.length > 0) {
        this.$refs.mapContainer.focusOnSpot(this.currentDaySpots[0]);
      }
    }
  }
};
</script>

<style scoped lang="scss">
.travel-guide {
  min-height: 100vh;
  background-color: $theme-bg;

  &__header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: $spacing-xl $spacing-lg;
    text-align: center;
    box-shadow: $shadow-base;
  }

  &__title {
    font-size: 32px;
    font-weight: bold;
    margin-bottom: $spacing-sm;
  }

  &__subtitle {
    font-size: $font-size-base;
    opacity: 0.9;
  }

  &__content {
    display: flex;
    height: calc(100vh - 120px);
  }

  &__map {
    flex: 0 0 60%;
    position: relative;
  }

  &__plans {
    flex: 1;
    overflow-y: auto;
    padding: $spacing-lg;
    background-color: $theme-bg;
  }

  &__tabs {
    margin-bottom: $spacing-lg;

    ::v-deep .el-tabs--card > .el-tabs__header .el-tabs__nav {
      border: none;
      background-color: transparent;
    }

    ::v-deep .el-tabs__item {
      background-color: white;
      border: 1px solid $border-color;
      margin-right: $spacing-xs;
      border-radius: $border-radius $border-radius 0 0;

      &.is-active {
        background-color: $primary-color;
        color: white;
        border-color: $primary-color;
      }
    }

    .day-tab-label {
      display: flex;
      flex-direction: column;
      align-items: center;

      .day-tab__date {
        font-size: $font-size-small;
        opacity: 0.8;
      }

      .day-tab__title {
        font-size: $font-size-base;
        font-weight: 500;
      }
    }
  }

  &__plan-list {
    margin-bottom: $spacing-lg;
  }

  &__controls {
    margin-bottom: $spacing-xl;
    text-align: center;
  }

  &__spots-grid {
    margin-top: $spacing-xl;

    .spots-grid__title {
      font-size: $font-size-large;
      font-weight: 600;
      color: #333;
      margin-bottom: $spacing-lg;
      display: flex;
      align-items: center;
      gap: $spacing-xs;

      .el-icon {
        color: $primary-color;
      }
    }

    .spot-card-wrapper {
      margin-bottom: $spacing-lg;
    }
  }
}

// 响应式设计
@media (max-width: 1200px) {
  .travel-guide {
    &__content {
      flex-direction: column;
      height: auto;
    }

    &__map {
      flex: none;
      height: 500px;
    }
  }
}

@media (max-width: 768px) {
  .travel-guide {
    &__title {
      font-size: 24px;
    }

    &__content {
      height: auto;
    }

    &__map {
      height: 400px;
    }

    &__plans {
      padding: $spacing-md;
    }

    &__controls {
      ::v-deep .el-button-group {
        display: flex;
        flex-direction: column;
        gap: $spacing-xs;

        .el-button {
          width: 100%;
        }
      }
    }
  }
}
</style>
