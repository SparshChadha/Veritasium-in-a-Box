import { useState, useRef } from 'react'
import { motion } from 'framer-motion'
import { ArrowUp, Paperclip, Plus, Sparkles, Wand2 } from 'lucide-react'

const HeroSection = ({ onGenerate }) => {
  const [inputValue, setInputValue] = useState('')
  const [isFocused, setIsFocused] = useState(false)
  const inputRef = useRef(null)

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
    <div className="min-h-[calc(100vh-80px)] flex items-center justify-center relative overflow-hidden bg-dark-slate">
      {/* Background: Lovable-style moving gradient + cinematic overlays */}
      <div className="absolute inset-0">
        <div className="moving-aurora" />
        <div className="gradient-overlay" />
        <div className="vignette" />
        <div className="film-grain" />
      </div>

      {/* Content */}
      <div className="relative z-10 w-full max-w-5xl mx-auto px-6 pb-16">
        <div className="text-center">
          {/* Badge (Lovable-ish) */}
          <motion.a
            href="#"
            onClick={(e) => e.preventDefault()}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-black/35 border border-white/10 text-xs text-gray-200 backdrop-blur-md"
          >
            <span className="px-2 py-0.5 rounded-full bg-neon-blue/20 border border-neon-blue/30 text-neon-blue">New</span>
            <span className="opacity-80">ELEMENT OF TRUTH Studio is live</span>
            <span className="opacity-60">→</span>
          </motion.a>

          {/* Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9, delay: 0.1 }}
            className="mt-6 text-5xl md:text-7xl font-cinzel font-bold tracking-tight"
          >
            <span className="text-white/90">Uncover</span>{' '}
            <span className="bg-gradient-to-r from-neon-blue via-white to-neon-cyan bg-clip-text text-transparent neon-text">
              the Truth
            </span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9, delay: 0.2 }}
            className="mt-4 text-base md:text-xl text-gray-200/70 font-montserrat max-w-2xl mx-auto"
          >
            Ask a question. We’ll research, script, and produce a cinematic explainer — like a DreamWorks-grade science studio.
          </motion.p>
        </div>

        {/* Lovable-style Prompt Bar */}
        <motion.form
          onSubmit={handleSubmit}
          initial={{ opacity: 0, scale: 0.98, y: 18 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.25 }}
          className="mt-10"
        >
          <motion.div
            className="mx-auto w-full max-w-3xl rounded-2xl border bg-black/45 backdrop-blur-xl transition-[box-shadow,border-color] duration-500 ease-out"
            animate={
              isFocused
                ? {
                    boxShadow:
                      '0 25px 50px -12px rgba(0, 0, 0, 0.55), 0 0 0 1px rgba(0, 242, 254, 0.45), 0 0 28px rgba(0, 242, 254, 0.22), 0 0 70px rgba(79, 172, 254, 0.12)',
                    borderColor: 'rgba(0, 242, 254, 0.45)',
                  }
                : {
                    boxShadow:
                      '0 25px 50px -12px rgba(0, 0, 0, 0.55), 0 0 0 1px rgba(255, 255, 255, 0.10)',
                    borderColor: 'rgba(255, 255, 255, 0.10)',
                  }
            }
            transition={{ duration: 0.45, ease: [0.16, 1, 0.3, 1] }}
          >
            <div className="p-5 md:p-6">
              <textarea
                ref={inputRef}
                rows={2}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onFocus={() => setIsFocused(true)}
                onBlur={() => setIsFocused(false)}
                placeholder="What truth shall we uncover today?"
                className="w-full resize-none bg-transparent text-gray-100 placeholder:text-gray-400/70 outline-none text-base md:text-lg font-montserrat leading-relaxed"
              />

              <div className="mt-4 flex items-center justify-between gap-3">
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    className="h-9 w-9 grid place-items-center rounded-full bg-white/5 border border-white/10 text-gray-200/80 hover:text-white hover:border-white/20 transition"
                    title="New"
                  >
                    <Plus className="w-4 h-4" />
                  </button>
                  <button
                    type="button"
                    className="h-9 px-3 inline-flex items-center gap-2 rounded-full bg-white/5 border border-white/10 text-gray-200/80 hover:text-white hover:border-white/20 transition"
                    title="Attach"
                  >
                    <Paperclip className="w-4 h-4" />
                    <span className="text-sm">Attach</span>
                  </button>
                  <button
                    type="button"
                    className="h-9 px-3 inline-flex items-center gap-2 rounded-full bg-white/5 border border-white/10 text-gray-200/80 hover:text-white hover:border-white/20 transition"
                    title="Theme"
                  >
                    <Wand2 className="w-4 h-4" />
                    <span className="text-sm">Theme</span>
                  </button>
                </div>

                <div className="flex items-center gap-2">
                  <motion.button
                    type="submit"
                    disabled={!inputValue.trim()}
                    whileHover={inputValue.trim() ? { scale: 1.03 } : {}}
                    whileTap={inputValue.trim() ? { scale: 0.97 } : {}}
                    className={`h-10 px-4 inline-flex items-center gap-2 rounded-full font-montserrat font-semibold transition ${
                      inputValue.trim()
                        ? 'bg-gradient-to-r from-neon-blue to-neon-cyan text-black shadow-[0_0_24px_rgba(0,242,254,0.25)]'
                        : 'bg-white/10 text-gray-400 cursor-not-allowed'
                    }`}
                  >
                    <Sparkles className={`w-4 h-4 ${inputValue.trim() ? 'animate-pulse' : ''}`} />
                    <span>Generate</span>
                  </motion.button>

                  <button
                    type="submit"
                    disabled={!inputValue.trim()}
                    className={`h-10 w-10 grid place-items-center rounded-full border transition ${
                      inputValue.trim()
                        ? 'bg-white/10 border-white/15 text-white hover:bg-white/15'
                        : 'bg-white/5 border-white/10 text-gray-500 cursor-not-allowed'
                    }`}
                    title="Send"
                  >
                    <ArrowUp className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Suggestion chips */}
          <div className="mt-6 flex flex-wrap justify-center gap-2">
            {suggestionChips.map((suggestion) => (
              <button
                key={suggestion}
                type="button"
                onClick={() => handleChipClick(suggestion)}
                className="px-3 py-1.5 rounded-full bg-black/30 border border-white/10 text-sm text-gray-200/80 hover:text-white hover:border-neon-cyan/40 transition"
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
