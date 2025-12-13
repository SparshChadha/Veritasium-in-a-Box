import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { CheckCircle, Clock, BookOpen, Shield, GraduationCap, Film } from 'lucide-react'

const AgentStatus = () => {
  const [currentStep, setCurrentStep] = useState(0)
  const [logs, setLogs] = useState([])

  const agents = [
    {
      id: 'historian',
      name: 'Historian Agent',
      icon: BookOpen,
      color: 'text-blue-400',
      action: 'Researching historical context...',
      duration: 800
    },
    {
      id: 'skeptic',
      name: 'Skeptic Agent',
      icon: Shield,
      color: 'text-yellow-400',
      action: 'Analyzing claims and debunking myths...',
      duration: 1200
    },
    {
      id: 'professor',
      name: 'Professor Agent',
      icon: GraduationCap,
      color: 'text-green-400',
      action: 'Validating scientific accuracy...',
      duration: 1000
    },
    {
      id: 'director',
      name: 'Director Agent',
      icon: Film,
      color: 'text-purple-400',
      action: 'Crafting the final narrative...',
      duration: 600
    }
  ]

  useEffect(() => {
    const timer = setTimeout(() => {
      if (currentStep < agents.length) {
        const agent = agents[currentStep]
        setLogs(prev => [...prev, {
          id: agent.id,
          message: `${agent.name} ${agent.action}`,
          timestamp: new Date().toLocaleTimeString(),
          status: 'completed'
        }])
        setCurrentStep(prev => prev + 1)
      }
    }, agents[currentStep]?.duration || 0)

    return () => clearTimeout(timer)
  }, [currentStep])

  const getAgentIcon = (agentId, isActive, isCompleted) => {
    const agent = agents.find(a => a.id === agentId)
    const Icon = agent?.icon

    if (isCompleted) {
      return <CheckCircle className="w-6 h-6 text-green-400" />
    } else if (isActive) {
      return <Icon className={`w-6 h-6 ${agent?.color} animate-pulse`} />
    } else {
      return <Clock className="w-6 h-6 text-gray-500" />
    }
  }

  return (
    <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-dark-slate to-slate-900 flex items-center justify-center">
      {/* Background Animation */}
      <div className="absolute inset-0">
        {[...Array(15)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-px h-px bg-neon-cyan rounded-full"
            animate={{
              opacity: [0, 1, 0],
              scale: [1, 1.5, 1],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
          />
        ))}
      </div>

      <div className="relative z-10 max-w-2xl mx-auto px-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h2 className="text-3xl font-cinzel font-bold text-white mb-2 neon-text">
            AI Production Studio
          </h2>
          <p className="text-gray-400 font-montserrat">
            Our expert agents are crafting your video...
          </p>
        </motion.div>

        {/* Agent Progress */}
        <div className="space-y-4 mb-8">
          {agents.map((agent, index) => {
            const isCompleted = index < currentStep
            const isActive = index === currentStep
            const isPending = index > currentStep

            return (
              <motion.div
                key={agent.id}
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.2 }}
                className={`flex items-center space-x-4 p-4 rounded-lg backdrop-blur-sm border transition-all duration-500 ${
                  isCompleted
                    ? 'bg-green-900/20 border-green-500/30'
                    : isActive
                    ? 'bg-glass border-neon-cyan shadow-neon'
                    : 'bg-glass border-glass-border'
                }`}
              >
                <div className="flex-shrink-0">
                  {getAgentIcon(agent.id, isActive, isCompleted)}
                </div>

                <div className="flex-1">
                  <h3 className={`font-montserrat font-semibold ${
                    isCompleted ? 'text-green-400' :
                    isActive ? 'text-white' :
                    'text-gray-400'
                  }`}>
                    {agent.name}
                  </h3>
                  <p className={`text-sm font-montserrat ${
                    isCompleted ? 'text-green-300' :
                    isActive ? 'text-gray-300 animate-pulse' :
                    'text-gray-500'
                  }`}>
                    {isCompleted ? '✓ Complete' :
                     isActive ? agent.action :
                     'Waiting...'}
                  </p>
                </div>

                {/* Progress Bar for Active Agent */}
                {isActive && (
                  <motion.div
                    className="w-24 h-2 bg-gray-700 rounded-full overflow-hidden"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                  >
                    <motion.div
                      className="h-full bg-gradient-to-r from-neon-blue to-neon-cyan rounded-full"
                      initial={{ width: '0%' }}
                      animate={{ width: '100%' }}
                      transition={{
                        duration: agent.duration / 1000,
                        ease: "easeInOut"
                      }}
                    />
                  </motion.div>
                )}
              </motion.div>
            )
          })}
        </div>

        {/* Terminal-style Logs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-black/50 backdrop-blur-sm border border-glass-border rounded-lg p-4 font-mono text-sm"
        >
          <div className="text-green-400 mb-2">$ veritasium-ai production.log</div>
          <div className="space-y-1 max-h-32 overflow-y-auto">
            <AnimatePresence>
              {logs.map((log, index) => (
                <motion.div
                  key={log.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  className="text-gray-300"
                >
                  <span className="text-gray-500">[{log.timestamp}]</span>{' '}
                  <span className="text-green-400">✓</span>{' '}
                  {log.message}
                </motion.div>
              ))}
            </AnimatePresence>

            {currentStep < agents.length && (
              <motion.div
                animate={{ opacity: [1, 0.5, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
                className="text-neon-cyan"
              >
                [{new Date().toLocaleTimeString()}] ⟳ {agents[currentStep]?.name} {agents[currentStep]?.action}
              </motion.div>
            )}
          </div>
        </motion.div>

        {/* Progress Indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="text-center mt-6"
        >
          <div className="text-gray-400 font-montserrat text-sm">
            Progress: {Math.round((currentStep / agents.length) * 100)}%
          </div>
          <motion.div
            className="w-full h-1 bg-gray-700 rounded-full mt-2 overflow-hidden"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.2 }}
          >
            <motion.div
              className="h-full bg-gradient-to-r from-neon-blue to-neon-cyan rounded-full"
              initial={{ width: '0%' }}
              animate={{ width: `${(currentStep / agents.length) * 100}%` }}
              transition={{ duration: 0.5, ease: "easeOut" }}
            />
          </motion.div>
        </motion.div>
      </div>
    </div>
  )
}

export default AgentStatus
