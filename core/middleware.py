from django.conf import settings


class ProposalPdfFrameOptionsMiddleware:
    """
    Allow same-origin framing for proposal PDFs so they can render in iframe.
    Other routes keep default clickjacking protection.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self._proposal_prefix = f"{settings.MEDIA_URL}proposals/"

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith(self._proposal_prefix):
            response["X-Frame-Options"] = "SAMEORIGIN"

        return response

