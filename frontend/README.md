# ELEMENT OF TRUTH - Frontend

A modern, cinematic React frontend for AI-powered educational video production, inspired by DreamWorks production studios and YouTube's content consumption experience.

## ✨ Features

### 🎬 Hero Section
- **Cinematic Background**: Animated particles and rotating atom structures
- **Premium Input Experience**: Large glowing text input with backdrop blur and neon effects
- **Interactive Suggestions**: Clickable chips that auto-fill the input
- **Smooth Animations**: Framer Motion powered transitions

### 🎭 Studio View
- **YouTube-style Layout**: 2-column grid with video player and script viewer
- **Agent Status Animation**: Step-by-step progress tracking of AI agents
- **Script Editor**: Markdown-style script display with copy functionality
- **Refinement Interface**: Chat-like input for script improvements

### 🎨 Design System
- **"Element of Truth" Theme**: Deep dark mode with blue/cyan neon accents
- **Glassmorphism**: Modern backdrop blur effects throughout
- **Cinematic Lighting**: Subtle animated light rays and particles
- **DreamWorks Aesthetic**: Professional production studio feel

## 🛠️ Tech Stack

- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS + Custom animations
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Fonts**: Cinzel (headers) + Montserrat (body) via Google Fonts

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm run dev
   ```

3. **Build for Production**:
   ```bash
   npm run build
   ```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── HeroSection.jsx      # Input experience with animations
│   │   ├── StudioView.jsx       # YouTube-style content layout
│   │   └── AgentStatus.jsx      # AI agent progress tracking
│   ├── App.jsx                  # Main layout orchestrator
│   ├── main.jsx                 # React entry point
│   └── index.css               # Tailwind + custom styles
├── index.html                   # HTML template
├── tailwind.config.js          # Tailwind configuration
├── vite.config.js              # Vite configuration
└── package.json                # Dependencies and scripts
```

## 🎯 Component Architecture

### App.jsx
- State management for view switching
- Fixed glassmorphism navbar
- Smooth page transitions

### HeroSection.jsx
- Animated background particles
- Premium input with focus effects
- Suggestion chips
- Generate button with sparkle animation

### StudioView.jsx
- 2-column responsive layout
- Video player placeholder
- Script viewer with markdown rendering
- Refinement input interface

### AgentStatus.jsx
- Terminal-style progress logs
- Animated agent completion
- Cinematic loading effects

## 🎨 Design Philosophy

Inspired by DreamWorks production studios, the interface combines:
- **Cinematic lighting effects** with subtle neon accents
- **Professional production aesthetics** with modern glassmorphism
- **YouTube's content consumption patterns** adapted for educational content
- **Terminal/command-line vibes** for the AI processing states

## 🔮 Future Enhancements

- Real video player integration
- Advanced script editing capabilities
- Multiple theme variants
- Accessibility improvements
- Performance optimizations

## 📄 License

This project is part of the Veritasium-in-a-Box ecosystem for AI-powered educational content creation.