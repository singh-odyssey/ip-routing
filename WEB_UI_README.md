# 🌐 IP Routing Bot - Web UI

A professional web interface for the IP Routing Bot Suite that allows users to generate unique views and simulate traffic through a clean, modern web dashboard.

## ✨ Features

### 🎯 **Google Ambassador Bot**
- **Web-based URL input** - Simply paste any URL into the form
- **Configurable view count** - Set target number of views or run unlimited
- **Real-time monitoring** - Watch progress with live updates
- **Indian IP rotation** - Automatically uses 65+ Indian IP addresses
- **Bot controls** - Start, pause, resume, and stop operations

### 👥 **Seminar Parallel Bot**
- **QR code simulation** - Simulates students scanning QR codes simultaneously
- **Configurable seminar size** - 25 to 300+ students
- **Live student tracking** - See individual student scans in real-time
- **Geographic diversity** - Students from different Indian cities and ISPs
- **Seminar analytics** - Completion rates, timing, and distribution

### 📊 **Statistics Dashboard**
- **IP database overview** - All 65+ Indian IPs with city/ISP details
- **Geographic distribution** - Interactive charts showing IP coverage
- **Performance metrics** - Success rates, response times, uptime
- **Real-time analytics** - Live updates during bot operations

### 🛡️ **Advanced Features**
- **Real-time WebSocket updates** - Live progress without page refresh
- **Beautiful UI** - Modern, responsive design with Bootstrap 5
- **Mobile-friendly** - Works on phones, tablets, and desktops
- **Error handling** - Comprehensive error messages and recovery
- **Session management** - Track multiple bot instances

## 🚀 Quick Start

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Start the Web Server**
```bash
python web_ui.py
```

### 3. **Open Your Browser**
Navigate to: `http://localhost:5000`

## 📱 Using the Web Interface

### **Dashboard (Home Page)**
- Overview of the entire system
- Quick start buttons for both bots
- IP database statistics
- System status monitoring

### **Google Ambassador Bot Page**
1. **Paste your target URL** in the input field
2. **Set number of views** (or leave empty for unlimited)
3. **Click "Start Google Bot"** 
4. **Watch real-time progress** with live updates
5. **Control the bot** with pause/resume/stop buttons

### **Seminar Bot Page**
1. **Enter the QR code target URL**
2. **Select seminar size** (25-300 students)
3. **Click "Start Seminar Simulation"**
4. **Watch the countdown** as students prepare to scan
5. **Monitor live scanning** progress and analytics

### **Statistics Page**
- **View IP database** details and distribution
- **Geographic charts** showing city/ISP coverage
- **Performance metrics** and success rates
- **Export tools** for reports and analysis

## 🎯 How It Works

### **Google Ambassador Bot Flow:**
1. User pastes URL in web form
2. Bot creates unique Indian sessions (different IP, ISP, device)
3. Each session visits the URL with realistic timing (2-5 seconds)
4. Real-time updates show progress via WebSocket
5. Statistics track success rate and geographic diversity

### **Seminar Bot Flow:**
1. User configures seminar size and QR target URL
2. Simulation shows countdown like real presentation
3. All "students" scan QR code simultaneously 
4. Live feed shows individual student activity
5. Analytics display completion rate and demographics

## 🔧 Technical Details

### **Backend:**
- **Flask** web framework with **SocketIO** for real-time updates
- **Threading** for concurrent bot operations
- **Smart IP rotation** using the existing Indian IP database
- **Session management** for multiple concurrent bots

### **Frontend:**
- **Bootstrap 5** for responsive design
- **Socket.IO client** for real-time updates
- **Chart.js** for statistics visualization
- **Font Awesome** icons for modern UI

### **Real-time Updates:**
- WebSocket connection for live progress
- Individual session details (IP, city, ISP)
- Success/failure notifications
- Geographic diversity tracking
- Performance metrics

## 🌍 IP Database Integration

The web UI seamlessly integrates with your existing:
- **65+ Indian IP addresses** from 30+ cities
- **8+ ISP providers** (Jio, Airtel, Vi, BSNL, etc.)
- **Smart session management** with unique fingerprints
- **Geographic bias** toward Delhi NCR when configured

## 📊 Real-time Monitoring

### **Live Updates Include:**
- Current Indian user (location, ISP, device)
- View generation progress and success rate
- Geographic diversity (cities, IPs, ISPs used)
- Timing information and bot status
- Error messages and recovery suggestions

### **Interactive Controls:**
- Start/stop/pause bot operations
- Real-time configuration changes
- Export functionality for reports
- Session management and monitoring

## 🎨 User Interface

### **Modern Design:**
- Clean, professional appearance
- Intuitive navigation between tools
- Mobile-responsive layout
- Real-time status indicators
- Beautiful charts and visualizations

### **User Experience:**
- **No terminal needed** - Everything through web browser
- **Simple URL pasting** - Just copy and paste target URLs
- **One-click operation** - Start bots with single button
- **Visual feedback** - See exactly what's happening
- **Error recovery** - Clear error messages and solutions

## 🔒 Security & Detection Avoidance

The web UI maintains all the advanced anti-detection features:
- **Unique sessions** - Every view appears from different user
- **Realistic timing** - 2-5 second intervals between requests
- **Indian characteristics** - Proper headers, language, timezone
- **ISP simulation** - Different network characteristics
- **Device diversity** - Mobile and desktop user agents

## 📞 Support & Troubleshooting

### **Common Issues:**
1. **"Connection failed"** - Check if server is running on port 5000
2. **"Bot won't start"** - Verify URL is valid and accessible
3. **"No real-time updates"** - Refresh page to reconnect WebSocket
4. **"Import errors"** - Run `pip install -r requirements.txt`

### **Performance:**
- Web UI uses minimal resources
- Real-time updates are efficient
- Bot operations same speed as terminal version
- Can handle multiple concurrent sessions

## 🎉 Benefits of Web UI

### **Compared to Terminal:**
✅ **User-friendly** - No command-line knowledge needed  
✅ **Visual feedback** - See progress and statistics  
✅ **Easy URL input** - Simple copy and paste  
✅ **Multi-tasking** - Use browser while bot runs  
✅ **Better control** - Start/stop with single click  
✅ **Shareable** - Others can use the same interface  
✅ **Mobile access** - Works on phones and tablets  

## 🎯 Perfect For

- **Google Student Ambassadors** generating unique views
- **Content creators** needing traffic simulation
- **Marketing teams** testing website engagement
- **Researchers** studying user behavior patterns
- **Anyone** who wants an easy-to-use interface

---

**🚀 Ready to get started? Run `python web_ui.py` and open http://localhost:5000 in your browser!**