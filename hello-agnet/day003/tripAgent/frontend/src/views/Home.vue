<template>
  <div class="home-container">
    <div class="page-header">
      <h1 class="page-title">✈️ 智能旅行助手</h1>
      <p class="page-subtitle">基于 AI 的个性化旅行规划</p>
    </div>

    <a-card class="form-card">
      <a-form :model="formData" layout="vertical" @finish="handleSubmit">
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="目的地城市" name="city" :rules="[{ required: true, message: '请输入目的地城市' }]">
              <a-input v-model:value="formData.city" placeholder="如：北京" />
            </a-form-item>
          </a-col>
          <a-col :span="6">
            <a-form-item label="出发日期" name="start_date" :rules="[{ required: true, message: '请选择出发日期' }]">
              <a-input v-model:value="formData.start_date" type="date" />
            </a-form-item>
          </a-col>
          <a-col :span="6">
            <a-form-item label="返程日期" name="end_date" :rules="[{ required: true, message: '请选择返程日期' }]">
              <a-input v-model:value="formData.end_date" type="date" />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="旅行天数" name="days">
              <a-input-number v-model:value="formData.days" :min="1" :max="30" style="width: 100%" />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="旅行偏好" name="preferences">
              <a-select v-model:value="formData.preferences">
                <a-select-option value="历史文化">历史文化</a-select-option>
                <a-select-option value="自然风光">自然风光</a-select-option>
                <a-select-option value="美食打卡">美食打卡</a-select-option>
                <a-select-option value="亲子游乐">亲子游乐</a-select-option>
                <a-select-option value="休闲度假">休闲度假</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="预算档位" name="budget">
              <a-select v-model:value="formData.budget">
                <a-select-option value="经济">经济</a-select-option>
                <a-select-option value="中等">中等</a-select-option>
                <a-select-option value="豪华">豪华</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="交通方式" name="transportation">
              <a-select v-model:value="formData.transportation">
                <a-select-option value="公共交通">公共交通</a-select-option>
                <a-select-option value="自驾">自驾</a-select-option>
                <a-select-option value="打车">打车</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="住宿类型" name="accommodation">
              <a-select v-model:value="formData.accommodation">
                <a-select-option value="经济型酒店">经济型酒店</a-select-option>
                <a-select-option value="舒适型酒店">舒适型酒店</a-select-option>
                <a-select-option value="豪华酒店">豪华酒店</a-select-option>
                <a-select-option value="民宿">民宿</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item>
          <a-button type="primary" html-type="submit" size="large" block :loading="loading">
            开始规划
          </a-button>
        </a-form-item>

        <a-form-item v-if="loading">
          <a-progress :percent="loadingProgress" status="active" />
          <p class="loading-status">{{ loadingStatus }}</p>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { generateTripPlan } from '@/services/api'
import type { TripPlanRequest } from '@/types'

const router = useRouter()

const loading = ref(false)
const loadingProgress = ref(0)
const loadingStatus = ref('')

const formData = ref<TripPlanRequest>({
  city: '',
  start_date: '',
  end_date: '',
  days: 3,
  preferences: '历史文化',
  budget: '中等',
  transportation: '公共交通',
  accommodation: '经济型酒店'
})

const handleSubmit = async () => {
  loading.value = true
  loadingProgress.value = 0

  // 模拟进度更新：后端无法实时回传进度，这里用定时器给用户反馈
  const progressInterval = setInterval(() => {
    if (loadingProgress.value < 90) {
      loadingProgress.value += 10
      if (loadingProgress.value <= 30) loadingStatus.value = '🔍 正在搜索景点...'
      else if (loadingProgress.value <= 50) loadingStatus.value = '🌤️ 正在查询天气...'
      else if (loadingProgress.value <= 70) loadingStatus.value = '🏨 正在推荐酒店...'
      else loadingStatus.value = '📋 正在生成行程计划...'
    }
  }, 500)

  try {
    const response = await generateTripPlan(formData.value)
    clearInterval(progressInterval)
    loadingProgress.value = 100
    loadingStatus.value = '✅ 完成！'
    router.push({ name: 'result', state: { tripPlan: response } as any })
  } catch (error) {
    clearInterval(progressInterval)
    message.error('生成计划失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.home-container {
  max-width: 880px;
  margin: 0 auto;
  padding: 48px 24px;
}
.page-header {
  text-align: center;
  margin-bottom: 32px;
}
.page-title {
  font-size: 36px;
  font-weight: 700;
  margin: 0;
}
.page-subtitle {
  color: #888;
  margin-top: 8px;
}
.form-card {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}
.loading-status {
  text-align: center;
  color: #1677ff;
  margin-top: 8px;
}
</style>
