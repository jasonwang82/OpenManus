<template>
  <div class="day-plan">
    <div class="day-plan__header">
      <div class="day-plan__date">{{ day.date }}</div>
      <h3 class="day-plan__title">{{ day.title }}</h3>
      <div class="day-plan__theme">
        <el-tag type="primary" size="small">{{ day.theme }}</el-tag>
      </div>
    </div>

    <div class="day-plan__content">
      <div
        v-for="(spot, index) in day.spots"
        :key="spot.id"
        class="day-plan__spot"
        :class="{ 'day-plan__spot--active': activeSpotId === spot.id }"
        @click="handleSpotClick(spot)"
      >
        <div class="day-plan__spot-number">
          <span>{{ index + 1 }}</span>
        </div>

        <div class="day-plan__spot-info">
          <h4 class="day-plan__spot-name">{{ spot.name }}</h4>
          <p class="day-plan__spot-name-en">{{ spot.nameEn }}</p>

          <div class="day-plan__spot-details">
            <div class="detail-item">
              <el-icon><Location /></el-icon>
              <span>{{ spot.address }}</span>
            </div>
            <div class="detail-item">
              <el-icon><Clock /></el-icon>
              <span>{{ spot.openingHours }}</span>
            </div>
            <div class="detail-item">
              <el-icon><Tickets /></el-icon>
              <span>{{ spot.ticket }}</span>
            </div>
            <div class="detail-item">
              <el-icon><Timer /></el-icon>
              <span>{{ spot.duration }}</span>
            </div>
          </div>

          <div class="day-plan__spot-description">
            {{ spot.description }}
          </div>

          <div class="day-plan__spot-tips">
            <el-alert
              :title="'💡 小贴士'"
              type="info"
              :closable="false"
              show-icon
            >
              {{ spot.tips }}
            </el-alert>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Location, Clock, Tickets, Timer } from 'element-ui';

export default {
  name: 'DayPlan',
  components: {
    Location,
    Clock,
    Tickets,
    Timer
  },
  props: {
    day: {
      type: Object,
      required: true
    },
    activeSpotId: {
      type: Number,
      default: null
    }
  },
  methods: {
    handleSpotClick(spot) {
      this.$emit('spot-click', spot);
    }
  }
};
</script>

<style scoped lang="scss">
.day-plan {
  margin-bottom: $spacing-xl;

  &__header {
    position: relative;
    padding: $spacing-lg;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: $border-radius $border-radius 0 0;
    text-align: center;
  }

  &__date {
    font-size: 48px;
    font-weight: bold;
    opacity: 0.9;
    line-height: 1;
    margin-bottom: $spacing-sm;
  }

  &__title {
    font-size: $font-size-large;
    font-weight: 600;
    margin: $spacing-xs 0 $spacing-sm;
  }

  &__theme {
    margin-top: $spacing-xs;
  }

  &__content {
    background: $theme-card-bg;
    border-radius: 0 0 $border-radius $border-radius;
    box-shadow: $shadow-card;
    overflow: hidden;
  }

  &__spot {
    position: relative;
    padding: $spacing-lg;
    border-bottom: 1px solid $border-color;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    gap: $spacing-md;

    &:last-child {
      border-bottom: none;
    }

    &:hover {
      background-color: #f8f9fa;
    }

    &--active {
      background-color: #e6f7ff;
      border-left: 4px solid $primary-color;
    }
  }

  &__spot-number {
    flex-shrink: 0;
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 20px;
    font-weight: bold;
    margin-right: $spacing-md;
  }

  &__spot-info {
    flex: 1;
  }

  &__spot-name {
    font-size: $font-size-large;
    font-weight: 600;
    color: #333;
    margin: $spacing-xs 0 $spacing-xs;
  }

  &__spot-name-en {
    font-size: $font-size-small;
    color: #999;
    margin: 0 0 $spacing-sm;
    font-style: italic;
  }

  &__spot-details {
    display: flex;
    flex-wrap: wrap;
    gap: $spacing-md;
    margin: $spacing-md 0;

    .detail-item {
      display: flex;
      align-items: center;
      gap: $spacing-xs;
      color: #666;
      font-size: $font-size-base;

      .el-icon {
        color: $primary-color;
      }
    }
  }

  &__spot-description {
    color: #666;
    line-height: 1.6;
    margin: $spacing-md 0;
  }

  &__spot-tips {
    margin-top: $spacing-md;

    ::v-deep .el-alert {
      background-color: #f0f9ff;
      border-color: #bae7ff;

      .el-alert__content {
        color: #096dd9;
      }

      .el-icon {
        color: #1890ff;
      }
    }
  }
}
</style>
