document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('qrForm');
  const contentInput = document.getElementById('id_content');
  const fillColorInput = document.getElementById('id_fill_color');
  const backColorInput = document.getElementById('id_back_color');
  const boxSizeInput = document.getElementById('id_box_size');
  const errorCorrectionInput = document.getElementById('id_error_correction');
  
  const generateBtn = document.getElementById('generateBtn');
  const btnSpinner = document.getElementById('btnSpinner');
  const btnText = document.getElementById('btnText');
  
  const pasteBtn = document.getElementById('pasteBtn');
  const clearBtn = document.getElementById('clearBtn');
  const settingsToggle = document.getElementById('settingsToggle');
  const settingsPanel = document.getElementById('settingsPanel');
  
  const qrImage = document.getElementById('qrImage');
  const qrPlaceholder = document.getElementById('qrPlaceholder');
  const qrDetails = document.getElementById('qrDetails');
  const qrUrlBadge = document.getElementById('qrUrlBadge');
  const actionButtons = document.getElementById('actionButtons');
  
  const downloadPngBtn = document.getElementById('downloadPngBtn');
  const downloadSvgBtn = document.getElementById('downloadSvgBtn');
  const copyImageBtn = document.getElementById('copyImageBtn');
  const copyLinkBtn = document.getElementById('copyLinkBtn');
  
  const historySection = document.getElementById('historySection');
  const historyList = document.getElementById('historyList');
  const clearHistoryBtn = document.getElementById('clearHistoryBtn');
  const toastContainer = document.getElementById('toastContainer');

  let currentQrDataUri = qrImage?.dataset?.initialUri || null;
  let currentContent = contentInput?.value || '';

  // Toast notification system
  function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        ${type === 'success' ? '<path d="M20 6L9 17l-5-5"/>' : '<circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>'}
      </svg>
      <span>${message}</span>
    `;
    toastContainer.appendChild(toast);
    requestAnimationFrame(() => toast.classList.add('show'));
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  }

  // Toggle settings panel
  if (settingsToggle && settingsPanel) {
    settingsToggle.addEventListener('click', () => {
      const isHidden = settingsPanel.classList.toggle('hidden');
      settingsToggle.querySelector('.toggle-arrow').textContent = isHidden ? '▼' : '▲';
    });
  }

  // Color chips preset
  document.querySelectorAll('.color-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const color = chip.dataset.color;
      if (fillColorInput) {
        fillColorInput.value = color;
      }
      if (contentInput.value.trim()) {
        generateQr();
      }
    });
  });

  // Preset pill clicks
  document.querySelectorAll('.pill-tag').forEach(pill => {
    pill.addEventListener('click', () => {
      contentInput.value = pill.dataset.url;
      contentInput.focus();
      generateQr();
    });
  });

  // Paste from clipboard button
  if (pasteBtn) {
    pasteBtn.addEventListener('click', async () => {
      try {
        const text = await navigator.clipboard.readText();
        if (text) {
          contentInput.value = text.trim();
          showToast('Pasted link from clipboard');
          generateQr();
        }
      } catch (err) {
        contentInput.focus();
        showToast('Please paste manually using Ctrl+V', 'error');
      }
    });
  }

  // Clear button
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      contentInput.value = '';
      contentInput.focus();
    });
  }

  // Submit via AJAX
  async function generateQr() {
    const content = contentInput.value.trim();
    if (!content) {
      showToast('Please enter or paste a link first', 'error');
      contentInput.focus();
      return;
    }

    setLoading(true);

    const formData = new FormData(form);

    try {
      const response = await fetch(form.action || window.location.pathname, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'Accept': 'application/json',
        },
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.success) {
        updateQrDisplay(data.qr_data_uri, data.content);
        saveToHistory(data.content);
        showToast('QR Code generated successfully!');
      } else {
        const errorMsg = data.errors?.content?.[0]?.message || data.error || 'Failed to generate QR code.';
        showToast(errorMsg, 'error');
      }
    } catch (err) {
      console.error(err);
      // Fallback: standard form submit
      form.submit();
    } finally {
      setLoading(false);
    }
  }

  function setLoading(isLoading) {
    if (isLoading) {
      btnSpinner.style.display = 'inline-block';
      btnText.textContent = 'Generating...';
      generateBtn.disabled = true;
    } else {
      btnSpinner.style.display = 'none';
      btnText.textContent = 'Generate QR Code';
      generateBtn.disabled = false;
    }
  }

  function updateQrDisplay(dataUri, content) {
    currentQrDataUri = dataUri;
    currentContent = content;

    qrImage.src = dataUri;
    qrImage.style.display = 'block';
    qrPlaceholder.style.display = 'none';

    qrUrlBadge.textContent = content;
    qrUrlBadge.href = content.startsWith('http://') || content.startsWith('https://') ? content : '#';
    qrUrlBadge.title = content;
    qrDetails.style.display = 'block';

    actionButtons.style.display = 'grid';
  }

  // Handle form submission
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      generateQr();
    });
  }

  // Download buttons
  if (downloadPngBtn) {
    downloadPngBtn.addEventListener('click', (e) => {
      e.preventDefault();
      if (!currentContent) return;
      const downloadUrl = `/download/?content=${encodeURIComponent(currentContent)}&fill_color=${encodeURIComponent(fillColorInput.value)}&back_color=${encodeURIComponent(backColorInput.value)}&box_size=${encodeURIComponent(boxSizeInput.value)}&error_correction=${encodeURIComponent(errorCorrectionInput.value)}&format=png`;
      window.location.href = downloadUrl;
      showToast('Downloading PNG image...');
    });
  }

  if (downloadSvgBtn) {
    downloadSvgBtn.addEventListener('click', (e) => {
      e.preventDefault();
      if (!currentContent) return;
      const downloadUrl = `/download/?content=${encodeURIComponent(currentContent)}&fill_color=${encodeURIComponent(fillColorInput.value)}&back_color=${encodeURIComponent(backColorInput.value)}&box_size=${encodeURIComponent(boxSizeInput.value)}&error_correction=${encodeURIComponent(errorCorrectionInput.value)}&format=svg`;
      window.location.href = downloadUrl;
      showToast('Downloading SVG vector...');
    });
  }

  // Copy Image to clipboard
  if (copyImageBtn) {
    copyImageBtn.addEventListener('click', async () => {
      if (!currentQrDataUri) return;

      try {
        const res = await fetch(currentQrDataUri);
        const blob = await res.blob();
        await navigator.clipboard.write([
          new ClipboardItem({ 'image/png': blob })
        ]);
        showToast('QR Code image copied to clipboard!');
      } catch (err) {
        showToast('Clipboard image copy not supported on this browser', 'error');
      }
    });
  }

  // Copy target link
  if (copyLinkBtn) {
    copyLinkBtn.addEventListener('click', async () => {
      if (!currentContent) return;
      try {
        await navigator.clipboard.writeText(currentContent);
        showToast('Link copied to clipboard!');
      } catch (err) {
        showToast('Could not copy link', 'error');
      }
    });
  }

  // History management via localStorage
  const HISTORY_KEY = 'qr_generator_recent_v1';

  function getHistory() {
    try {
      return JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
    } catch {
      return [];
    }
  }

  function saveToHistory(text) {
    if (!text) return;
    let list = getHistory().filter(item => item !== text);
    list.unshift(text);
    if (list.length > 6) list = list.slice(0, 6);
    try {
      localStorage.setItem(HISTORY_KEY, JSON.stringify(list));
      renderHistory();
    } catch (e) {
      console.warn('LocalStorage error:', e);
    }
  }

  function renderHistory() {
    const list = getHistory();
    if (!historySection || !historyList) return;

    if (list.length === 0) {
      historySection.style.display = 'none';
      return;
    }

    historySection.style.display = 'block';
    historyList.innerHTML = '';

    list.forEach(item => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'history-item';
      btn.title = item;
      btn.innerHTML = `
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
        </svg>
        <span>${escapeHtml(item.length > 25 ? item.substring(0, 22) + '...' : item)}</span>
      `;
      btn.addEventListener('click', () => {
        contentInput.value = item;
        generateQr();
      });
      historyList.appendChild(btn);
    });
  }

  if (clearHistoryBtn) {
    clearHistoryBtn.addEventListener('click', () => {
      localStorage.removeItem(HISTORY_KEY);
      renderHistory();
      showToast('Recent history cleared');
    });
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // Initialize display
  if (currentQrDataUri && qrImage) {
    updateQrDisplay(currentQrDataUri, currentContent);
  }
  renderHistory();
});
