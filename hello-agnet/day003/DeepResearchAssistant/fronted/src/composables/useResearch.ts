import { ref } from 'vue'

/**
 * SSE 研究事件数据类型
 */
export interface ProgressEvent {
  type: 'progress'
  stage: 'planning' | 'executing' | 'reporting' | 'completed'
  percentage: number
  text: string
}

export interface PlanEvent {
  type: 'plan'
  data: Array<{
    id: string
    title: string
    intent: string
    query: string
  }>
}

export interface TaskSummaryEvent {
  type: 'task_summary'
  task_id: string
  summary: string
}

export interface ReportEvent {
  type: 'report'
  data: string
}

export interface ErrorEvent {
  type: 'error'
  message: string
}

export type ResearchEvent =
  | ProgressEvent
  | PlanEvent
  | TaskSummaryEvent
  | ReportEvent
  | ErrorEvent

export function useResearch() {
  const isLoading = ref(false)
  const progressPercentage = ref(0)
  const progressText = ref('')
  const markdownContent = ref('')
  const error = ref<string | null>(null)
  const currentStage = ref<'planning' | 'executing' | 'reporting' | 'completed' | ''>('')

  let eventSource: EventSource | null = null

  /**
   * 开始深度研究
   * @param topic 研究主题
   * @param onPlan 规划完成回调（可选）
   * @param onTaskSummary 每项任务总结回调（可选）
   */
  const startResearch = (
    topic: string,
    onPlan?: (data: PlanEvent['data']) => void,
    onTaskSummary?: (taskId: string, summary: string) => void
  ) => {
    // 重置状态
    isLoading.value = true
    error.value = null
    progressPercentage.value = 0
    progressText.value = '准备中...'
    markdownContent.value = ''
    currentStage.value = 'planning'

    // 关闭之前的连接
    if (eventSource) {
      eventSource.close()
    }

    const encodedTopic = encodeURIComponent(topic)
    eventSource = new EventSource(`/api/research?topic=${encodedTopic}`)

    eventSource.onmessage = (event) => {
      try {
        const data: ResearchEvent = JSON.parse(event.data)

        switch (data.type) {
          case 'progress':
            progressPercentage.value = data.percentage
            progressText.value = data.text
            currentStage.value = data.stage

            if (data.stage === 'completed') {
              eventSource?.close()
              isLoading.value = false
            }
            break

          case 'plan':
            onPlan?.(data.data)
            break

          case 'task_summary':
            // 追加任务总结到 Markdown
            markdownContent.value += `\n\n## 任务 ${data.task_id}\n\n${data.summary}`
            onTaskSummary?.(data.task_id, data.summary)
            break

          case 'report':
            // 显示最终报告
            markdownContent.value = data.data
            break

          case 'error':
            error.value = data.message
            eventSource?.close()
            isLoading.value = false
            break
        }
      } catch (e) {
        console.error('解析 SSE 数据失败:', e)
      }
    }

    eventSource.onerror = () => {
      // EventSource 会在连接断开时自动重连
      // 如果已经完成或出错，不处理
      if (!isLoading.value) return

      console.error('SSE 连接错误')
      error.value = '连接中断，正在重试...'
      // 不立即关闭，让 EventSource 自动重连
    }
  }

  /**
   * 停止研究
   */
  const stopResearch = () => {
    if (eventSource) {
      eventSource.close()
      eventSource = null
    }
    isLoading.value = false
  }

  /**
   * 重置状态
   */
  const reset = () => {
    stopResearch()
    isLoading.value = false
    progressPercentage.value = 0
    progressText.value = ''
    markdownContent.value = ''
    error.value = null
    currentStage.value = ''
  }

  return {
    isLoading,
    progressPercentage,
    progressText,
    markdownContent,
    error,
    currentStage,
    startResearch,
    stopResearch,
    reset
  }
}