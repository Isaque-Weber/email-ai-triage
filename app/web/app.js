document.addEventListener('DOMContentLoaded', () => {
    // References to DOM elements
    const form = document.getElementById('triageForm');
    const resultSection = document.getElementById('resultSection');
    const errorMsg = document.getElementById('errorMsg');
    const loading = document.getElementById('loading');
    const processBtn = document.getElementById('processBtn');
    const emailFile = document.getElementById('emailFile');
    const dropZone = document.getElementById('dropZone');
    const fileInfo = document.getElementById('fileInfo');
    const emailText = document.getElementById('emailText');

    // Result Elements
    const badgeCategory = document.getElementById('badgeCategory');
    const confidenceVal = document.getElementById('confidenceVal');
    const confidenceBar = document.getElementById('confidenceBar');
    const suggestedReply = document.getElementById('suggestedReply');
    const copyBtn = document.getElementById('copyBtn');

    let currentResult = null;
    let originalTextCache = "";

    // Drag and Drop Logic
    dropZone.addEventListener('click', () => emailFile.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        if (e.dataTransfer.files.length) {
            emailFile.files = e.dataTransfer.files;
            updateFileInfo(e.dataTransfer.files[0].name);
        }
    });

    emailFile.addEventListener('change', () => {
        if (emailFile.files.length) {
            updateFileInfo(emailFile.files[0].name);
        }
    });

    function updateFileInfo(name) {
        fileInfo.innerHTML = `
            <span>Arquivo: <strong>${name}</strong></span>
            <button type="button" id="removeFileBtn" class="btn-text" title="Remover arquivo">❌</button>
        `;
        fileInfo.classList.remove('hidden');
        emailText.value = ''; 
        emailText.disabled = true;
        emailText.placeholder = "Arquivo selecionado. Remova para digitar texto.";

        const btn = document.getElementById('removeFileBtn');
        btn.addEventListener('click', (e) => {
            e.stopPropagation(); // Previne que o click suba para o dropZone
            removeFile();
        });
    }

    function removeFile() {
        emailFile.value = ''; // Clear input
        fileInfo.classList.add('hidden');
        fileInfo.innerHTML = '';
        emailText.disabled = false;
        emailText.placeholder = "Ex: Olá, gostaria de saber o status do meu pedido...";
        currentResult = null; 
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Reset UI
        errorMsg.classList.add('hidden');
        resultSection.classList.add('hidden');
        loading.classList.remove('hidden');
        processBtn.disabled = true;

        const formData = new FormData();
        
        if (emailFile.files.length > 0) {
            formData.append('file', emailFile.files[0]);
        } else if (emailText.value.trim()) {
            formData.append('text', emailText.value);
            originalTextCache = emailText.value;
        } else {
            showError("Por favor, insira um texto ou selecione um arquivo.");
            loading.classList.add('hidden');
            processBtn.disabled = false;
            return;
        }

        try {
            const response = await fetch('/api/process', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Erro ao processar email.');
            }

            const data = await response.json();
            currentResult = data;
            
            // Show Result
            showResult(data);

        } catch (err) {
            showError(err.message);
        } finally {
            loading.classList.add('hidden');
            processBtn.disabled = false;
        }
    });

    copyBtn.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent duplicate submit
        if (suggestedReply.value) {
            navigator.clipboard.writeText(suggestedReply.value)
                .then(() => {
                    const originalText = copyBtn.innerText;
                    copyBtn.innerText = "Copiado!";
                    setTimeout(() => copyBtn.innerText = originalText, 2000);
                });
        }
    });

    // Feedback Buttons
    const feedbackBtns = document.querySelectorAll('.feedback-buttons button');
    feedbackBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            if (!currentResult) return;

            const isCorrect = btn.dataset.correct === "true";
            const correctLabel = isCorrect 
                ? currentResult.category 
                : (currentResult.category === "Produtivo" ? "Improdutivo" : "Produtivo");

            try {
                await fetch('/api/feedback', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        text: originalTextCache || "[Arquivo Enviado]",
                        predicted: currentResult.category,
                        correct: correctLabel
                    })
                });
                
                const msg = document.getElementById('feedbackMsg');
                msg.classList.remove('hidden');
                setTimeout(() => msg.classList.add('hidden'), 3000);

            } catch (error) {
                console.error("Erro ao enviar feedback", error);
            }
        });
    });

    function showResult(data) {
        resultSection.classList.remove('hidden');

        // Category
        badgeCategory.innerText = data.category;
        badgeCategory.className = `badge ${data.category.toLowerCase()}`;

        // Confidence
        confidenceVal.innerText = `${data.confidence.toFixed(1)}%`;
        confidenceBar.style.width = `${data.confidence}%`;

        // Reply
        suggestedReply.value = data.suggested_reply;

        // Source
        const sourceBadge = document.getElementById('replySourceBadge');
        if (data.reply_source) {
            sourceBadge.innerText = `Fonte: ${data.reply_source}`;
            // Optional: visual distinction
            if (data.reply_source.includes("Gemini")) {
                sourceBadge.style.backgroundColor = "#e0e7ff"; // Blueish
                sourceBadge.style.color = "#3730a3";
            } else {
                sourceBadge.style.backgroundColor = "#f3f4f6"; // Grayish
                sourceBadge.style.color = "#374151";
            }
        }

        // Smooth scroll
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }

    function showError(msg) {
        errorMsg.innerText = msg;
        errorMsg.classList.remove('hidden');
    }
});
