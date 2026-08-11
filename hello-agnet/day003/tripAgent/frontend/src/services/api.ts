import axios from 'axios'
import type { TripPlan, TripPlanRequest } from '@/types'

// 创建 Axios 实例
// 开发环境通过 vite.config.ts 的 proxy 把 /api 转发到后端 http://localhost:8000，
// 因此这里使用相对路径即可，避免跨域问题。
const api = axios.create({
  baseURL: '/api',
  timeout: 300000, // 5 分钟超时：生成旅行计划需并发调用多个 Agent + 高德 MCP，可能耗时较久
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器：打印日志、统一附加 token 等
api.interceptors.request.use(
  (config) => {
    console.log('发送请求：', config)
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器：统一处理错误
api.interceptors.response.use(
  (response) => {
    console.log('收到响应：', response)
    return response
  },
  (error) => {
    console.error('请求失败：', error)
    return Promise.reject(error)
  }
)

// 生成旅行计划 —— 前端调用后端的唯一入口
export const generateTripPlan = async (request: TripPlanRequest): Promise<TripPlan> => {
  const response = await api.post<TripPlan>('/trip/plan', request)
  return response.data
}

export default api
