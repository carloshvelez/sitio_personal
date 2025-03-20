import  PATIENTS  from './patients.js';

document.addEventListener("DOMContentLoaded", function(){


let config = {
    patientId: 'valentina-tca',
    provider: 'google',
    maxTokens: 500,
    therapistName: '',    
    openai: { key: '' },
    google: { key: '', model: 'gemini-2.0-flash' },
    deepseek: { key: '' },
    ollama: { url: 'http://localhost:11434', model: 'phi4' }
};

let conversationHistory = [];

// Inicializar selector de pacientes
function initPatientSelector() {
    const select = document.getElementById('patient-select');
    Object.values(PATIENTS).forEach(patient => {
        const option = document.createElement('option');
        option.value = patient.id;
        option.textContent = `${patient.name}, ${patient.age} años (${patient.description})`;
        select.appendChild(option);
    });
}

function changePatient() {
    const patientId = document.getElementById('patient-select').value;
    config.patientId = patientId;
    const patient = getCurrentPatient();
    
    // Update patient info display
    document.getElementById('patient-name').textContent = `Atendiendo a ${patient.name}`;
    document.getElementById('patient-details').textContent = `${patient.age} años - ${patient.description}`;
    
    newConversation();
    checkConfiguration();
}

function getCurrentPatient() {
    return PATIENTS[config.patientId];
}

// Funciones de configuración
function toggleConfig() {
    const configPanel = document.getElementById('config-panel');
    const overlay = document.querySelector('.modal-overlay');
    configPanel.classList.toggle('active');
    overlay.classList.toggle('active');
    const configIcon= document.getElementById('config-icon');
    if (configPanel.classList.value === "active") {
        configIcon.className='fa-solid fa-xmark'    
    }
    else{
        configIcon.className='menu-icon'
    }

    updateProviderSection();
}

function updateProviderSection() {
    const provider = document.getElementById('llm-provider').value;
    document.querySelectorAll('.config-section').forEach(el => {
        el.classList.remove('visible');
    });
    const configSection = document.getElementById(`${provider}-config`);
    if (configSection) {
        configSection.classList.add('visible');
    } else {
        console.error(`Configuration section for provider ${provider} not found`);
    }
}

function saveConfig() {
    config.patientId = document.getElementById('patient-select').value;
    config.therapistName = document.getElementById('therapist-name').value;
    config.provider = document.getElementById('llm-provider').value;
    config.maxTokens = parseInt(document.getElementById('max-tokens').value);
    config.openai.key = document.getElementById('openai-key').value;
    config.google.key = document.getElementById('google-key').value;
    config.google.model = document.getElementById('google-model').value;
    config.deepseek.key = document.getElementById('deepseek-key').value;
    config.ollama.url = document.getElementById('ollama-url').value;
    config.ollama.model = document.getElementById('ollama-model').value;
    localStorage.setItem('llm-config', JSON.stringify(config));

    
    
    // Show toast notification
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = 'Configuración guardada!';
    document.body.appendChild(toast);
    
    // Show the toast
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Remove the toast after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => document.body.removeChild(toast), 300);
    }, 1000);
    
    toggleConfig(); // Close the configuration modal            
    checkConfiguration();
}

function loadConfig() {
    const saved = localStorage.getItem('llm-config');
    if (saved) config = JSON.parse(saved);
    
    // Cargar paciente
    document.getElementById('patient-select').value = config.patientId;
    
    document.getElementById('max-tokens').value = config.maxTokens || 500;
    document.getElementById('llm-provider').value = config.provider;
    document.getElementById('openai-key').value = config.openai.key;
    document.getElementById('google-key').value = config.google.key;
    document.getElementById('google-model').value = config.google.model;
    document.getElementById('deepseek-key').value = config.deepseek.key;
    document.getElementById('ollama-url').value = config.ollama.url;
    document.getElementById('ollama-model').value = config.ollama.model;
    toggleConfig();
}

// Funciones del chat
function newConversation() {
    conversationHistory = [];
    document.getElementById('messages').innerHTML = '';
}

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    if (!message) return;

    let privacyWarning = document.getElementById('privacy-warning');
    if (privacyWarning){
        privacyWarning.remove()        
    }

    addMessage(message, 'user');
    userInput.value = '';

    try {
        const response = await fetchLLMResponse(message);
        addMessage(response, 'bot');
        
        conversationHistory.push({ role: 'user', content: message });
        conversationHistory.push({ role: 'assistant', content: response });
        
    } catch (error) {
        addMessage(`Error: ${error.message}`, 'bot');
    }
}

async function fetchLLMResponse(prompt) {
    const patient = getCurrentPatient();
    const messages = [
        { role: 'system', content: patient.prompt },
        ...conversationHistory,
        { role: 'user', content: prompt }
    ];

    switch(config.provider) {
        case 'openai': return fetchOpenAI(messages);
        case 'google': return fetchGoogleAI(messages);
        case 'deepseek': return fetchDeepSeek(messages);
        case 'ollama': return fetchOllama(messages);
        default: throw new Error('Proveedor no configurado');
    }
}

async function fetchOpenAI(messages) {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${config.openai.key}`
        },
        body: JSON.stringify({
            model: 'gpt-4o-mini',
            messages: messages,
            temperature: 0.7,
            max_tokens: config.maxTokens
        })
    });
    
    const data = await response.json();
    return data.choices[0].message.content;
}

async function fetchGoogleAI(messages) {
    const contents = messages.map(m => ({
        role: m.role === 'system' ? 'user' : m.role,
        parts: [{ text: m.content }]
    }));
    
    const response = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${config.google.model}:generateContent?key=${config.google.key}`,
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contents: contents,
                generationConfig: {
                    temperature: 0.7,
                    maxOutputTokens: config.maxTokens
                }
            })
        }
    );
    
    const data = await response.json();
    return data.candidates[0].content.parts[0].text;
}

async function fetchOllama(messages) {
try {
// Convertir mensajes al formato específico de Ollama
const ollamaMessages = messages.map(msg => ({
    role: msg.role === 'system' ? 'assistant' : msg.role,
    content: msg.content
}));

const response = await fetch(`${config.ollama.url}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        model: config.ollama.model,
        messages: ollamaMessages,
        options: {
            temperature: 0.7,
            num_predict: config.maxTokens
        },
        stream: false
    })
});

if (!response.ok) {
    throw new Error(`Error HTTP: ${response.status} - ${await response.text()}`);
}

const data = await response.json();
return data.message.content;
} catch (error) {
console.error('Error en Ollama:', error);
throw new Error(`Problema con Ollama: ${error.message}. Verifica: 
1. Ollama corriendo (ollama serve)
2. Modelo instalado (ollama pull ${config.ollama.model})
3. URL correcta en configuración`);
}
}

function addMessage(text, sender) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = text;
    messageDiv.id = `msg-${Date.now()}-${Math.random().toString(16).slice(2)}`;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }


// Funciones de exportación
function exportToPDF() {
if (conversationHistory.length === 0) {
alert("No hay conversación para exportar");
return;
}

if (config.therapistName === "") {
alert("Ingresa el nombre del terapeuta en la configuración");
return;
}



const patient = getCurrentPatient();
const doc = new jspdf.jsPDF();

// Configuración inicial
const margin = 15;
let yPos = 20;
const lineHeight = 8;
const pageHeight = 280;
const textWidth = 180; // Ancho máximo del texto

// Encabezado
doc.setFontSize(18);
doc.text(`Informe de Sesión - ${patient.name}`, margin, yPos);
yPos += 15;

// Metadatos
doc.setFontSize(12);
doc.text(`Fecha: ${new Date().toLocaleDateString()}`, margin, yPos);
yPos += lineHeight;
doc.text(`Terapeuta: ${config.therapistName}`, margin, yPos);
yPos += lineHeight;
doc.text(`Usuario: ${patient.name}`, margin, yPos);
yPos += lineHeight;
doc.text(`Edad: ${patient.age} años`, margin, yPos);
yPos += lineHeight;
doc.text(`Problema: ${patient.description}`, margin, yPos);
yPos += 15;

// Línea divisoria
doc.setLineWidth(0.5);
doc.line(margin, yPos, 200 - margin, yPos);
yPos += 10;

// Conversación
doc.setFontSize(12);
const messages = document.querySelectorAll('.message');

messages.forEach((msg, index) => {
if (yPos > pageHeight) {
    doc.addPage();
    yPos = margin;
}

const sender = msg.classList.contains('user-message') ? 'Terapeuta' : patient.name;
const text = `${sender}: ${msg.textContent}`;

doc.setFont(sender === 'Terapeuta' ? 'helvetica' : 'times', 'normal');
doc.setTextColor(sender === 'Terapeuta'? '#0793a8' : '#000000');


const splitText = doc.splitTextToSize(text, 180);

splitText.forEach((line, lineIndex) => {
    if (yPos > pageHeight) {
        doc.addPage();
        yPos = margin;
    }
    doc.text(line, margin, yPos);
    yPos += lineHeight;
});

yPos += lineHeight/2; // Espacio entre mensajes
});

// Guardar PDF
doc.save(`Conversacion_${patient.name}_${new Date().toISOString().slice(0,10)}.pdf`);
}

// Inicialización al cargar
function checkConfiguration() {
    const patient = document.getElementById('patient-select').value;
    const therapist = document.getElementById('therapist-name').value;
    const provider = document.getElementById('llm-provider').value;
    const providerKey = document.getElementById(`${provider}-key`)?.value;
    
    let isConfigured = false
    if (provider === 'ollama'){        
        isConfigured = patient && therapist
        console.log(isConfigured)
    } else{
        isConfigured = patient && therapist && providerKey;
    }
    
    
    // Add visual feedback for empty therapist name
    const therapistInput = document.getElementById('therapist-name');
    if (!therapist) {
        therapistInput.style.border = '2px solid #dc3545';
        therapistInput.style.boxShadow = '0 0 0 0.2rem rgba(220, 53, 69, 0.25)';
    } else {
        therapistInput.style.border = '';
        therapistInput.style.boxShadow = '';
    }

    // Add input event listener to remove highlight when typing
    therapistInput.addEventListener('input', function() {
        this.style.border = '';
        this.style.boxShadow = '';
    });
    
    document.getElementById('setup-message').style.display = isConfigured ? 'none' : 'block';
    document.getElementById('user-input').disabled = !isConfigured;
    document.getElementById('user-input').placeholder = isConfigured ? 
        'Escribe tu intervención...' : 'Complete la configuración antes de comenzar...';
    

        if (isConfigured && !document.getElementById('privacy-warning')){
            // Add privacy warning
            let privacyWarning = document.createElement("p")
            privacyWarning.id = "privacy-warning"            
            privacyWarning.textContent = "Empat IA no recolecta ningún dato. El proveedor de IA puede guardar y analizar tu conversación. No uses información confidencial. Ahora puedes iniciar la conversación"
            let messagesContainer = document.getElementById("messages")
            messagesContainer.appendChild(privacyWarning)
            console.log("hola")
        }

    return isConfigured;
}



window.onload = () => {
    initPatientSelector();
    loadConfig();
    
    // Set initial patient info
    const initialPatient = getCurrentPatient();
    document.getElementById('patient-name').textContent = `Atendiendo a ${initialPatient.name}`;
    document.getElementById('patient-details').textContent = `${initialPatient.age} años - ${initialPatient.description}`;
    
    // Add event listeners
    document.getElementById('save-config-btn').addEventListener('click', saveConfig);
    document.getElementById('config-toggle').addEventListener('click', toggleConfig);
    document.getElementById('modal-overlay').addEventListener('click', toggleConfig);
    document.getElementById('patient-select').addEventListener('change', changePatient);
    document.getElementById('llm-provider').addEventListener('change', updateProviderSection);
    document.getElementById('send-message-btn').addEventListener('click', sendMessage);
    document.getElementById('new-conversation-btn').addEventListener('click', newConversation);
    document.getElementById('export-pdf-btn').addEventListener('click', exportToPDF);
    document.getElementById('user-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    
    checkConfiguration();
};
})