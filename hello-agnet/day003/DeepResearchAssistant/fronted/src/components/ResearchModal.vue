<template>
  <Teleport to="body">
    <div v-if="isOpen" class="modal-overlay" @click.self="close">
      <div class="modal-container" :class="{ 'modal-enter': isEntering }">
        <!-- 顶部栏 -->
        <div class="modal-header">
          <div class="header-left">
            <span class="header-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
              </svg>
            </span>
            <h2 class="header-title">{{ researchTopic }}</h2>
          </div>
          <button @click="close" class="close-button" title="关闭 (ESC)">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 6 6 18"></path>
              <path d="m6 6 12 12"></path>
            </svg>
          </button>
        </div>

        <!-- 进度区域 -->
        <div class="progress-section">
          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: progressPercentage + '%' }"
              :class="{
                'progress-planning': currentStage === 'planning',
                'progress-executing': currentStage === 'executing',
                'progress-reporting': currentStage === 'reporting',
                'progress-completed': currentStage === 'completed'
              }"
            ></div>
          </div>
          <div class="progress-info">
            <span class="progress-text">
              <span v-if="currentStage === 'planning'" class="stage-badge stage-planning">规划</span>
              <span v-else-if="currentStage === 'executing'" class="stage-badge stage-executing">执行</span>
              <span v-else-if="currentStage === 'reporting'" class="stage-badge stage-reporting">报告</span>
              <span v-else-if="currentStage === 'completed'" class="stage-badge stage-completed">完成</span>
              {{ progressText }}
            </span>
            <span class="progress-percentage">{{ Math.round(progressPercentage) }}%</span>
          </div>
        </div>

        <!-- 内容区域 -->
        <div class="content-section">
          <!-- 加载中状态 -->
          <div v-if="isLoading && !markdownContent" class="loading-state">
            <div class="loading-spinner">
              <div class="spinner"></div>
            </div>
            <div class="loading-tips">
              <p class="loading-title">深度研究中，请稍候...</p>
              <p class="loading-subtitle">系统正在搜索相关资料并进行分析</p>
              <div class="loading-stages">
                <div class="stage-item" :class="{ active: currentStage === 'planning', done: stageDone.planning }">
                  <div class="stage-dot">
                    <svg v-if="stageDone.planning" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    <span v-else>1</span>
                  </div>
                  <span class="stage-label">规划研究</span>
                </div>
                <div class="stage-connector" :class="{ active: currentStage === 'executing' || stageDone.executing }"></div>
                <div class="stage-item" :class="{ active: currentStage === 'executing', done: stageDone.executing }">
                  <div class="stage-dot">
                    <svg v-if="stageDone.executing" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    <span v-else>2</span>
                  </div>
                  <span class="stage-label">执行搜索</span>
                </div>
                <div class="stage-connector" :class="{ active: currentStage === 'reporting' || stageDone.reporting }"></div>
                <div class="stage-item" :class="{ active: currentStage === 'reporting', done: stageDone.reporting }">
                  <div class="stage-dot">
                    <svg v-if="stageDone.reporting" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    <span v-else>3</span>
                  </div>
                  <span class="stage-label">生成报告</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 错误状态 -->
          <div v-else-if="error" class="error-state">
            <div class="error-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="m15 9-6 6"></path>
                <path d="m9 9 6 6"></path>
              </svg>
            </div>
            <h3 class="error-title">研究过程中出现错误</h3>
            <p class="error-message">{{ error }}</p>
            <button @click="retry" class="retry-button">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                <path d="M3 3v5h5"></path>
              </svg>
              重新开始
            </button>
          </div>

          <!-- Markdown 内容 -->
          <div v-else class="markdown-body" v-html="renderedMarkdown"></div>
        </div>

        <!-- 底部栏 -->
        <div class="modal-footer">
          <div class="footer-left">
            <span class="status-indicator" :class="statusClass"></span>
            <span class="status-text">{{ statusText }}</span>
          </div>
          <div class="footer-right">
            <span v-if="isLoading" class="footer-tip">研究过程中可随时关闭，进度不会丢失</span>
            <button v-if="!isLoading && markdownContent" @click="copyContent" class="action-button">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
              复制内容
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch, onBeforeUnmount } from 'vue'
import { marked } from 'marked'
import { useResearch } from '@/composables/useResearch'

interface Props {
  isOpen: boolean
  researchTopic: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  close: []
  retry: [topic: string]
}>()

const isEntering = ref(false)

// 阶段状态追踪
const stageDone = ref({
  planning: false,
  executing: false,
  reporting: false
})

// 使用 research composable
const {
  isLoading,
  progressPercentage,
  progressText,
  markdownContent,
  error,
  currentStage,
  startResearch,
  stopResearch,
  reset
} = useResearch()

// 配置 marked
marked.setOptions({
  breaks: true,
  gfm: true
})

// 渲染 Markdown
const renderedMarkdown = computed(() => {
  if (!markdownContent.value) return ''
  return marked(markdownContent.value) as string
})

// 状态文本
const statusText = computed(() => {
  if (error.value) return '研究出错'
  if (currentStage.value === 'completed') return '研究完成'
  if (isLoading.value) return progressText.value || '研究中...'
  return '准备就绪'
})

// 状态指示器样式
const statusClass = computed(() => {
  if (error.value) return 'status-error'
  if (currentStage.value === 'completed') return 'status-completed'
  if (isLoading.value) return 'status-loading'
  return 'status-idle'
})

// 关闭模态框
const close = () => {
  stopResearch()
  emit('close')
}

// 重试
const retry = () => {
  reset()
  stageDone.value = { planning: false, executing: false, reporting: false }
  emit('retry', props.researchTopic)
}

// 复制内容
const copyContent = async () => {
  try {
    await navigator.clipboard.writeText(markdownContent.value)
    alert('研究内容已复制到剪贴板')
  } catch {
    alert('复制失败，请手动复制')
  }
}

// 键盘监听
const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && props.isOpen) {
    close()
  }
}

// 监听模态框打开/关闭
watch(
  () => props.isOpen,
  (isOpen) => {
    if (isOpen) {
      isEntering.value = true
      setTimeout(() => {
        isEntering.value = false
      }, 50)
      document.addEventListener('keydown', handleKeydown)
      document.body.style.overflow = 'hidden'

      // 自动开始研究
      reset()
      stageDone.value = { planning: false, executing: false, reporting: false }
      startResearch(props.researchTopic, onPlan, onTaskSummary)
    } else {
      document.removeEventListener('keydown', handleKeydown)
      document.body.style.overflow = ''
      stopResearch()
      reset()
    }
  }
)

// 规划完成回调
const onPlan = () => {
  stageDone.value.planning = true
}

// 任务总结回调
const onTaskSummary = (taskId: string, summary: string) => {
  stageDone.value.executing = true
}

// 监听阶段变化，更新阶段完成状态
watch(currentStage, (stage) => {
  if (stage === 'executing') {
    stageDone.value.planning = true
  }
  if (stage === 'reporting') {
    stageDone.value.planning = true
    stageDone.value.executing = true
  }
  if (stage === 'completed') {
    stageDone.value.planning = true
    stageDone.value.executing = true
    stageDone.value.reporting = true
  }
})

// 组件卸载时清理
onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleKeydown)
  document.body.style.overflow = ''
  stopResearch()
})
</script>

<style scoped>
/* ============================================
   模态框覆盖层
   ============================================ */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

@keyframes overlayFadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* ============================================
   模态框容器
   ============================================ */
.modal-container {
  width: 90vw;
  height: 88vh;
  max-width: 1200px;
  background-color: #ffffff;
  border-radius: 20px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: containerSlideUp 0.3s ease;
}

.modal-enter .modal-container {
  animation: none;
}

@keyframes containerSlideUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.97);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* ============================================
   顶部栏
   ============================================ */
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  flex: 1;
}

.header-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background-color: var(--primary-light);
  color: var(--primary-color);
  border-radius: 10px;
  flex-shrink: 0;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.close-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  background: none;
  color: var(--text-muted);
  border-radius: 10px;
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.close-button:hover {
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
}

/* ============================================
   进度区域
   ============================================ */
.progress-section {
  padding: 16px 24px;
  border-bottom: 1px solid var(--border-light);
  flex-shrink: 0;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: var(--bg-tertiary);
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 10px;
  transition: width 0.5s ease, background-color 0.3s ease;
  background: linear-gradient(90deg, var(--primary-color), #818cf8);
  background-size: 200% 100%;
  animation: progressPulse 2s ease infinite;
}

.progress-planning {
  background: linear-gradient(90deg, #4a6cf7, #6366f1);
}

.progress-executing {
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
}

.progress-reporting {
  background: linear-gradient(90deg, #8b5cf6, #a855f7);
}

.progress-completed {
  background: linear-gradient(90deg, #10b981, #34d399);
  animation: none;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.progress-text {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-secondary);
}

.progress-percentage {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
}

/* 阶段徽章 */
.stage-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  line-height: 1.6;
  flex-shrink: 0;
}

.stage-planning {
  background-color: #e8ecff;
  color: #4a6cf7;
}

.stage-executing {
  background-color: #ede9fe;
  color: #8b5cf6;
}

.stage-reporting {
  background-color: #f3e8ff;
  color: #a855f7;
}

.stage-completed {
  background-color: #d1fae5;
  color: #059669;
}

/* ============================================
   内容区域
   ============================================ */
.content-section {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  min-height: 0;
}

/* ============================================
   加载状态
   ============================================ */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 32px;
  animation: fadeIn 0.5s ease;
}

.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-tips {
  text-align: center;
}

.loading-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.loading-subtitle {
  font-size: 14px;
  color: var(--text-muted);
  margin-bottom: 24px;
}

/* 阶段步骤指示器 */
.loading-stages {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
}

.stage-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.stage-dot {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  background-color: var(--bg-tertiary);
  color: var(--text-muted);
  border: 2px solid var(--border-color);
  transition: all var(--transition-normal);
}

.stage-item.active .stage-dot {
  background-color: var(--primary-color);
  color: #fff;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 4px var(--primary-light);
}

.stage-item.done .stage-dot {
  background-color: var(--success-color);
  color: #fff;
  border-color: var(--success-color);
}

.stage-label {
  font-size: 12px;
  color: var(--text-muted);
  white-space: nowrap;
}

.stage-item.active .stage-label {
  color: var(--primary-color);
  font-weight: 600;
}

.stage-item.done .stage-label {
  color: var(--success-color);
  font-weight: 600;
}

.stage-connector {
  width: 60px;
  height: 2px;
  background-color: var(--border-color);
  margin: 0 8px;
  margin-bottom: 40px;
  transition: background-color var(--transition-normal);
}

.stage-connector.active {
  background-color: var(--primary-color);
}

/* ============================================
   错误状态
   ============================================ */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 16px;
  animation: fadeIn 0.3s ease;
}

.error-icon {
  color: var(--error-color);
}

.error-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.error-message {
  font-size: 14px;
  color: var(--text-secondary);
  text-align: center;
  max-width: 400px;
}

.retry-button {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  padding: 10px 20px;
  background-color: var(--primary-color);
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  transition: background-color var(--transition-fast);
}

.retry-button:hover {
  background-color: var(--primary-hover);
}

/* ============================================
   Markdown 内容样式
   ============================================ */
.markdown-body {
  animation: fadeIn 0.3s ease;
  max-width: 100%;
}

.markdown-body :deep(h1) {
  font-size: 26px;
  font-weight: 700;
  color: var(--text-primary);
  margin-top: 0;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-color);
}

.markdown-body :deep(h2) {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-top: 28px;
  margin-bottom: 12px;
}

.markdown-body :deep(h3) {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  margin-top: 20px;
  margin-bottom: 8px;
}

.markdown-body :deep(h4) {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-top: 16px;
  margin-bottom: 6px;
}

.markdown-body :deep(p) {
  font-size: 15px;
  line-height: 1.8;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 24px;
  margin-bottom: 12px;
}

.markdown-body :deep(li) {
  font-size: 15px;
  line-height: 1.8;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.markdown-body :deep(blockquote) {
  margin: 12px 0;
  padding: 12px 16px;
  border-left: 4px solid var(--primary-color);
  background-color: var(--primary-light);
  border-radius: 0 12px 12px 0;
}

.markdown-body :deep(blockquote p) {
  margin-bottom: 0;
  color: var(--text-secondary);
}

.markdown-body :deep(code) {
  font-family: var(--font-mono);
  font-size: 13px;
  padding: 2px 6px;
  background-color: var(--bg-tertiary);
  border-radius: 6px;
  color: #e11d48;
}

.markdown-body :deep(pre) {
  margin: 12px 0;
  padding: 16px;
  background-color: #1e293b;
  border-radius: 12px;
  overflow-x: auto;
}

.markdown-body :deep(pre code) {
  padding: 0;
  background: none;
  color: #e2e8f0;
  font-size: 13px;
  line-height: 1.6;
}

.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
}

.markdown-body :deep(th) {
  background-color: var(--bg-tertiary);
  padding: 10px 12px;
  text-align: left;
  font-weight: 600;
  font-size: 14px;
  border: 1px solid var(--border-color);
}

.markdown-body :deep(table) {
  border-radius: 12px;
  overflow: hidden;
}

.markdown-body :deep(td) {
  padding: 8px 12px;
  font-size: 14px;
  border: 1px solid var(--border-color);
}

.markdown-body :deep(tr:nth-child(even)) {
  background-color: var(--bg-secondary);
}

.markdown-body :deep(a) {
  color: var(--primary-color);
  text-decoration: none;
}

.markdown-body :deep(a:hover) {
  text-decoration: underline;
}

.markdown-body :deep(hr) {
  border: none;
  border-top: 1px solid var(--border-color);
  margin: 24px 0;
}

.markdown-body :deep(img) {
  max-width: 100%;
  border-radius: 12px;
  margin: 12px 0;
}

.markdown-body :deep(strong) {
  font-weight: 600;
}

/* ============================================
   底部栏
   ============================================ */
.modal-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  border-top: 1px solid var(--border-color);
  flex-shrink: 0;
}

.footer-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-idle {
  background-color: var(--text-muted);
}

.status-loading {
  background-color: var(--primary-color);
  animation: pulse 1.5s ease infinite;
}

.status-completed {
  background-color: var(--success-color);
}

.status-error {
  background-color: var(--error-color);
}

.status-text {
  font-size: 13px;
  color: var(--text-secondary);
}

.footer-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.footer-tip {
  font-size: 12px;
  color: var(--text-muted);
}

.action-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background-color: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  font-size: 13px;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
}

.action-button:hover {
  background-color: var(--border-color);
  color: var(--text-primary);
}

/* ============================================
   响应式设计
   ============================================ */

/* 平板设备 */
@media (max-width: 768px) {
  .modal-container {
    width: 95vw;
    height: 95vh;
    background-color: #ffffff;
    border-radius: 16px;
  }

  .modal-header {
    padding: 16px 20px;
  }

  .progress-section {
    padding: 12px 20px;
  }

  .content-section {
    padding: 20px;
  }

  .modal-footer {
    padding: 12px 20px;
  }

  .header-title {
    font-size: 16px;
  }

  .loading-stages {
    gap: 0;
  }

  .stage-connector {
    width: 40px;
  }
}

/* 手机设备 */
@media (max-width: 480px) {
  .modal-container {
    width: 100vw;
    height: 100vh;
    border-radius: 0;
    background-color: #ffffff;
  }

  .modal-header h2 {
    font-size: 16px;
  }

  .modal-header {
    padding: 12px 16px;
  }

  .progress-section {
    padding: 10px 16px;
  }

  .content-section {
    padding: 16px;
  }

  .modal-footer {
    padding: 10px 16px;
    flex-direction: column;
    gap: 8px;
  }

  .footer-right {
    width: 100%;
    justify-content: flex-end;
  }

  .header-title {
    font-size: 14px;
  }

  .stage-connector {
    width: 24px;
  }

  .stage-label {
    font-size: 10px;
  }

  .stage-dot {
    width: 28px;
    height: 28px;
    font-size: 11px;
  }

  .footer-tip {
    display: none;
  }

  .markdown-body :deep(h1) {
    font-size: 22px;
  }

  .markdown-body :deep(h2) {
    font-size: 18px;
  }
}
</style>