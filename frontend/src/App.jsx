import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Activity, Sparkles, Zap } from 'lucide-react'
import HeroSection from './components/HeroSection'
import StudioView from './components/StudioView'
import AuthView from './components/AuthView'

function App() {
  const [currentView, setCurrentView] = useState('hero') // 'hero' | 'studio' | 'auth'
  const [generatedContent, setGeneratedContent] = useState(null)
  const [isGenerating, setIsGenerating] = useState(false)

  const handleGenerate = async (topic) => {
    setIsGenerating(true)
    setCurrentView('studio')

    // Simulate API call - replace with actual API integration
    setTimeout(() => {
      setGeneratedContent({
        title: `The Truth About ${topic}`,
        script: `# The Truth About ${topic}

## Introduction
*[DRAMATIC MUSIC PLAYS]*

**NARRATOR:** In our quest to understand the universe, few questions have puzzled humanity more than...

## The Core Mystery
*[VISUAL: Time-lapse of seasons changing]*

**NARRATOR:** What is the arrow of time? Why does time only flow forward?

## Scientific Breakthrough
*[VISUAL: Einstein's relativity equations]*

**NARRATOR:** Recent discoveries in quantum physics suggest...

## Conclusion
*[VISUAL: Beautiful cosmic imagery]*

**NARRATOR:** The arrow of time remains one of physics' greatest mysteries...`,
        thumbnail: null, // Will be generated
        stats: {
          views: '1.2M',
          likes: '45K',
          duration: '5:23'
        }
      })
      setIsGenerating(false)
    }, 3000)
  }

  const handleBackToHero = () => {
    setCurrentView('hero')
    setGeneratedContent(null)
    setIsGenerating(false)
  }

  return (
    <div className="min-h-screen bg-dark-slate relative overflow-x-hidden">
      {/* Global moving background (studio lighting) */}
      <div className="pointer-events-none fixed inset-0 -z-10">
        <div className="moving-aurora" />
        {/* Keep streaks extremely subtle so they don't read as a strip */}
        <div className="diagonal-streaks opacity-[0.06]" />
        <div className="gradient-overlay" />
        <div className="top-haze" />
        <div className="vignette" />
        <div className="film-grain" />
      </div>
      {/* Fixed Glassmorphism Navbar */}
      <motion.nav
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="fixed top-0 left-0 right-0 z-50"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3">
          {/* StreamNext-like floating header card */}
          <div className="relative rounded-2xl bg-white/6 border border-white/12 backdrop-blur-xl shadow-[0_18px_55px_rgba(0,0,0,0.35)]">
            <div className="absolute inset-x-0 -bottom-px h-px bg-gradient-to-r from-transparent via-neon-cyan/40 to-transparent" />
            <div className="px-4 sm:px-5 py-3 flex items-center justify-between gap-4">
            <motion.div className="flex items-center gap-3" whileHover={{ scale: 1.02 }}>
              <div className="w-9 h-9 bg-gradient-to-r from-neon-blue to-neon-cyan rounded-xl flex items-center justify-center shadow-[0_0_24px_rgba(0,242,254,0.18)]">
                <Zap className="w-5 h-5 text-black" />
              </div>
              <div className="leading-tight">
                <div className="text-lg md:text-xl font-cinzel font-bold tracking-wide text-white/90">
                  ELEMENT OF TRUTH
                </div>
              </div>
            </motion.div>

            <div className="flex items-center gap-3">
              <div className="hidden sm:flex items-center gap-2 px-3 py-2 rounded-full bg-white/5 border border-white/10">
                <Activity className="w-4 h-4 text-neon-cyan animate-pulse" />
                <span className="text-sm text-gray-200/80 font-montserrat">AI Systems Ready</span>
              </div>
              <button
                className="inline-flex items-center gap-2 h-10 px-4 rounded-full bg-white text-black/90 hover:bg-white/90 transition font-montserrat text-sm shadow-[0_10px_28px_rgba(0,0,0,0.25)]"
                onClick={() => setCurrentView('auth')}
              >
                <Sparkles className="w-4 h-4" />
                Get Started
              </button>
            </div>
            </div>
          </div>
        </div>
      </motion.nav>

      {/* Main Content */}
      <div className="pt-20">
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
      </div>
    </div>
  )
}

export default App
