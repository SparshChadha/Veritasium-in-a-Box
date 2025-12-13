import { useState } from 'react'
import { motion } from 'framer-motion'
import { Play, Copy, Send, Eye, ThumbsUp, Clock, User, ArrowLeft } from 'lucide-react'
import AgentStatus from './AgentStatus'

const StudioView = ({ content, isGenerating, onBack }) => {
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
    <div className="min-h-screen bg-dark-slate">
      {/* Back Button */}
      <motion.button
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        onClick={onBack}
        className="fixed top-24 left-6 z-40 flex items-center space-x-2 px-4 py-2 bg-glass backdrop-blur-sm border border-glass-border rounded-lg text-gray-300 hover:text-white hover:border-neon-cyan transition-all duration-300"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <ArrowLeft className="w-4 h-4" />
        <span className="font-montserrat">Back to Search</span>
      </motion.button>

      <div className="max-w-7xl mx-auto px-6 py-8 pt-24">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Column - Video Player */}
          <div className="lg:col-span-8">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="relative aspect-video bg-black rounded-xl overflow-hidden cinematic-shadow border border-white/10"
            >
              {isGenerating ? (
                <AgentStatus />
              ) : content ? (
                <>
                  {/* Video Thumbnail Placeholder */}
                  <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-950 to-black flex items-center justify-center">
                    <div className="text-center">
                      <div className="w-32 h-32 mx-auto mb-4 bg-gradient-to-r from-neon-blue to-neon-cyan rounded-full flex items-center justify-center shadow-[0_0_40px_rgba(0,242,254,0.25)]">
                        <Play className="w-16 h-16 text-black ml-2" />
                      </div>
                      <p className="text-gray-400 font-montserrat">Click to play generated video</p>
                    </div>
                  </div>

                  {/* Play Button Overlay */}
                  <motion.button
                    className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-40 hover:bg-opacity-30 transition-all duration-300"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <div className="w-20 h-20 bg-neon-cyan rounded-full flex items-center justify-center shadow-[0_0_30px_rgba(0,242,254,0.35)]">
                      <Play className="w-8 h-8 text-black ml-1" />
                    </div>
                  </motion.button>
                </>
              ) : null}

              {/* Duration Badge */}
              {content && (
                <div className="absolute bottom-4 right-4 bg-black/80 px-2 py-1 rounded text-xs font-montserrat text-white border border-white/10">
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
                <h1 className="text-2xl md:text-3xl font-cinzel font-bold text-white mb-4">
                  {content.title}
                </h1>

                <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-neon-blue to-neon-cyan rounded-full flex items-center justify-center">
                      <User className="w-6 h-6 text-black" />
                    </div>
                    <div>
                      <h3 className="font-montserrat font-semibold text-white">Veritasium AI</h3>
                      <p className="text-gray-400 text-sm">1.5M subscribers</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 flex-wrap text-gray-300">
                    <div className="inline-flex items-center gap-2 px-3 py-2 rounded-full bg-white/5 border border-white/10">
                      <Eye className="w-5 h-5" />
                      <span className="font-montserrat">{content.stats.views}</span>
                    </div>
                    <div className="inline-flex items-center gap-2 px-3 py-2 rounded-full bg-white/5 border border-white/10">
                      <ThumbsUp className="w-5 h-5" />
                      <span className="font-montserrat">{content.stats.likes}</span>
                    </div>
                    <div className="inline-flex items-center gap-2 px-3 py-2 rounded-full bg-white/5 border border-white/10">
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
              className="bg-black/35 backdrop-blur-xl border border-white/10 rounded-xl h-[calc(100vh-128px)] flex flex-col sticky top-24 cinematic-shadow"
            >
              {/* Script Header */}
              <div className="p-5 border-b border-white/10">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-cinzel font-bold text-white">Generated Script</h2>
                  <motion.button
                    onClick={handleCopyScript}
                    className="p-2 bg-white/5 border border-white/10 rounded-lg text-gray-300 hover:text-neon-cyan hover:border-neon-cyan/50 transition-all duration-300"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Copy className="w-5 h-5" />
                  </motion.button>
                </div>
                <p className="text-sm text-gray-400 font-montserrat">
                  Professional screenplay format with scene markers and narration cues.
                </p>
              </div>

              {/* Script Content */}
              <div className="flex-1 p-5 overflow-y-auto">
                {content?.script ? (
                  <div className="font-montserrat text-gray-200/80 leading-relaxed whitespace-pre-wrap text-sm">
                    {content.script.split('\n').map((line, index) => {
                      if (line.startsWith('**') && line.endsWith('**')) {
                        return (
                          <div key={index} className="text-neon-cyan font-semibold mb-3 mt-4">
                            {line.replace(/\*\*/g, '')}
                          </div>
                        )
                      } else if (line.startsWith('## ')) {
                        return (
                          <h3 key={index} className="text-lg font-cinzel font-bold text-white mb-3 mt-6">
                            {line.replace('## ', '')}
                          </h3>
                        )
                      } else if (line.startsWith('*[') && line.includes(']*')) {
                        return (
                          <div key={index} className="text-yellow-300 italic mb-2 text-xs">
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
              <div className="p-5 border-t border-white/10">
                <div className="flex space-x-3">
                  <input
                    type="text"
                    value={refineInput}
                    onChange={(e) => setRefineInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleRefine()}
                    placeholder="Refine this script... (e.g., 'Make the intro funnier')"
                    className="flex-1 bg-black/30 border border-white/10 rounded-lg px-4 py-3 text-gray-200/80 placeholder-gray-400/60 outline-none focus:border-neon-cyan/60 transition-all duration-300 font-montserrat text-sm"
                  />
                  <motion.button
                    onClick={handleRefine}
                    disabled={!refineInput.trim()}
                    className={`p-3 rounded-lg transition-all duration-300 ${
                      refineInput.trim()
                        ? 'bg-neon-cyan text-black shadow-[0_0_18px_rgba(0,242,254,0.25)]'
                        : 'bg-white/10 text-gray-500 cursor-not-allowed'
                    }`}
                    whileHover={refineInput.trim() ? { scale: 1.05 } : {}}
                    whileTap={refineInput.trim() ? { scale: 0.95 } : {}}
                  >
                    <Send className="w-5 h-5" />
                  </motion.button>
                </div>
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
