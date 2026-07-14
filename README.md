# 🌤️ Weather_Tether

<div align="center">

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Kivy](https://img.shields.io/badge/Framework-Kivy-green?logo=python&logoColor=white)](https://kivy.org/)
[![CarbonKivy](https://img.shields.io/badge/UI%20Framework-CarbonKivy-black)](https://github.com/CarbonKivy/CarbonKivy)
[![Android](https://img.shields.io/badge/Platform-Android-green?logo=android&logoColor=white)](https://www.android.com/)
[![Status](https://img.shields.io/badge/Status-Active%20Development-orange)](https://github.com/arjunet/Weather_Tether)

A beautiful, modern weather application built with **CarbonKivy** UI framework featuring smooth animations and native Android support.

[Discord](#-join-the-community) • [Features](#-features) • [Screenshots](#-screens) • [Installation](#-getting-started)

</div>

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| **Screens Built** | 9 |
| **UI Components** | 13+ |
| **Helper Modules** | 14 |
| **Image Assets** | 12 |
| **Python Version** | 3.11+ |
| **Latest Version** | v0.4-DEV (05/29/2026) |
| **Development Status** | Active 🚀 |

---

## 🎯 Features

- ✨ Modern **CarbonKivy UI** with smooth animations and transitions  
- 🌡️ Real-time weather data integration  
- 📱 Responsive design optimized for mobile  
- 🔐 Secure authentication system (Signup, Sign-in, Forgot Password)  
- 🌍 Multi-city weather tracking (30 cities supported)    
- 🎨 Dynamic backgrounds based on weather conditions  
- ⚙️ Comprehensive settings panel  
- 🔔 Real-time notifications  
- 📦 **APK successfully compiled** with Buildozer  

---

## 📱 Screens

<table>
<tr>
<td>
  
**Authentication**
- Signup Screen
- Sign-in Screen
- Forgot Password Screen
- Verification Screen
  
</td>
<td>
  
**Weather Display**
- Base Screens
  
</td>
<td>
  
**Configuration**
- Setup Screen
- Settings Screen
  
</td>
</tr>
</table>

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Framework** | Kivy 2.3.1+ |
| **UI Library** | CarbonKivy |
| **Language** | Python 3.11+ |
| **Build Tool** | Buildozer |
| **Package Manager** | pip |
| **API Integration** | requests |
| **Data Storage** | JSON Store |
| **Android SDK** | pyjnius |

---

## 📦 Key Dependencies

```
kivy>=2.3.1
CarbonKivy (from GitHub)
requests
pyjnius
python3
android
```

---

## 🏗️ Project Structure

```
Weather_Tether/
├── main.py                 # Application entry point
├── main.kv                 # Main UI layout
├── pyproject.toml          # Project configuration
├── buildozer.spec          # Android build configuration
├── config.toml             # App configuration
├── helpers/                # Helper modules (14 files)
│   ├── app.py              # Core weather logic
│   ├── login.py            # Login handler
│   ├── signup.py           # Signup handler
│   ├── token_management.py # Auth token management
│   ├── notification.py     # Notification system
│   ├── settings.py         # Settings management
│   ├── sidepanel.py        # Side panel component
│   ├── modal_loader.py     # Modal dialogs
│   └── ...                 # More helper modules
├── images/                 # Image assets (12 files)
│   ├── icon.png            # App icon
│   ├── presplash.jpg       # Splash screen
│   ├── sun_bg.jpg          # Weather backgrounds
│   ├── rain_bg.jpg
│   ├── cloud_bg.jpg
│   └── ...                 # More assets
└── docs/                   # Documentation
    ├── privacy_policy.html
    └── deletion.html
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Buildozer (for APK compilation)
- Android SDK/NDK (for mobile deployment)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/arjunet/Weather_Tether.git
   cd Weather_Tether
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install https://github.com/CarbonKivy/CarbonKivy/archive/master.zip
   ```

4. **Run the app**
   ```bash
   python main.py
   ```

### Building APK

```bash
buildozer android debug
```

---

## 📝 Version History

| Version | Released | Status |
|---------|----------|--------|
| **v0.4-DEV** | 05/29/2026 | 🟢 Current |
| **v0.3-DEV** | 01/17/2026 | ✅ Supported |
| **v0.2-DEV** | 11/23/2025 | ✅ Supported |
| **v0.1-DEV** | 11/11/2025 | ✅ Supported |

---

## 🔒 Security

For security concerns, see [SECURITY.md](SECURITY.md).

**Supported Versions:**
- v0.3-DEV ✅
- v0.2-DEV ✅
- v0.1-DEV ✅

---

## 💬 Join the Community

<div align="center">

[![Discord](https://img.shields.io/badge/Discord-Join%20Server-5865F2?logo=discord&logoColor=white)](https://discord.gg/MJP7dAtY3D)

Have questions? Want to contribute? Join our Discord community!

</div>

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## 🙌 Special Thanks

Big thanks to **[@Novfensec](https://github.com/Novfensec)** for the compilation fixes and helping me navigate the quirks of this project! 🎉

---

<div align="center">

Made with ❤️ by [arjunet (Arjune Mithu)](https://github.com/arjunet)

⭐ If you found this helpful, please star the repository!

</div>
