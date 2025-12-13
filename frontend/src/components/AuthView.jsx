import { useMemo, useState } from 'react'
// eslint-disable-next-line no-unused-vars
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
            className="inline-flex items-center gap-2 px-3 py-2 rounded-full bg-gray-100 border border-gray-200 text-gray-700 hover:bg-gray-200 transition font-montserrat text-sm"
          >
            <ArrowLeft className="w-4 h-4" />
            Back
          </button>
          <div className="hidden sm:flex items-center gap-2 text-xs text-gray-600 font-montserrat">
            <ShieldCheck className="w-4 h-4 text-blue-600" />
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
          <div className="rounded-3xl bg-white border border-gray-200 backdrop-blur-xl p-8 shadow-lg">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-100 border border-gray-200 text-xs text-gray-700">
              ELEMENT OF TRUTH
            </div>
            <h2 className="mt-4 text-3xl md:text-4xl font-cinzel font-bold text-gray-900 tracking-tight">
              Enter the studio.
            </h2>
            <p className="mt-3 text-gray-600 font-montserrat">
              Sign in to save projects, refine scripts, and publish your generated videos.
            </p>

            <div className="mt-8 space-y-3 text-sm text-gray-600 font-montserrat">
              <div className="flex items-center gap-3">
                <KeyRound className="w-4 h-4 text-blue-600" />
                Fast sign-in (UI only for now)
              </div>
              <div className="flex items-center gap-3">
                <ShieldCheck className="w-4 h-4 text-blue-600" />
                Built for your "Element of Truth" pipeline
              </div>
            </div>
          </div>

          {/* Right: form */}
          <div className="rounded-3xl bg-white border border-gray-200 backdrop-blur-xl p-8 shadow-lg">
            <div className="flex items-center gap-2 p-1 rounded-full bg-gray-100 border border-gray-200 w-fit">
              <button
                type="button"
                onClick={() => setMode('signin')}
                className={`px-4 py-2 rounded-full text-sm font-montserrat transition ${
                  mode === 'signin' ? 'bg-gray-900 text-white' : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Sign in
              </button>
              <button
                type="button"
                onClick={() => setMode('signup')}
                className={`px-4 py-2 rounded-full text-sm font-montserrat transition ${
                  mode === 'signup' ? 'bg-gray-900 text-white' : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Sign up
              </button>
            </div>

            <h3 className="mt-6 text-xl font-cinzel font-bold text-gray-900">{title}</h3>
            <p className="mt-1 text-sm text-gray-600 font-montserrat">
              {mode === 'signin' ? 'Welcome back.' : 'Create a new account to continue.'}
            </p>

            <form onSubmit={submit} className="mt-6 space-y-4">
              {mode === 'signup' && (
                <label className="block">
                  <div className="text-xs text-gray-600 font-montserrat mb-2">Name</div>
                  <div className="flex items-center gap-2 rounded-xl bg-gray-50 border border-gray-200 px-3 py-3 focus-within:border-blue-400 transition">
                    <User className="w-4 h-4 text-gray-500" />
                    <input
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="w-full bg-transparent outline-none text-gray-900 font-montserrat"
                      placeholder="Your name"
                    />
                  </div>
                </label>
              )}

              <label className="block">
                <div className="text-xs text-gray-600 font-montserrat mb-2">Email</div>
                <div className="flex items-center gap-2 rounded-xl bg-gray-50 border border-gray-200 px-3 py-3 focus-within:border-blue-400 transition">
                  <Mail className="w-4 h-4 text-gray-500" />
                  <input
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    type="email"
                    className="w-full bg-transparent outline-none text-gray-900 font-montserrat"
                    placeholder="you@domain.com"
                    required
                  />
                </div>
              </label>

              <label className="block">
                <div className="text-xs text-gray-600 font-montserrat mb-2">Password</div>
                <div className="flex items-center gap-2 rounded-xl bg-gray-50 border border-gray-200 px-3 py-3 focus-within:border-blue-400 transition">
                  <KeyRound className="w-4 h-4 text-gray-500" />
                  <input
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    type="password"
                    className="w-full bg-transparent outline-none text-gray-900 font-montserrat"
                    placeholder="••••••••"
                    required
                  />
                </div>
              </label>

              <motion.button
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
                type="submit"
                className="w-full h-11 rounded-xl bg-gray-900 text-white hover:bg-gray-800 transition font-montserrat font-semibold shadow-lg"
              >
                {mode === 'signin' ? 'Continue' : 'Create account'}
              </motion.button>

              <div className="text-xs text-gray-500 font-montserrat">
                This is a UI-only auth screen. Hook it to your backend when ready.
              </div>
            </form>
          </div>
        </motion.div>
      </div>
    </div>
  )
}


