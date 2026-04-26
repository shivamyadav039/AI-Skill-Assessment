# UI Setup & Demo Guide

**Status**: 🚀 Ready to Run  
**Frontend Framework**: React 18 + Vite + Tailwind CSS  
**Backend**: FastAPI (http://localhost:8000)

---

## 🎯 Quick Start (5 minutes)

### 1. Install Frontend Dependencies
```bash
cd frontend
npm install
```

### 2. Start the Frontend (Dev Server)
```bash
npm run dev
```
Runs on: **http://localhost:5173**

### 3. Start the Backend (in another terminal)
```bash
cd backend
python3 -m app.main
```
API available at: **http://localhost:8000**  
API Docs: **http://localhost:8000/docs**

### 4. View the Application
Open browser: **http://localhost:5173**

---

## 📱 Features in UI

### Landing Page
- ✅ Beautiful gradient design with purple/pink theme
- ✅ Project status dashboard (phases 1-5)
- ✅ Tech stack showcase
- ✅ Feature highlights
- ✅ "How It Works" step-by-step guide
- ✅ Call-to-action for interactive demo

### Interactive Demo
- 📋 Quick start instructions
- ✅ Status of all systems
- 🔄 Integration with backend API
- 📖 Links to documentation

---

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── App.jsx              # Main app component (landing page + demo)
│   ├── App.css              # Tailwind CSS setup
│   ├── main.jsx             # React entry point
│   └── components/          # UI components (future)
│       ├── DocumentUpload.jsx
│       ├── SkillAssessment.jsx
│       └── ResultsDashboard.jsx
│
├── index.html               # HTML entry point
├── package.json             # Dependencies
├── vite.config.js           # Vite configuration
├── tailwind.config.js       # Tailwind configuration
├── postcss.config.js        # PostCSS configuration
└── README.md
```

---

## 🎨 Design System

### Color Palette
- **Primary**: Purple (#a855f7)
- **Secondary**: Pink (#ec4899)
- **Background**: Dark Slate (#0f172a)
- **Text**: Light Gray (#f3f4f6)
- **Accent**: Green (success), Yellow (warning)

### Typography
- Font Family: Inter (via Tailwind)
- Heading Sizes: 2xl, 3xl, 4xl, 5xl
- Regular text: 14px - 18px

### Components
- Cards with hover effects
- Gradient buttons
- Progress bars
- Status indicators
- Feature cards
- Statistics display

---

## 🔌 API Integration

### Endpoints Used
```javascript
// Backend API configuration
const API_BASE = 'http://localhost:8000';

// Available endpoints:
POST /api/v1/upload          // Upload JD & Resume
POST /api/v1/chat            // Assessment conversation
POST /api/v1/score           // Score responses
POST /api/v1/plan            // Generate learning plan
GET  /api/v1/gaps/{id}       // Get skill gaps
GET  /health                 // Health check
```

### Example API Call (React)
```javascript
import axios from 'axios';

const uploadDocuments = async (jdContent, resumeContent, candidateName) => {
  try {
    const response = await axios.post('http://localhost:8000/api/v1/upload', {
      jd_content: jdContent,
      resume_content: resumeContent,
      candidate_name: candidateName
    });
    return response.data;
  } catch (error) {
    console.error('Upload failed:', error);
  }
};
```

---

## 🚀 Build for Production

### Build
```bash
npm run build
```
Output: `dist/` folder

### Preview Production Build
```bash
npm run preview
```

### Deployment
1. Build: `npm run build`
2. Deploy `dist/` folder to static hosting (Vercel, Netlify, AWS S3, etc.)
3. Configure API proxy to backend

---

## 📋 Implementation Roadmap

### Phase 5.1: Document Upload (Next)
- [ ] File upload form
- [ ] JD & Resume parsing
- [ ] Skill extraction display
- [ ] Session initialization

### Phase 5.2: Assessment Chat
- [ ] Real-time chat interface
- [ ] Message history
- [ ] Response quality indicators
- [ ] Turn counter

### Phase 5.3: Results Dashboard
- [ ] Skill score visualization
- [ ] Proficiency level display
- [ ] Gap analysis charts
- [ ] Learning plan timeline

### Phase 5.4: Learning Dashboard
- [ ] Interactive learning roadmap
- [ ] Resource recommendations
- [ ] Progress tracking
- [ ] Milestone tracking

---

## 🔧 Development Tips

### Adding New Components
```javascript
// Create: src/components/MyComponent.jsx
import React from 'react';

export default function MyComponent() {
  return (
    <div className="bg-slate-800/50 border border-purple-500/20 rounded-lg p-6">
      {/* Component content */}
    </div>
  );
}

// Use in App.jsx
import MyComponent from './components/MyComponent';
```

### Styling
All styling uses Tailwind CSS classes. Key patterns:
```javascript
// Background
className="bg-slate-800/50"  // Dark background with transparency

// Borders
className="border border-purple-500/20"  // Subtle purple border

// Text
className="text-white"      // White text
className="text-gray-400"   // Muted gray text
className="text-purple-300" // Purple accent

// Gradients
className="bg-gradient-to-r from-purple-500 to-pink-500"

// Hover Effects
className="hover:border-purple-500/50 transition"
```

### Debugging
```bash
# Check for Tailwind CSS issues
npm run dev -- --debug

# Build with source maps
npm run build
```

---

## 📦 Dependencies

### Production
- `react@18.2.0` - UI framework
- `react-dom@18.2.0` - React DOM
- `axios@1.6.0` - HTTP client
- `lucide-react@0.263.1` - Icons
- `classnames@2.3.2` - Utility for className

### Development
- `vite@4.4.0` - Build tool
- `@vitejs/plugin-react@4.0.0` - React plugin
- `tailwindcss@3.3.0` - CSS framework
- `postcss@8.4.24` - CSS processor
- `autoprefixer@10.4.14` - CSS autoprefixer

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9

# Or use different port
npm run dev -- --port 3000
```

### API Connection Issues
1. Ensure backend is running: `cd backend && python3 -m app.main`
2. Check API is accessible: `curl http://localhost:8000/health`
3. Verify CORS is configured (it should be by default)

### Tailwind Not Working
1. Delete node_modules: `rm -rf node_modules`
2. Clear npm cache: `npm cache clean --force`
3. Reinstall: `npm install`

### Build Errors
```bash
# Clean rebuild
rm -rf node_modules dist
npm install
npm run build
```

---

## 📚 Resources

- [React Docs](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Vite Guide](https://vitejs.dev)
- [Axios Documentation](https://axios-http.com)

---

## ✅ Checklist Before Demo

- [ ] Frontend running on localhost:5173
- [ ] Backend running on localhost:8000
- [ ] API docs accessible at localhost:8000/docs
- [ ] UI loads without errors
- [ ] Responsive design works on different screen sizes
- [ ] All links/buttons functional
- [ ] No console errors

---

## 🎬 Demo Script

1. **Show Landing Page**
   - Display beautiful UI
   - Highlight project status (60% complete)
   - Show tech stack

2. **Launch Interactive Demo**
   - Click "Launch Interactive Demo" button
   - Show quick start instructions
   - Demonstrate system status

3. **API Documentation**
   - Navigate to http://localhost:8000/docs
   - Show available endpoints
   - Try sample requests

4. **Backend Status**
   - Run health check: `curl http://localhost:8000/health`
   - Show all systems operational

5. **Test Results**
   - Run: `python3 test_phase25_integration.py`
   - Show all 6 tests passing

---

**Next Steps After Phase 5.1:**
- Implement document upload component
- Connect to backend /api/v1/upload
- Build assessment chat UI
- Create results dashboard

**Estimated Time to Phase 5 Complete**: 2-3 hours

---

*Status: Phase 5 (UI) - 60% Complete*  
*Last Updated: April 26, 2026*
