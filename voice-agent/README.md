# 🎙️ Qwen Voice Agent (Chained Architecture)

- voice assistant built using a **Chained Architecture** (STT → LLM → TTS). This agent features an emotional reasoning layer, phonetic error correction, and high-fidelity speech synthesis via Groq's Orpheus model.

## 🏗️ Architecture

1.  **STT (Speech-to-Text):** Uses `SpeechRecognition` (Google Web API) to capture user intent.
2.  **LLM (Reasoning):** Uses **Qwen 3 (32B)** via Groq to process text. It includes a "Thinking" phase to handle phonetic corrections (e.g., mishearing "Queen" as "Qwen").
3.  **Clean-up:** A custom filter to strip `<think>` tags before the response reaches the voice layer.
4.  **TTS (Text-to-Speech):** Uses **Canopy Labs Orpheus** via Groq to generate realistic WAV audio, played directly from memory using `PyAudio`.

---

## 🚀 Installation & Prerequisites

- This project uses `uv` for lightning-fast Python package management.

### System Dependencies (Audio Drivers)

- Before installing Python packages, you must ensure your system handles audio input/output correctly.

- **For macOS:**
  You must install `portaudio` first.
  ```bash
  brew install portaudio

- **For windows:**
No extra config is needed

- Create env File:
- add GROQ_API_KEY=your_groq_api_key_here