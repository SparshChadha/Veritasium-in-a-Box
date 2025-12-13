import { useMemo } from 'react'
// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion'
import { CheckCircle2, Clock3, AlertTriangle, BookOpen, GraduationCap, Film, AudioLines, Video } from 'lucide-react'

const STEP_ORDER = ['research', 'draft', 'director', 'tts', 'video']

const STEP_ICONS = {
  research: BookOpen,
  draft: GraduationCap,
  director: Film,
  tts: AudioLines,
  video: Video,
}

function normalizeStepStatus(s) {
  if (!s) return 'pending'
  return String(s).toLowerCase()
}

export default function AgentStatus({ pipeline }) {
  const overall = pipeline?.status || 'running'
  const currentStep = pipeline?.current_step || 'running'
  const updatedAt = pipeline?.updated_at

  const ordered = useMemo(() => {
    const steps = pipeline?.steps || {}
    return STEP_ORDER.map((key) => {
      const meta = steps[key] || {}
      return {
        key,
        label: meta.label || key,
        status: normalizeStepStatus(meta.status),
      }
    })
  }, [pipeline?.steps])

  const completedCount = ordered.filter((s) => s.status === 'completed' || s.status === 'skipped').length
  const percent = Math.round((completedCount / Math.max(ordered.length, 1)) * 100)

  return (
    <div className="absolute inset-0 flex items-center justify-center">
      {/* Glass overlay */}
      <div className="absolute inset-0 bg-white/70 backdrop-blur-sm" />

      <div className="relative z-10 w-full max-w-2xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-2xl bg-white border border-gray-200 shadow-xl p-6"
        >
          <div className="flex items-start justify-between gap-4">
            <div>
              <div className="text-sm font-montserrat text-gray-500">Generating</div>
              <div className="text-2xl font-cinzel font-bold text-gray-900">Pipeline progress</div>
              <div className="mt-1 text-sm font-montserrat text-gray-600">
                {overall === 'failed' ? 'Failed' : overall === 'completed' ? 'Completed' : 'Working…'} • step: {currentStep}
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm font-montserrat text-gray-500">Progress</div>
              <div className="text-xl font-semibold text-gray-900">{percent}%</div>
              {updatedAt && (
                <div className="text-xs font-montserrat text-gray-500 mt-1">Updated {new Date(updatedAt).toLocaleTimeString()}</div>
              )}
            </div>
          </div>

          <div className="mt-5 space-y-3">
            {ordered.map((s) => {
              const Icon = STEP_ICONS[s.key] || Clock3
              const isRunning = s.status === 'running'
              const isDone = s.status === 'completed'
              const isSkipped = s.status === 'skipped'
              const isFailed = s.status === 'failed'

              return (
                <div
                  key={s.key}
                  className={`flex items-center gap-3 rounded-xl border px-4 py-3 ${
                    isFailed
                      ? 'border-red-200 bg-red-50'
                      : isDone || isSkipped
                      ? 'border-green-200 bg-green-50'
                      : isRunning
                      ? 'border-blue-200 bg-blue-50'
                      : 'border-gray-200 bg-gray-50'
                  }`}
                >
                  <div className="w-8 h-8 rounded-lg bg-white border border-gray-200 grid place-items-center">
                    {isDone || isSkipped ? (
                      <CheckCircle2 className="w-5 h-5 text-green-600" />
                    ) : isFailed ? (
                      <AlertTriangle className="w-5 h-5 text-red-600" />
                    ) : (
                      <Icon className={`w-5 h-5 ${isRunning ? 'text-blue-600 animate-pulse' : 'text-gray-500'}`} />
                    )}
                  </div>
                  <div className="flex-1">
                    <div className="font-montserrat font-medium text-gray-900">{s.label}</div>
                    <div className="text-xs font-montserrat text-gray-600">
                      {isDone ? 'Complete' : isSkipped ? 'Skipped' : isFailed ? 'Failed' : isRunning ? 'Running…' : 'Queued'}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>

          {pipeline?.error && (
            <div className="mt-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 font-montserrat">
              {pipeline.error}
            </div>
          )}

          <div className="mt-4 h-2 rounded-full bg-gray-100 overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-blue-600 to-purple-600"
              initial={{ width: '0%' }}
              animate={{ width: `${percent}%` }}
              transition={{ duration: 0.4, ease: 'easeOut' }}
            />
          </div>
        </motion.div>
      </div>
    </div>
  )
}
