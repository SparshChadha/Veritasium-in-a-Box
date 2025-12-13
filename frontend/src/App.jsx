import { useEffect, useRef, useState } from 'react'
// eslint-disable-next-line no-unused-vars
import { motion, AnimatePresence, LayoutGroup } from 'framer-motion'
import { Zap } from 'lucide-react'
import HeroSection from './components/HeroSection'
import StudioView from './components/StudioView'
import AuthView from './components/AuthView'

// In production (nginx), we proxy /api -> backend, so default to '/api'
// In local dev, set VITE_API_BASE_URL=http://localhost:8000
const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api'

function App() {
  const [currentView, setCurrentView] = useState('hero') // 'hero' | 'studio' | 'auth'
  const [generatedContent, setGeneratedContent] = useState(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [taskId, setTaskId] = useState(null)
  const [pipeline, setPipeline] = useState(null)
  const pollRef = useRef(null)

  const handleGenerate = async (topic) => {
    // reset state
    if (pollRef.current) {
      clearInterval(pollRef.current)
      pollRef.current = null
    }
    setGeneratedContent(null)
    setPipeline(null)
    setTaskId(null)
    setIsGenerating(true)
    setCurrentView('studio')

    // Start backend pipeline
    const res = await fetch(`${API_BASE}/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        topic,
        tts_engine: 'elevenlabs',
        generate_video: true,
      }),
    })

    if (!res.ok) {
      const text = await res.text().catch(() => '')
      setIsGenerating(false)
      setPipeline({ status: 'failed', error: `Backend error: ${res.status} ${text}` })
      return
    }

    const data = await res.json()
    setTaskId(data.task_id)
  }

  useEffect(() => {
    if (!taskId) return

    const poll = async () => {
      try {
        const res = await fetch(`${API_BASE}/status/${taskId}`)
        if (!res.ok) throw new Error(`status ${res.status}`)
        const status = await res.json()
        setPipeline(status)

        if (status.status === 'failed') {
          setIsGenerating(false)
          if (pollRef.current) clearInterval(pollRef.current)
          pollRef.current = null
          return
        }

        if (status.status === 'completed') {
          if (pollRef.current) clearInterval(pollRef.current)
          pollRef.current = null

          const files = status.files || {}
          const title = `The Truth About ${status.topic || 'Your Topic'}`

          // Fetch final script markdown (best UX) — fallback to empty if not available
          let scriptText = ''
          if (files.final_script) {
            const scriptRes = await fetch(`${API_BASE}/download/${encodeURI(files.final_script)}`)
            if (scriptRes.ok) scriptText = await scriptRes.text()
          }

          const audioUrl = files.tts_audio ? `${API_BASE}/download/${encodeURI(files.tts_audio)}` : null
          const videoUrl = files.video ? `${API_BASE}/download/${encodeURI(files.video)}` : null

          setGeneratedContent({
            title,
            script: scriptText,
            audioUrl,
            videoUrl,
            stats: { views: '—', likes: '—', duration: '—' },
          })
          setIsGenerating(false)
        }
      } catch {
        setPipeline((p) => ({ ...(p || {}), status: 'running', error: null }))
      }
    }

    poll()
    pollRef.current = setInterval(poll, 1500)

    return () => {
      if (pollRef.current) clearInterval(pollRef.current)
      pollRef.current = null
    }
  }, [taskId])

  const handleBackToHero = () => {
    setCurrentView('hero')
    setGeneratedContent(null)
    setIsGenerating(false)
    setTaskId(null)
    setPipeline(null)
    if (pollRef.current) {
      clearInterval(pollRef.current)
      pollRef.current = null
    }
  }

  return (
    <div className="min-h-screen relative overflow-x-hidden">
      {/* Subtle animated gradient background */}
      <div className="pointer-events-none fixed inset-0 -z-10">
        <div className="moving-aurora" />
      </div>
      {/* Minimal Clean Navbar */}
      <motion.nav
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6 }}
        className="fixed top-0 left-0 right-0 z-50 backdrop-blur-sm"
      >
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <motion.div className="flex items-center gap-2" whileHover={{ scale: 1.02 }}>
              <Zap className="w-5 h-5 text-blue-600" />
              <span className="text-lg font-semibold tracking-tight text-gray-900">
                Element of Truth
              </span>
            </motion.div>

            <div className="flex items-center gap-3">
              <button
                className="px-4 py-2 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-900 text-sm font-medium transition-colors"
                onClick={() => setCurrentView('auth')}
              >
                Log in
              </button>
              <button
                className="px-4 py-2 rounded-full bg-gray-900 text-white hover:bg-gray-800 text-sm font-medium transition-colors"
                onClick={() => setCurrentView('auth')}
              >
                Get started
              </button>
            </div>
          </div>
        </div>
      </motion.nav>

      {/* Main Content */}
      <div className="pt-20">
        <LayoutGroup>
          <AnimatePresence mode="wait">
            {currentView === 'hero' ? (
              <motion.div
                key="hero"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.5 }}
              >
                <HeroSection onGenerate={handleGenerate} />
              </motion.div>
            ) : currentView === 'studio' ? (
              <motion.div
                key="studio"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 1.05 }}
                transition={{ duration: 0.5 }}
              >
                <StudioView
                  content={generatedContent}
                  isGenerating={isGenerating}
                  pipeline={pipeline}
                  onBack={handleBackToHero}
                />
              </motion.div>
            ) : (
              <motion.div
                key="auth"
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -12 }}
                transition={{ duration: 0.4 }}
              >
                <AuthView onClose={() => setCurrentView('hero')} onSuccess={() => setCurrentView('hero')} />
              </motion.div>
            )}
          </AnimatePresence>
        </LayoutGroup>
      </div>
    </div>
  )
}

export default App
