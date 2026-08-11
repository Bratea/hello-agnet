<template>
  <div class="app-container">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="bg-circle bg-circle-1"></div>
      <div class="bg-circle bg-circle-2"></div>
      <div class="bg-circle bg-circle-3"></div>
    </div>

    <div class="app-content">
      <!-- 头部区域 -->
      <header class="app-header">
        <div class="header-brand">
          <div class="brand-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.35-4.35"></path>
              <path d="M11 8v6"></path>
              <path d="M8 11h6"></path>
            </svg>
          </div>
          <div class="brand-text">
            <h1 class="brand-title">深度研究助手</h1>
            <p class="brand-subtitle">Deep Research Assistant</p>
          </div>
        </div>
      </header>

      <!-- 主内容 -->
      <main class="app-main">
        <div class="search-card">
          <div class="card-header">
            <h2 class="card-title">开始一次深度研究</h2>
            <p class="card-desc">输入研究主题，AI 将自动规划任务、搜索资料并生成结构化报告</p>
          </div>

          <div class="search-form">
            <div class="input-wrapper">
              <div class="input-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.35-4.35"></path>
                </svg>
              </div>
              <input
                ref="inputRef"
                v-model="topic"
                type="text"
                class="search-input"
                placeholder="例如：Datawhale 社区的历史与发展"
                @keydown.enter="handleStartResearch"
                :disabled="isResearching"
              />
              <button
                v-if="topic"
                class="input-clear"
                @click="topic = ''"
                :disabled="isResearching"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M18 6 6 18"></path>
                  <path d="m6 6 12 12"></path>
                </svg>
              </button>
            </div>

            <button
              class="search-button"
              :class="{ 'searching': isResearching }"
              :disabled="!topic.trim() || isResearching"
              @click="handleStartResearch"
            >
              <template v-if="isResearching">
                <div class="btn-spinner"></div>
                <span>研究中...</span>
              </template>
              <template v-else>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 2v4"></path>
                  <path d="m16.24 7.76 2.12-2.12"></path>
                  <path d="M22 12h-4"></path>
                  <path d="m16.24 16.24 2.12 2.12"></path>
                  <path d="M12 22v-4"></path>
                  <path d="m5.64 17.64 2.12-2.12"></path>
                  <path d="M6 12H2"></path>
                  <path d="m5.64 6.36 2.12 2.12"></path>
                </svg>
                <span>开始深度研究</span>
              </template>
            </button>
          </div>

          <!-- 示例主题 -->
          <div class="examples">
            <span class="examples-label">试试这些主题：</span>
            <div class="example-tags">
              <button
                v-for="example in exampleTopics"
                :key="example"
                class="example-tag"
                :disabled="isResearching"
                @click="selectExample(example)"
              >
                {{ example }}
              </button>
            </div>
          </div>
        </div>

        <!-- 功能介绍 -->
        <div class="features">
          <div class="feature-item">
            <div class="feature-icon feature-icon-plan">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <path d="M3 9h18"></path>
                <path d="M9 21V9"></path>
              </svg>
            </div>
            <div class="feature-text">
              <h3>智能规划</h3>
              <p>自动将研究主题分解为多个子任务，明确搜索方向</p>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon feature-icon-search">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
              </svg>
            </div>
            <div class="feature-text">
              <h3>多源搜索</h3>
              <p>整合多种搜索引擎结果，确保信息全面准确</p>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon feature-icon-report">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <path d="M16 13H8"></path>
                <path d="M16 17H8"></path>
                <path d="M10 9H8"></path>
              </svg>
            </div>
            <div class="feature-text">
              <h3>结构化报告</h3>
              <p>生成 Markdown 格式的研究报告，包含来源引用</p>
            </div>
          </div>
        </div>
      </main>

      <!-- 页脚 -->
      <footer class="app-footer">
        <p>深度研究助手 &mdash; 基于 AI Agent 的自动化研究工具</p>
      </footer>
    </div>

    <!-- 研究模态框 -->
    <ResearchModal
      :is-open="isModalOpen"
      :research-topic="currentTopic"
      @close="handleClose"
      @retry="handleRetry"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ResearchModal from '@/components/ResearchModal.vue'

const topic = ref('')
const currentTopic = ref('')
const isModalOpen = ref(false)
const isResearching = ref(false)
const inputRef = ref<HTMLInputElement | null>(null)

const exampleTopics = [
  'Datawhale 社区的历史与发展',
  'AutoGPT 的原理与应用',
  'React 19 的新特性',
  '大语言模型微调技术综述'
]

const selectExample = (example: string) => {
  topic.value = example
  startResearch(example)
}

const handleStartResearch = () => {
  const trimmed = topic.value.trim()
  if (!trimmed) return
  startResearch(trimmed)
}

const startResearch = (topicText: string) => {
  currentTopic.value = topicText
  isResearching.value = true
  isModalOpen.value = true
}

const handleClose = () => {
  isModalOpen.value = false
  isResearching.value = false
}

const handleRetry = (topicText: string) => {
  // 关闭后重新打开，ResearchModal 的 watch 会自动触发重试
  isModalOpen.value = false
  setTimeout(() => {
    isResearching.value = true
    isModalOpen.value = true
  }, 100)
}
</script>

<style scoped>
/* ============================================
   页面容器
   ============================================ */
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

/* ============================================
   背景装饰
   ============================================ */
.bg-decoration {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.bg-circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.3;
}

.bg-circle-1 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(74, 108, 247, 0.15), transparent 70%);
  top: -200px;
  right: -200px;
  animation: float 20s ease-in-out infinite;
}

.bg-circle-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.1), transparent 70%);
  bottom: -100px;
  left: -100px;
  animation: float 25s ease-in-out infinite reverse;
}

.bg-circle-3 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.08), transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: float 15s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.05);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.95);
  }
}

/* ============================================
   内容
   ============================================ */
.app-content {
  position: relative;
  z-index: 1;
  flex: 1;
  display: flex;
  flex-direction: column;
  max-width: 800px;
  width: 100%;
  margin: 0 auto;
  padding: 0 24px;
}

/* ============================================
   头部
   ============================================ */
.app-header {
  padding: 48px 0 24px;
  text-align: center;
  animation: slideUp 0.6s ease;
}

.header-brand {
  display: inline-flex;
  align-items: center;
  gap: 16px;
}

.brand-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, var(--primary-color), #818cf8);
  color: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(74, 108, 247, 0.3);
}

.brand-text {
  text-align: left;
}

.brand-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}

.brand-subtitle {
  font-size: 14px;
  color: var(--text-muted);
  margin-top: 2px;
}

/* ============================================
   主内容
   ============================================ */
.app-main {
  flex: 1;
  animation: slideUp 0.6s ease 0.1s both;
}

/* ============================================
   搜索卡片
   ============================================ */
.search-card {
  background-color: var(--bg-primary);
  border-radius: 20px;
  box-shadow: var(--shadow-md);
  padding: 32px;
  margin-bottom: 32px;
  border: 1px solid var(--border-color);
}

.card-header {
  margin-bottom: 24px;
  text-align: center;
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.card-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* ============================================
   搜索表单
   ============================================ */
.search-form {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.input-wrapper {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 14px;
  display: flex;
  align-items: center;
  color: var(--text-muted);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 12px 40px 12px 44px;
  font-size: 15px;
  color: var(--text-primary);
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  outline: none;
  transition: all var(--transition-fast);
}

.search-input::placeholder {
  color: var(--text-muted);
}

.search-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(74, 108, 247, 0.1);
  background-color: var(--bg-primary);
}

.search-input:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.input-clear {
  position: absolute;
  right: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  background: none;
  color: var(--text-muted);
  border-radius: 50%;
  transition: all var(--transition-fast);
}

.input-clear:hover {
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
}

.search-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  background: linear-gradient(135deg, #4a6cf7, #6366f1);
  color: #ffffff;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.3px;
  white-space: nowrap;
  transition: all var(--transition-fast);
  box-shadow: 0 4px 14px rgba(74, 108, 247, 0.35);
}

.search-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(74, 108, 247, 0.4);
}

.search-button:active:not(:disabled) {
  transform: translateY(0);
}

.search-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #94a3b8;
  box-shadow: none;
}

.search-button.searching {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

/* ============================================
   示例主题
   ============================================ */
.examples {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.examples-label {
  font-size: 13px;
  color: var(--text-muted);
  white-space: nowrap;
}

.example-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.example-tag {
  padding: 6px 14px;
  font-size: 13px;
  color: var(--text-secondary);
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.example-tag:hover:not(:disabled) {
  color: var(--primary-color);
  border-color: var(--primary-color);
  background-color: var(--primary-light);
}

.example-tag:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ============================================
   功能介绍
   ============================================ */
.features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 48px;
}

.feature-item {
  background-color: var(--bg-primary);
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  border: 1px solid var(--border-color);
  transition: all var(--transition-normal);
  animation: slideUp 0.6s ease 0.2s both;
}

.feature-item:nth-child(2) {
  animation-delay: 0.3s;
}

.feature-item:nth-child(3) {
  animation-delay: 0.4s;
}

.feature-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.feature-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 14px;
  margin-bottom: 16px;
}

.feature-icon-plan {
  background-color: #e8ecff;
  color: #4a6cf7;
}

.feature-icon-search {
  background-color: #ede9fe;
  color: #8b5cf6;
}

.feature-icon-report {
  background-color: #d1fae5;
  color: #10b981;
}

.feature-text h3 {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.feature-text p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* ============================================
   页脚
   ============================================ */
.app-footer {
  text-align: center;
  padding: 24px 0;
  margin-top: auto;
}

.app-footer p {
  font-size: 13px;
  color: var(--text-muted);
}

/* ============================================
   响应式设计
   ============================================ */

/* 平板设备 */
@media (max-width: 768px) {
  .app-content {
    padding: 0 16px;
  }

  .app-header {
    padding: 32px 0 20px;
  }

  .brand-icon {
    width: 48px;
    height: 48px;
  }

  .brand-title {
    font-size: 24px;
  }

  .search-card {
    padding: 24px;
  }

  .search-form {
    flex-direction: column;
  }

  .search-button {
    justify-content: center;
    padding: 12px 20px;
    width: 100%;
  }

  .features {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .feature-item {
    display: flex;
    align-items: center;
    text-align: left;
    gap: 16px;
    padding: 16px 20px;
  }

  .feature-icon {
    margin-bottom: 0;
    flex-shrink: 0;
  }

  .examples {
    flex-direction: column;
    align-items: flex-start;
  }
}

/* 手机设备 */
@media (max-width: 480px) {
  .app-header {
    padding: 24px 0 16px;
  }

  .brand-icon {
    width: 40px;
    height: 40px;
  }

  .brand-icon svg {
    width: 24px;
    height: 24px;
  }

  .brand-title {
    font-size: 20px;
  }

  .brand-subtitle {
    font-size: 12px;
  }

  .search-card {
    padding: 20px 16px;
  }

  .card-title {
    font-size: 18px;
  }

  .card-desc {
    font-size: 13px;
  }

  .example-tags {
    gap: 6px;
  }

  .example-tag {
    font-size: 12px;
    padding: 5px 12px;
  }
}
</style>