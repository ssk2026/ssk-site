(() => {
    const form = document.querySelector('[data-contact-form]');
    if (!form) return;

    const status = form.querySelector('[data-contact-status]');
    const submitButton = form.querySelector('button[type="submit"]');
    const startedAt = form.elements.namedItem('startedAt');
    startedAt.value = String(Date.now());

    const setStatus = (message, type = '') => {
        status.textContent = message;
        status.classList.remove('is-success', 'is-error');
        if (type) status.classList.add(`is-${type}`);
    };

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (!form.reportValidity()) return;

        submitButton.disabled = true;
        submitButton.textContent = '전송 중...';
        setStatus('문의 내용을 전송하고 있습니다.');

        try {
            const formData = new FormData(form);
            const payload = Object.fromEntries(formData.entries());
            const response = await fetch(form.action, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            const result = await response.json().catch(() => ({}));

            if (!response.ok) {
                throw new Error(result.message || '문의 전송에 실패했습니다. 잠시 후 다시 시도해 주세요.');
            }

            form.reset();
            startedAt.value = String(Date.now());
            setStatus('문의가 정상적으로 접수되었습니다. 확인 후 입력하신 이메일로 답변드리겠습니다.', 'success');
        } catch (error) {
            setStatus(error.message || '문의 전송에 실패했습니다. 잠시 후 다시 시도해 주세요.', 'error');
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = '문의 보내기';
        }
    });
})();
