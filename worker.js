const JSON_HEADERS = {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
};

const jsonResponse = (body, status = 200) =>
    new Response(JSON.stringify(body), { status, headers: JSON_HEADERS });

const cleanSingleLine = (value, maxLength) =>
    String(value ?? '').replace(/[\r\n\t]+/g, ' ').replace(/\s{2,}/g, ' ').trim().slice(0, maxLength);

const cleanMessage = (value, maxLength) => String(value ?? '').replace(/\r\n?/g, '\n').trim().slice(0, maxLength);

const escapeHtml = (value) =>
    value.replace(/[&<>"']/g, (character) => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;',
    })[character]);

const isEmail = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) && value.length <= 254;

async function handleContact(request, env) {
    if (request.method !== 'POST') {
        return jsonResponse({ message: 'POST 요청만 사용할 수 있습니다.' }, 405);
    }

    const requestUrl = new URL(request.url);
    const origin = request.headers.get('Origin');
    if (origin && origin !== requestUrl.origin) {
        return jsonResponse({ message: '허용되지 않은 요청입니다.' }, 403);
    }

    const contentLength = Number(request.headers.get('Content-Length') || 0);
    if (contentLength > 20_000) {
        return jsonResponse({ message: '문의 내용이 너무 깁니다.' }, 413);
    }

    let input;
    try {
        input = await request.json();
    } catch {
        return jsonResponse({ message: '올바른 문의 형식이 아닙니다.' }, 400);
    }

    if (input.website) {
        return jsonResponse({ ok: true });
    }

    const startedAt = Number(input.startedAt);
    if (!Number.isFinite(startedAt) || Date.now() - startedAt < 1500) {
        return jsonResponse({ message: '잠시 후 다시 제출해 주세요.' }, 400);
    }

    const name = cleanSingleLine(input.name, 60);
    const email = cleanSingleLine(input.email, 254);
    const subject = cleanSingleLine(input.subject, 120);
    const message = cleanMessage(input.message, 5000);

    if (!name || !isEmail(email) || !subject || !message || input.consent !== 'yes') {
        return jsonResponse({ message: '필수 항목과 개인정보 동의를 확인해 주세요.' }, 400);
    }

    if (!env.RESEND_API_KEY || !env.CONTACT_TO_EMAIL || !env.CONTACT_FROM_EMAIL) {
        console.error('Contact email bindings are not configured.');
        return jsonResponse({ message: '현재 문의 메일 기능을 준비 중입니다. 이메일로 직접 문의해 주세요.' }, 503);
    }

    const safeName = escapeHtml(name);
    const safeEmail = escapeHtml(email);
    const safeSubject = escapeHtml(subject);
    const safeMessage = escapeHtml(message).replace(/\n/g, '<br>');
    const mailSubject = `[홈페이지 문의] ${subject}`;

    let resendResponse;
    try {
        resendResponse = await fetch('https://api.resend.com/emails', {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${env.RESEND_API_KEY}`,
                'Content-Type': 'application/json',
                'Idempotency-Key': crypto.randomUUID(),
            },
            body: JSON.stringify({
                from: env.CONTACT_FROM_EMAIL,
                to: [env.CONTACT_TO_EMAIL],
                reply_to: email,
                subject: mailSubject,
                text: `이름: ${name}\n이메일: ${email}\n문의 제목: ${subject}\n\n${message}`,
                html: `
                    <h2>연구단 홈페이지 문의</h2>
                    <p><strong>이름:</strong> ${safeName}</p>
                    <p><strong>이메일:</strong> ${safeEmail}</p>
                    <p><strong>문의 제목:</strong> ${safeSubject}</p>
                    <hr>
                    <p style="line-height:1.7">${safeMessage}</p>
                `,
            }),
        });
    } catch (error) {
        console.error('Resend request failed:', error);
        return jsonResponse({ message: '메일 전송에 실패했습니다. 잠시 후 다시 시도해 주세요.' }, 502);
    }

    if (!resendResponse.ok) {
        const errorText = await resendResponse.text();
        console.error('Resend error:', resendResponse.status, errorText);
        return jsonResponse({ message: '메일 전송에 실패했습니다. 잠시 후 다시 시도해 주세요.' }, 502);
    }

    return jsonResponse({ ok: true });
}

export default {
    async fetch(request, env) {
        const url = new URL(request.url);
        if (url.pathname === '/api/contact') {
            return handleContact(request, env);
        }
        return env.ASSETS.fetch(request);
    },
};
