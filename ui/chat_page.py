import gradio as gr
from typing import List, Dict, Any
from models.session import ResearchSession
from services.chat_rag_service import ChatRAGService
from services.transcription_service import TranscriptionService
from ui.assets import CHAT_ASSISTANT_IMG

INITIAL_WELCOME_MESSAGE = [
    {
        "role": "assistant",
        "content": (
            "**Hello. I am Salim, your AI Research Assistant.**\n\n"
            "I can help you review, synthesize, and analyze academic literature. Here is how I can assist:\n\n"
            "- **Voice Input:** Click the **🎙️ Mic** button to speak your question directly.\n"
            "- **Literature Synthesis:** Summarize core contributions across your active papers.\n"
            "- **Methodology Extraction:** Compare datasets, models, and simulation frameworks.\n"
            "- **Research Gaps:** Identify empirical limitations and open challenges.\n\n"
            "Type a question below, click the microphone to speak, or select one of the quick actions on the left."
        )
    }
]

VOICE_SCRIPT_HEAD = """
<script>
(function() {
  let recognition = null;
  let isListening = false;

  function updateInputElement(input, text) {
    if (!input) return;
    const proto = input.tagName === "TEXTAREA" ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
    const setter = Object.getOwnPropertyDescriptor(proto, "value")?.set;
    if (setter) {
      setter.call(input, text);
    } else {
      input.value = text;
    }
    input.dispatchEvent(new Event("input", { bubbles: true }));
    input.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function getChatInput() {
    return document.querySelector("#chat-msg-input textarea, #chat-msg-input input, .chat-textbox-input textarea, .chat-textbox-input input, textarea.chat-textbox-input, input.chat-textbox-input");
  }

  function setVoiceStatus(msg, isError, isActive) {
    const pill = document.getElementById("chat-voice-status-pill");
    const textSpan = document.getElementById("chat-voice-status-text");
    const micBtn = document.getElementById("chat-mic-toggle-btn");

    if (pill && textSpan) {
      if (isActive) {
        pill.style.display = "inline-flex";
        pill.className = isError ? "voice-status-pill voice-status-error" : "voice-status-pill voice-status-active";
        textSpan.textContent = msg;
      } else if (isError) {
        pill.style.display = "inline-flex";
        pill.className = "voice-status-pill voice-status-error";
        textSpan.textContent = msg;
        setTimeout(function() {
          if (!isListening) pill.style.display = "none";
        }, 6000);
      } else {
        pill.style.display = "none";
      }
    }

    if (micBtn) {
      if (isActive) {
        micBtn.classList.add("recording-pulse");
        micBtn.setAttribute("title", "Listening... Click 🎙️ again to stop");
      } else {
        micBtn.classList.remove("recording-pulse");
        micBtn.setAttribute("title", "Click to speak (Voice Input)");
      }
    }
  }

  function initSpeechEngine() {
    const micBtn = document.getElementById("chat-mic-toggle-btn");
    if (!micBtn) return;
    if (micBtn.dataset.voiceAttached === "true") return;
    micBtn.dataset.voiceAttached = "true";

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    micBtn.addEventListener("click", function(e) {
      e.preventDefault();
      e.stopPropagation();

      const input = getChatInput();
      if (!input) {
        console.warn("LiteratureAI: Chat input not found in DOM.");
        return;
      }

      if (!SpeechRecognition) {
        setVoiceStatus("⚠️ Voice speech not supported in this browser. Please use Chrome or Edge.", true, false);
        return;
      }

      if (isListening) {
        // Stop listening
        if (recognition) {
          try { recognition.stop(); } catch(err) {}
        }
        isListening = false;
        setVoiceStatus("✅ Dictation stopped.", false, false);
        return;
      }

      // Start listening
      try {
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = (navigator.language && navigator.language.startsWith("hi")) ? "hi-IN" : "en-IN";

        let sessionBaseText = input.value ? (input.value.trim() + " ") : "";

        recognition.onstart = function() {
          isListening = true;
          setVoiceStatus("🔴 Listening... Speak now (Hinglish / English). Click 🎙️ again when done.", false, true);
        };

        recognition.onresult = function(event) {
          let interimText = "";
          let finalChunk = "";

          for (let i = event.resultIndex; i < event.results.length; ++i) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
              finalChunk += transcript + " ";
            } else {
              interimText += transcript;
            }
          }

          if (finalChunk) {
            sessionBaseText += finalChunk;
          }

          const displayText = (sessionBaseText + interimText).trim();
          updateInputElement(input, displayText);
        };

        recognition.onerror = function(event) {
          console.warn("Speech recognition error:", event.error);
          isListening = false;
          let errMsg = "⚠️ Speech error: " + event.error;
          if (event.error === "not-allowed" || event.error === "permission-denied") {
            errMsg = "⚠️ Mic permission blocked! Please allow microphone access in your browser URL bar.";
          } else if (event.error === "no-speech") {
            errMsg = "ℹ️ No speech heard. Click 🎙️ to speak again.";
          }
          setVoiceStatus(errMsg, true, false);
        };

        recognition.onend = function() {
          isListening = false;
          setVoiceStatus("", false, false);
        };

        recognition.start();

      } catch(err) {
        console.error("Could not start speech recognition:", err);
        isListening = false;
        setVoiceStatus("⚠️ Could not activate microphone: " + err.message, true, false);
      }
    });
  }

  // ----------------------------------------------------
  // THEME SWITCHING ENGINE (Dark Cyber / Academic Light)
  // ----------------------------------------------------
  function applyLiteratureTheme(theme) {
    const isLight = (theme === 'light');
    const containers = document.querySelectorAll('.gradio-container, .app-container');
    if (isLight) {
      document.documentElement.classList.add('light-theme');
      document.documentElement.classList.remove('dark-theme');
      document.body.classList.add('light-theme');
      document.body.classList.remove('dark-theme');
      containers.forEach(function(c) {
        c.classList.add('light-theme');
        c.classList.remove('dark-theme');
      });
      localStorage.setItem('literatureai_theme', 'light');
    } else {
      document.documentElement.classList.remove('light-theme');
      document.documentElement.classList.add('dark-theme');
      document.body.classList.remove('light-theme');
      document.body.classList.add('dark-theme');
      containers.forEach(function(c) {
        c.classList.remove('light-theme');
        c.classList.add('dark-theme');
      });
      localStorage.setItem('literatureai_theme', 'dark');
    }
    
    const icon = document.getElementById('appThemeIcon');
    const label = document.getElementById('appThemeLabel');
    const track = document.getElementById('appThemeToggleBtn');
    if (icon) icon.innerText = isLight ? '☀️' : '🌙';
    if (label) label.innerText = isLight ? 'Light Academic' : 'Dark Cyber';
    if (track) {
      if (isLight) track.classList.add('active-light');
      else track.classList.remove('active-light');
    }
  }

  window.toggleLiteratureTheme = function() {
    const isCurrentlyLight = document.body.classList.contains('light-theme');
    applyLiteratureTheme(isCurrentlyLight ? 'dark' : 'light');
  };

  function checkThemeSync() {
    const saved = localStorage.getItem('literatureai_theme') || 'dark';
    if (saved === 'light' && !document.body.classList.contains('light-theme')) {
      applyLiteratureTheme('light');
    } else if (saved === 'dark' && document.body.classList.contains('light-theme')) {
      applyLiteratureTheme('dark');
    }
  }

  // ----------------------------------------------------
  // ROBUST TAB NAVIGATION ENGINE (Radio Switcher)
  // ----------------------------------------------------
  window.navigateToTab = function(keyword) {
    if (!keyword) return;
    const key = keyword.toLowerCase();
    
    // Find all radio inputs in sidebar or whole document
    const radioInputs = document.querySelectorAll('.nav-tabs-container input[type="radio"], .sidebar-container input[type="radio"], input[type="radio"]');
    for (let i = 0; i < radioInputs.length; i++) {
      const inp = radioInputs[i];
      const val = (inp.value || "").toLowerCase();
      const parent = inp.closest('label') || inp.parentElement;
      const text = (parent ? parent.textContent : "").toLowerCase();
      
      if (val.includes(key) || text.includes(key)) {
        inp.checked = true;
        inp.click();
        inp.dispatchEvent(new Event("change", { bubbles: true }));
        inp.dispatchEvent(new Event("input", { bubbles: true }));
        return;
      }
    }

    // Fallback: Click label or button directly
    const labels = document.querySelectorAll('.nav-tabs-container label, .sidebar-container label, .nav-tabs-container button, .sidebar-container button');
    for (let j = 0; j < labels.length; j++) {
      const el = labels[j];
      const text = (el.textContent || "").toLowerCase();
      if (text.includes(key)) {
        const inp = el.querySelector('input[type="radio"]');
        if (inp) {
          inp.checked = true;
          inp.click();
          inp.dispatchEvent(new Event("change", { bubbles: true }));
          inp.dispatchEvent(new Event("input", { bubbles: true }));
        } else {
          el.click();
        }
        return;
      }
    }
  };

  // Continuously attach to handle Gradio view-switches and re-renders
  setInterval(initSpeechEngine, 800);
  setInterval(checkThemeSync, 500);

  // Initialize theme on start
  setTimeout(function() {
    const saved = localStorage.getItem('literatureai_theme') || 'dark';
    applyLiteratureTheme(saved);
  }, 100);
})();
</script>
"""


def render_chat_header_html() -> str:
    return f"""
    <div class="chat-header-banner">
      <div class="chat-header-left">
        <div class="chat-avatar-frame">
          <img src="{CHAT_ASSISTANT_IMG}" class="chat-assistant-hero-img" alt="Salim - Research Assistant" />
          <span class="chat-online-dot"></span>
        </div>

        <div class="chat-header-info">
          <div class="chat-assistant-name">
            Salim <span class="chat-title-separator">•</span> <span class="chat-assistant-role">AI Research Assistant</span>
            <span class="chat-badge-status">Online</span>
            <span class="chat-badge-voice">🎙️ Voice Active</span>
          </div>
          <div class="chat-assistant-desc">
            Context-grounded assistant for academic literature review. Supports text input and real-time voice dictation.
          </div>
        </div>
      </div>
      <div class="chat-header-right-action">
        <div class="chat-stats-pill">
          <span class="chat-stat-text">Active Engine: <strong>Groq / Llama 3.3 70B</strong></span>
        </div>
      </div>
    </div>
    """

def render_salim_sidebar_html(paper_count: int = 0, topic: str = "Space Communication Networks") -> str:
    topic_display = topic if len(topic) <= 32 else topic[:29] + "..."
    return f"""
    <div class="ren-agent-card">
      <div class="ren-card-header">
        <div class="ren-portrait-box">
          <img src="{CHAT_ASSISTANT_IMG}" class="ren-full-portrait-img" alt="Salim" />
        </div>
        <div class="ren-meta-box">
          <div class="ren-name-title">Salim</div>
          <div class="ren-subtitle">Literature Review Specialist</div>
        </div>
      </div>

      <div class="ren-session-summary-box">
        <div class="ren-summary-row">
          <span class="summary-label">Session Topic:</span>
          <span class="summary-val">{topic_display}</span>
        </div>
        <div class="ren-summary-row">
          <span class="summary-label">Loaded Papers:</span>
          <span class="summary-val highlight-val">{paper_count}</span>
        </div>
        <div class="ren-summary-row">
          <span class="summary-label">Citation Mode:</span>
          <span class="summary-val">Direct Evidence [1], [2]</span>
        </div>
      </div>
    </div>
    """

def create_chat_view():
    with gr.Column(elem_classes=["chat-view-container"]):
        chat_header_display = gr.HTML(value=render_chat_header_html())

        with gr.Row(elem_classes=["chat-main-row"]):
            # Left Column: Session Context & Quick Actions
            with gr.Column(scale=30, min_width=270, elem_classes=["chat-left-sidebar"]):
                salim_profile_display = gr.HTML(value=render_salim_sidebar_html(0, "Space Communication Networks"))
                
                gr.HTML('<div class="quick-actions-title">Quick Actions</div>')
                with gr.Column(elem_classes=["quick-buttons-col"]):
                    quick_btn_summary = gr.Button("Summarize Loaded Papers", elem_classes=["btn-quick-action"])
                    quick_btn_methods = gr.Button("Extract Methodologies & Datasets", elem_classes=["btn-quick-action"])
                    quick_btn_gaps = gr.Button("Identify Limitations & Gaps", elem_classes=["btn-quick-action"])
                    quick_btn_marl = gr.Button("Explain Key Theoretical Concepts", elem_classes=["btn-quick-action"])

            # Right Column: Chatbot Conversation & Controls
            with gr.Column(scale=70, elem_classes=["chat-right-area"]):
                chatbot = gr.Chatbot(
                    value=INITIAL_WELCOME_MESSAGE,
                    label="Literature Review Chat",
                    height=480,
                    avatar_images=("static/images/user_avatar.png", "static/images/chat_assistant.png"),
                    elem_classes=["literature-chatbot-box"],
                    show_label=False
                )

                # Voice Status Indicator (Live Dictation feedback)
                voice_status_html = gr.HTML(
                    value='<div id="chat-voice-status-pill" class="voice-status-pill" style="display:none;"><span class="voice-pulse-dot"></span><span id="chat-voice-status-text"></span></div>',
                    elem_classes=["chat-voice-status-wrap"]
                )

                # Voice Audio Recorder Panel (Whisper STT mode)
                with gr.Row(visible=False, elem_classes=["chat-voice-row"]) as voice_recorder_row:
                    voice_recorder = gr.Audio(
                        sources=["microphone"],
                        type="filepath",
                        label="Record Audio Clip (Transcribed with Groq Whisper)",
                        elem_classes=["chat-mic-audio-box"]
                    )

                with gr.Row(elem_classes=["chat-input-row"]):
                    msg_input = gr.Textbox(
                        placeholder="Ask Salim anything, or click 🎙️ to speak...",
                        scale=8,
                        lines=1,
                        show_label=False,
                        container=False,
                        elem_classes=["chat-textbox-input"],
                        elem_id="chat-msg-input"
                    )
                    mic_btn = gr.Button(
                        "🎙️",
                        scale=1,
                        min_width=44,
                        elem_classes=["btn-chat-mic"],
                        elem_id="chat-mic-toggle-btn"
                    )

                    send_btn = gr.Button("Send", variant="primary", scale=2, elem_classes=["btn-primary-gradient", "btn-chat-send"])
                    whisper_toggle_btn = gr.Button("🎙️ Whisper Mode", scale=1, min_width=120, elem_classes=["btn-whisper-toggle"])
                    clear_btn = gr.Button("Clear", scale=1, elem_classes=["btn-chat-clear"])

                gr.Examples(
                    examples=[
                        "What papers are currently loaded in the session?",
                        "Which paper proposes a reinforcement learning approach and what were the reported results?",
                        "What simulation tools or datasets were used across the papers?",
                        "Summarize the acknowledged empirical limitations across the papers.",
                        "Compare the consensus protocols suggested for autonomous satellite networks."
                    ],
                    inputs=msg_input,
                    label="Suggested Questions"
                )

    return {
        "chatbot": chatbot,
        "msg_input": msg_input,
        "mic_btn": mic_btn,
        "whisper_toggle_btn": whisper_toggle_btn,
        "voice_recorder": voice_recorder,
        "voice_recorder_row": voice_recorder_row,
        "send_btn": send_btn,
        "clear_btn": clear_btn,
        "chat_header_display": chat_header_display,
        "salim_profile_display": salim_profile_display,
        "quick_btn_summary": quick_btn_summary,
        "quick_btn_methods": quick_btn_methods,
        "quick_btn_gaps": quick_btn_gaps,
        "quick_btn_marl": quick_btn_marl
    }
