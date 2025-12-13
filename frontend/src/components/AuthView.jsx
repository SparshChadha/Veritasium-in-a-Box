import { useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowLeft, KeyRound, Mail, ShieldCheck, User } from 'lucide-react'

export default function AuthView({ onClose, onSuccess }) {
  const [mode, setMode] = useState('signin') // signin | signup
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')

  const title = useMemo(() => (mode === 'signin' ? 'Sign in' : 'Create account'), [mode])

  const submit = (e) => {
    e.preventDefault()
    // TODO: integrate real auth
    onSuccess?.({ email, name })
  }

  return (
    <div className="min-h-[calc(100vh-80px)] pt-6 pb-16 px-6">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between">
          <button
            onClick={onClose}
            className="inline-flex items-center gap-2 px-3 py-2 rounded-full bg-white/6 border border-white/10 text-white/80 hover:bg-white/10 transition font-montserrat text-sm"
          >
            <ArrowLeft className="w-4 h-4" />
            Back
          </button>
          <div className="hidden sm:flex items-center gap-2 text-xs text-gray-200/70 font-montserrat">
            <ShieldCheck className="w-4 h-4 text-neon-cyan" />
            Secure authentication (demo UI)
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8"
        >
          {/* Left: message */}
          <div className="rounded-3xl bg-white/5 border border-white/10 backdrop-blur-xl p-8 cinematic-shadow">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-black/30 border border-white/10 text-xs text-gray-200/80">
              ELEMENT OF TRUTH
            </div>
            <h2 className="mt-4 text-3xl md:text-4xl font-cinzel font-bold text-white/90 tracking-tight">
              Enter the studio.
            </h2>
            <p className="mt-3 text-gray-200/70 font-montserrat">
              Sign in to save projects, refine scripts, and publish your generated videos.
            </p>

            <div className="mt-8 space-y-3 text-sm text-gray-200/70 font-montserrat">
              <div className="flex items-center gap-3">
                <KeyRound className="w-4 h-4 text-neon-blue" />
                Fast sign-in (UI only for now)
              </div>
              <div className="flex items-center gap-3">
                <ShieldCheck className="w-4 h-4 text-neon-cyan" />
                Built for your “Element of Truth” pipeline
              </div>
            </div>
          </div>

          {/* Right: form */}
          <div className="rounded-3xl bg-black/35 border border-white/10 backdrop-blur-xl p-8 cinematic-shadow">
            <div className="flex items-center gap-2 p-1 rounded-full bg-white/5 border border-white/10 w-fit">
              <button
                type="button"
                onClick={() => setMode('signin')}
                className={`px-4 py-2 rounded-full text-sm font-montserrat transition ${
                  mode === 'signin' ? 'bg-white text-black' : 'text-white/70 hover:text-white'
                }`}
              >
                Sign in
              </button>
              <button
                type="button"
                onClick={() => setMode('signup')}
                className={`px-4 py-2 rounded-full text-sm font-montserrat transition ${
                  mode === 'signup' ? 'bg-white text-black' : 'text-white/70 hover:text-white'
                }`}
              >
                Sign up
              </button>
            </div>

            <h3 className="mt-6 text-xl font-cinzel font-bold text-white">{title}</h3>
            <p className="mt-1 text-sm text-gray-200/60 font-montserrat">
              {mode === 'signin' ? 'Welcome back.' : 'Create a new account to continue.'}
            </p>

            <form onSubmit={submit} className="mt-6 space-y-4">
              {mode === 'signup' && (
                <label className="block">
                  <div className="text-xs text-gray-200/60 font-montserrat mb-2">Name</div>
                  <div className="flex items-center gap-2 rounded-xl bg-black/30 border border-white/10 px-3 py-3 focus-within:border-neon-cyan/60 transition">
                    <User className="w-4 h-4 text-gray-300/70" />
                    <input
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="w-full bg-transparent outline-none text-white/90 font-montserrat"
                      placeholder="Your name"
                    />
                  </div>
                </label>
              )}

              <label className="block">
                <div className="text-xs text-gray-200/60 font-montserrat mb-2">Email</div>
                <div className="flex items-center gap-2 rounded-xl bg-black/30 border border-white/10 px-3 py-3 focus-within:border-neon-cyan/60 transition">
                  <Mail className="w-4 h-4 text-gray-300/70" />
                  <input
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    type="email"
                    className="w-full bg-transparent outline-none text-white/90 font-montserrat"
                    placeholder="you@domain.com"
                    required
                  />
                </div>
              </label>

              <label className="block">
                <div className="text-xs text-gray-200/60 font-montserrat mb-2">Password</div>
                <div className="flex items-center gap-2 rounded-xl bg-black/30 border border-white/10 px-3 py-3 focus-within:border-neon-cyan/60 transition">
                  <KeyRound className="w-4 h-4 text-gray-300/70" />
                  <input
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    type="password"
                    className="w-full bg-transparent outline-none text-white/90 font-montserrat"
                    placeholder="••••••••"
                    required
                  />
                </div>
              </label>

              <motion.button
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
                type="submit"
                className="w-full h-11 rounded-xl bg-white text-black/90 hover:bg-white/90 transition font-montserrat font-semibold shadow-[0_10px_28px_rgba(0,0,0,0.25)]"
              >
                {mode === 'signin' ? 'Continue' : 'Create account'}
              </motion.button>

              <div className="text-xs text-gray-200/50 font-montserrat">
                This is a UI-only auth screen. Hook it to your backend when ready.
              </div>
            </form>
          </div>
        </motion.div>
      </div>
    </div>
  )
}


