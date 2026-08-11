<template>
  <div class="result-container" v-if="tripPlan">
    <!-- 顶部信息 -->
    <a-page-header
      class="page-header"
      :title="`${tripPlan.city} · 旅行计划`"
      :sub-title="`${tripPlan.start_date} 至 ${tripPlan.end_date}`"
      @back="goHome"
    >
      <template #extra>
        <a-button @click="goHome">重新规划</a-button>
      </template>
    </a-page-header>

    <!-- 总体建议 -->
    <a-alert
      v-if="tripPlan.overall_suggestions"
      type="info"
      show-icon
      class="block"
      :message="'总体建议'"
      :description="tripPlan.overall_suggestions"
    />

    <!-- 预算总览 -->
    <a-card class="block" title="💰 预算总览" size="small" v-if="tripPlan.budget">
      <a-descriptions :column="{ xs: 1, sm: 2, md: 3 }" size="small" bordered>
        <a-descriptions-item label="景点门票">¥{{ tripPlan.budget.total_attractions }}</a-descriptions-item>
        <a-descriptions-item label="酒店">¥{{ tripPlan.budget.total_hotels }}</a-descriptions-item>
        <a-descriptions-item label="餐饮">¥{{ tripPlan.budget.total_meals }}</a-descriptions-item>
        <a-descriptions-item label="交通">¥{{ tripPlan.budget.total_transportation }}</a-descriptions-item>
        <a-descriptions-item label="合计">
          <strong style="color: #f5222d">¥{{ tripPlan.budget.total }}</strong>
        </a-descriptions-item>
      </a-descriptions>
    </a-card>

    <!-- 天气 -->
    <a-card class="block" title="🌤️ 天气参考" size="small" v-if="tripPlan.weather_info?.length">
      <a-space wrap>
        <a-tag v-for="w in tripPlan.weather_info" :key="w.date" color="blue">
          {{ w.date }}：{{ w.day_weather || '—' }} {{ w.day_temp ?? '—' }}°
          <template v-if="w.wind_direction || w.wind_power"> · {{ w.wind_direction }} {{ w.wind_power }}</template>
        </a-tag>
      </a-space>
    </a-card>

    <!-- 每日行程 -->
    <a-card
      class="block"
      v-for="(day, idx) in tripPlan.days"
      :key="idx"
      :title="`第 ${displayDay(day)} 天 · ${day.date || ''}`"
      size="small"
    >
      <p class="day-desc">{{ day.description }}</p>

      <!-- 景点 -->
      <a-divider orientation="left" plain>景点</a-divider>
      <a-empty v-if="!day.attractions?.length" description="暂无景点" />
      <a-list v-else :data-source="day.attractions" item-layout="horizontal">
        <template #renderItem="{ item }">
          <a-list-item>
            <a-list-item-meta>
              <template #avatar v-if="item.image_url">
                <a-image
                  :src="item.image_url"
                  :width="56"
                  :height="56"
                  :preview="{ mask: false }"
                  style="border-radius: 6px; object-fit: cover; cursor: pointer; display: block"
                />
              </template>
              <template #title>
                <span class="attr-name">{{ item.name }}</span>
                <a-tag v-if="item.category" color="green" class="attr-tag">{{ item.category }}</a-tag>
                <a-tag v-if="item.rating != null" color="gold">★ {{ item.rating }}</a-tag>
              </template>
              <template #description>
                <div class="attr-meta">
                  <span>🕒 约 {{ item.visit_duration }} 分钟</span>
                  <span v-if="item.ticket_price">🎫 ¥{{ item.ticket_price }}</span>
                  <span v-if="item.address">📍 {{ item.address }}</span>
                </div>
                <div v-if="item.description" class="attr-desc">{{ item.description }}</div>
              </template>
            </a-list-item-meta>
          </a-list-item>
        </template>
      </a-list>

      <!-- 餐饮 -->
      <a-divider orientation="left" plain>餐饮</a-divider>
      <a-empty v-if="!day.meals?.length" description="暂无餐饮安排" />
      <a-space v-else wrap>
        <a-tag v-for="(m, i) in day.meals" :key="i" color="orange">
          {{ mealLabel(m.type) }}：{{ m.name }}
          <template v-if="m.estimated_cost"> · ¥{{ m.estimated_cost }}</template>
        </a-tag>
      </a-space>

      <!-- 酒店 -->
      <a-divider orientation="left" plain>住宿</a-divider>
      <a-empty v-if="!day.hotel" description="暂无住宿安排" />
      <a-descriptions v-else size="small" bordered :column="1">
        <a-descriptions-item label="酒店">{{ day.hotel.name }}</a-descriptions-item>
        <a-descriptions-item label="类型" v-if="day.hotel.type">{{ day.hotel.type }}</a-descriptions-item>
        <a-descriptions-item label="评分" v-if="day.hotel.rating != null">{{ day.hotel.rating }}</a-descriptions-item>
        <a-descriptions-item label="价格" v-if="day.hotel.price_range">{{ day.hotel.price_range }}</a-descriptions-item>
        <a-descriptions-item label="预估费用" v-if="day.hotel.estimated_cost">¥{{ day.hotel.estimated_cost }}/晚</a-descriptions-item>
        <a-descriptions-item label="地址" v-if="day.hotel.address">{{ day.hotel.address }}</a-descriptions-item>
      </a-descriptions>

      <div class="day-footer">
        <a-tag color="cyan">🚗 {{ day.transportation || '—' }}</a-tag>
        <a-tag color="purple">🏠 {{ day.accommodation || '—' }}</a-tag>
      </div>
    </a-card>
  </div>

  <!-- 未携带数据（如直接访问 /result 或刷新） -->
  <div class="result-container" v-else>
    <a-empty description="没有可显示的旅行计划，请先生成">
      <a-button type="primary" @click="goHome">去规划</a-button>
    </a-empty>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import type { DayPlan, TripPlan } from '@/types'

const router = useRouter()

// Home.vue 通过 router.push({ state: { tripPlan } }) 传递数据
const tripPlan = computed<TripPlan | undefined>(
  () => (history.state as { tripPlan?: TripPlan })?.tripPlan
)

const goHome = () => router.push('/')

// day_index 从 0 开始，展示时 +1
const displayDay = (day: DayPlan) => (day.day_index ?? 0) + 1

const mealLabel = (type?: string) => {
  const map: Record<string, string> = {
    breakfast: '早餐',
    lunch: '午餐',
    dinner: '晚餐',
    snack: '小吃'
  }
  return (type && map[type]) || type || '餐饮'
}
</script>

<style scoped>
.result-container {
  max-width: 920px;
  margin: 0 auto;
  padding: 24px;
}
.block {
  margin-bottom: 20px;
}
.page-header {
  background: #fff;
  border-radius: 8px;
  margin-bottom: 16px;
}
.day-desc {
  color: #555;
  margin: 0 0 8px;
}
.attr-name {
  font-weight: 600;
}
.attr-tag {
  margin-left: 6px;
}
.attr-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  color: #888;
  font-size: 13px;
  margin: 4px 0;
}
.attr-desc {
  color: #666;
  font-size: 13px;
}
.day-footer {
  margin-top: 12px;
}
</style>
