import { useState } from 'react'
// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion'
import { Play, Copy, Send, Eye, ThumbsUp, Clock, User, ArrowLeft } from 'lucide-react'
import AgentStatus from './AgentStatus'

const StudioView = ({ content, isGenerating, pipeline, onBack }) => {
  const [refineInput, setRefineInput] = useState('')

  const handleCopyScript = () => {
    if (content?.script) {
      navigator.clipboard.writeText(content.script)
      // You could add a toast notification here
    }
  }

  const handleRefine = () => {
    if (refineInput.trim()) {
      // Handle script refinement - would integrate with API
      console.log('Refining script:', refineInput)
      setRefineInput('')
    }
  }

  return (
    <div className="min-h-screen">
      {/* Back Button */}
      <motion.button
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        onClick={onBack}
        className="fixed top-24 left-6 z-40 flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 backdrop-blur-sm border border-gray-200 rounded-lg text-gray-900 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back</span>
      </motion.button>

      <div className="max-w-7xl mx-auto px-6 py-8 pt-24">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Column - Video Player */}
          <div className="lg:col-span-8">
            <motion.div
              layoutId="primary-surface"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="relative aspect-video bg-gray-100 rounded-xl overflow-hidden border border-gray-200 shadow-lg"
            >
              {isGenerating ? (
                <AgentStatus pipeline={pipeline} />
              ) : content ? (
                <>
                  {content.videoUrl ? (
                    <video
                      className="absolute inset-0 w-full h-full object-cover"
                      src={content.videoUrl}
                      controls
                    />
                  ) : content.audioUrl ? (
                    <div className="absolute inset-0 bg-gradient-to-br from-gray-50 via-gray-100 to-gray-200 flex items-center justify-center">
                      <div className="w-full max-w-md px-6 text-center">
                        <div className="mx-auto mb-4 w-14 h-14 rounded-2xl bg-gray-900 text-white grid place-items-center shadow-lg">
                          <Play className="w-6 h-6 ml-0.5" />
                        </div>
                        <div className="text-gray-900 font-montserrat font-semibold">Audio ready</div>
                        <div className="mt-2">
                          <audio className="w-full" src={content.audioUrl} controls />
                        </div>
                        <div className="mt-2 text-xs text-gray-500 font-montserrat">
                          Video is optional (requires WaveSpeed key). You can still listen to the generated narration.
                        </div>
                      </div>
                    </div>
                  ) : (
                    <>
                      {/* Video Thumbnail Placeholder */}
                      <div className="absolute inset-0 bg-gradient-to-br from-gray-50 via-gray-100 to-gray-200 flex items-center justify-center">
                        <div className="text-center">
                          <div className="w-32 h-32 mx-auto mb-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center shadow-lg">
                            <Play className="w-16 h-16 text-white ml-2" />
                          </div>
                          <p className="text-gray-600 font-montserrat">Generated output will appear here</p>
                        </div>
                      </div>
                    </>
                  )}
                </>
              ) : null}

              {/* Duration Badge */}
              {content && (
                <div className="absolute bottom-4 right-4 bg-gray-900 px-2 py-1 rounded text-xs font-montserrat text-white border border-gray-700">
                  {content.stats.duration}
                </div>
              )}
            </motion.div>

            {/* Video Info */}
            {content && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.3 }}
                className="mt-6"
              >
                <h1 className="text-2xl md:text-3xl font-cinzel font-bold text-gray-900 mb-4">
                  {content.title}
                </h1>

                <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center">
                      <User className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-montserrat font-semibold text-gray-900">Veritasium AI</h3>
                      <p className="text-gray-600 text-sm">1.5M subscribers</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 flex-wrap text-gray-700">
                    <div className="inline-flex items-center gap-2 px-3 py-2 rounded-full bg-gray-100 border border-gray-200">
                      <Eye className="w-5 h-5" />
                      <span className="font-montserrat">{content.stats.views}</span>
                    </div>
                    <div className="inline-flex items-center gap-2 px-3 py-2 rounded-full bg-gray-100 border border-gray-200">
                      <ThumbsUp className="w-5 h-5" />
                      <span className="font-montserrat">{content.stats.likes}</span>
                    </div>
                    <div className="inline-flex items-center gap-2 px-3 py-2 rounded-full bg-gray-100 border border-gray-200">
                      <Clock className="w-5 h-5" />
                      <span className="font-montserrat">2 days ago</span>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </div>

          {/* Right Column - Script Viewer */}
          <div className="lg:col-span-4">
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="bg-white backdrop-blur-sm border border-gray-200 rounded-xl h-[calc(100vh-128px)] flex flex-col sticky top-24 shadow-lg"
            >
              {/* Script Header */}
              <div className="p-5 border-b border-gray-200">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-cinzel font-bold text-gray-900">Generated Script</h2>
                  <motion.button
                    onClick={handleCopyScript}
                    className="p-2 bg-gray-100 border border-gray-200 rounded-lg text-gray-700 hover:text-blue-600 hover:border-blue-400 transition-all duration-300"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Copy className="w-5 h-5" />
                  </motion.button>
                </div>
                <p className="text-sm text-gray-600 font-montserrat">
                  Professional screenplay format with scene markers and narration cues.
                </p>
              </div>

              {/* Script Content */}
              <div className="flex-1 p-5 overflow-y-auto">
                {content?.script ? (
                  <div className="font-montserrat text-gray-800 leading-relaxed whitespace-pre-wrap text-sm">
                    {content.script.split('\n').map((line, index) => {
                      if (line.startsWith('**') && line.endsWith('**')) {
                        return (
                          <div key={index} className="text-blue-600 font-semibold mb-3 mt-4">
                            {line.replace(/\*\*/g, '')}
                          </div>
                        )
                      } else if (line.startsWith('## ')) {
                        return (
                          <h3 key={index} className="text-lg font-cinzel font-bold text-gray-900 mb-3 mt-6">
                            {line.replace('## ', '')}
                          </h3>
                        )
                      } else if (line.startsWith('*[') && line.includes(']*')) {
                        return (
                          <div key={index} className="text-amber-600 italic mb-2 text-xs">
                            {line}
                          </div>
                        )
                      }
                      return <div key={index} className="mb-2">{line}</div>
                    })}
                  </div>
                ) : (
                  <div className="flex items-center justify-center h-full text-gray-500">
                    <p>Script will appear here after generation</p>
                  </div>
                )}
              </div>

              {/* Refine Script Input */}
              <div className="p-5 border-t border-gray-200">
                <form
                  className="flex space-x-3"
                  onSubmit={(e) => {
                    e.preventDefault()
                    handleRefine()
                  }}
                >
                  <input
                    type="text"
                    value={refineInput}
                    onChange={(e) => setRefineInput(e.target.value)}
                    placeholder="Refine this script... (e.g., 'Make the intro funnier')"
                    className="flex-1 bg-gray-50 border border-gray-200 rounded-lg px-4 py-3 text-gray-900 placeholder-gray-400 outline-none focus:border-blue-400 transition-all duration-300 font-montserrat text-sm"
                  />
                  <motion.button
                    type="submit"
                    disabled={!refineInput.trim()}
                    className={`p-3 rounded-lg transition-all duration-300 ${
                      refineInput.trim()
                        ? 'bg-blue-600 text-white shadow-md'
                        : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                    }`}
                    whileHover={refineInput.trim() ? { scale: 1.05 } : {}}
                    whileTap={refineInput.trim() ? { scale: 0.95 } : {}}
                  >
                    <Send className="w-5 h-5" />
                  </motion.button>
                </form>
                <p className="text-xs text-gray-500 mt-2 font-montserrat">
                  AI will regenerate the script based on your feedback
                </p>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default StudioView
