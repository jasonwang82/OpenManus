<template>
  <div class="spot-card" @click="handleClick">
    <div class="spot-card__image">
      <el-image
        :src="imageSrc"
        fit="cover"
        style="width: 100%; height: 200px;"
      >
        <div slot="placeholder" class="image-placeholder">
          <el-icon><Picture /></el-icon>
        </div>
      </el-image>
      <div class="spot-card__number">{{ number }}</div>
    </div>

    <div class="spot-card__content">
      <h3 class="spot-card__name">{{ spot.name }}</h3>
      <p class="spot-card__name-en">{{ spot.nameEn }}</p>

      <div class="spot-card__info">
        <div class="info-item">
          <el-icon><Location /></el-icon>
          <span>{{ spot.address }}</span>
        </div>
        <div class="info-item">
          <el-icon><Clock /></el-icon>
          <span>{{ spot.openingHours }}</span>
        </div>
      </div>

      <div class="spot-card__tags">
        <el-tag size="small" type="warning">{{ spot.ticket }}</el-tag>
        <el-tag size="small" type="info">{{ spot.duration }}</el-tag>
      </div>

      <p class="spot-card__description">{{ spot.description }}</p>
    </div>
  </div>
</template>

<script>
import { Picture, Location, Clock } from 'element-ui';

export default {
  name: 'SpotCard',
  components: {
    Picture,
    Location,
    Clock
  },
  props: {
    spot: {
      type: Object,
      required: true
    },
    number: {
      type: Number,
      default: 1
    }
  },
  computed: {
    imageSrc() {
      // 使用占位图，实际项目中可以使用真实图片
      return `https://via.placeholder.com/400x300/667eea/ffffff?text=${encodeURIComponent(this.spot.name)}`;
    }
  },
  methods: {
    handleClick() {
      this.$emit('click', this.spot);
    }
  }
};
</script>

<style scoped lang="scss">
.spot-card {
  background: $theme-card-bg;
  border-radius: $border-radius;
  box-shadow: $shadow-card;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
}

.spot-card__image {
  position: relative;
  width: 100%;
  height: 200px;
  background-color: #f0f0f0;
  overflow: hidden;

  .image-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ccc;
    font-size: 48px;
  }
}

.spot-card__number {
  position: absolute;
  top: $spacing-md;
  left: $spacing-md;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: $font-size-large;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.spot-card__content {
  padding: $spacing-lg;
}

.spot-card__name {
  font-size: $font-size-large;
  font-weight: 600;
  color: #333;
  margin: $spacing-xs 0 $spacing-xs;
}

.spot-card__name-en {
  font-size: $font-size-small;
  color: #999;
  margin: 0 0 $spacing-md;
  font-style: italic;
}

.spot-card__info {
  margin-bottom: $spacing-md;

  .info-item {
    display: flex;
    align-items: center;
    gap: $spacing-xs;
    color: #666;
    font-size: $font-size-small;
    margin-bottom: $spacing-xs;

    &:last-child {
      margin-bottom: 0;
    }

    .el-icon {
      color: $primary-color;
    }
  }
}

.spot-card__tags {
  display: flex;
  gap: $spacing-xs;
  margin-bottom: $spacing-md;
}

.spot-card__description {
  color: #666;
  font-size: $font-size-small;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
