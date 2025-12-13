import { useState, useRef } from 'react'
// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion'
import { ArrowUp, Paperclip } from 'lucide-react'

const HeroSection = ({ onGenerate }) => {
  const [inputValue, setInputValue] = useState('')
  const [isFocused, setIsFocused] = useState(false)
  const inputRef = useRef(null)
  const formRef = useRef(null)

  const suggestionChips = [
    "Physics of Time",
    "Quantum Entanglement",
    "Black Hole Mysteries",
    "The Big Bang Theory"
  ]

  const handleChipClick = (suggestion) => {
    setInputValue(suggestion)
    inputRef.current?.focus()
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (inputValue.trim()) {
      onGenerate(inputValue.trim())
    }
  }

  return (
    <div className="min-h-[calc(100vh-80px)] flex items-center justify-center relative overflow-hidden">
      {/* Content */}
      <div className="relative z-10 w-full max-w-4xl mx-auto px-6 pb-16">
        <div className="text-center">
          {/* Badge (Lovable-style) */}
          <motion.a
            href="#"
            onClick={(e) => e.preventDefault()}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-100 border border-gray-200 text-xs text-gray-700 hover:bg-gray-200 transition-colors"
          >
            <span className="px-1.5 py-0.5 rounded-full bg-blue-600 text-white text-xs font-medium">New</span>
            <span>AI-powered content generation</span>
            <span className="opacity-60">→</span>
          </motion.a>

          {/* Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="mt-8 text-5xl md:text-7xl font-bold tracking-tight leading-tight"
          >
            <span className="text-gray-900">Create </span>
            <span className="bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent">
              Educational Videos
            </span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="mt-6 text-lg md:text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed"
          >
            Enter a topic and let AI research, write, and produce a Veritasium-style explainer video
          </motion.p>
        </div>

        {/* Minimalist Prompt Input (Lovable-style) */}
        <motion.form
          ref={formRef}
          onSubmit={handleSubmit}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-12"
        >
          <div className="mx-auto w-full max-w-3xl">
            <motion.div
              layoutId="primary-surface"
              className={`rounded-2xl border bg-white backdrop-blur-sm transition-all duration-300 shadow-sm ${
                isFocused ? 'border-blue-400 shadow-lg shadow-blue-500/10' : 'border-gray-200'
              }`}
            >
              <div className="p-4">
                <textarea
                  ref={inputRef}
                  rows={1}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={(e) => {
                    // Chat-style UX: Enter submits, Shift+Enter adds a newline.
                    // Also avoid interfering with IME composition.
                    if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) {
                      e.preventDefault()
                      formRef.current?.requestSubmit()
                    }
                  }}
                  onFocus={() => setIsFocused(true)}
                  onBlur={() => setIsFocused(false)}
                  placeholder="Ask Element of Truth to create a science video..."
                  className="w-full resize-none bg-transparent text-gray-900 placeholder:text-gray-400 outline-none text-base leading-relaxed"
                />

                <div className="mt-3 flex items-center justify-between gap-3">
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      className="h-8 w-8 grid place-items-center rounded-lg hover:bg-gray-100 text-gray-500 hover:text-gray-900 transition"
                      title="Attach"
                    >
                      <Paperclip className="w-4 h-4" />
                    </button>
                  </div>

                  <button
                    type="submit"
                    disabled={!inputValue.trim()}
                    className={`h-9 w-9 grid place-items-center rounded-full transition-all ${
                      inputValue.trim()
                        ? 'bg-gray-900 text-white hover:bg-gray-800'
                        : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                    }`}
                    title="Generate"
                  >
                    <ArrowUp className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Suggestion chips */}
          <div className="mt-4 flex flex-wrap justify-center gap-2">
            {suggestionChips.map((suggestion) => (
              <button
                key={suggestion}
                type="button"
                onClick={() => handleChipClick(suggestion)}
                className="px-3 py-1.5 rounded-full bg-gray-100 hover:bg-gray-200 border border-gray-200 hover:border-gray-300 text-sm text-gray-700 transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </motion.form>
      </div>
    </div>
  )
}

export default HeroSection
