(function () {
    "use strict";

    function setHidden(element, hidden) {
        element.classList.toggle("static-list-hidden", hidden);
        element.hidden = hidden;
    }

    function updateUrl(params) {
        var query = params.toString();
        var nextUrl = window.location.pathname + (query ? "?" + query : "");
        window.history.pushState({}, "", nextUrl);
    }

    document.querySelectorAll("[data-static-list]").forEach(function (root) {
        var form = root.querySelector("form");
        var items = Array.from(root.querySelectorAll("[data-static-item]"));
        var emptyStates = Array.from(root.querySelectorAll("[data-static-empty]"));
        var pagination = root.querySelector("[data-static-pagination]");
        var count = root.querySelector(".briefing-count span, .notice-top p span");
        var pageSize = Math.max(1, Number(root.dataset.pageSize) || 10);

        function render() {
            var params = new URLSearchParams(window.location.search);
            var query = (params.get("q") || "").trim().toLocaleLowerCase("ko");
            var searchType = params.get("type") || "title";
            var requestedPage = Math.max(1, Number(params.get("page")) || 1);
            var matches = items.filter(function (item) {
                var haystack = searchType === "content"
                    ? item.dataset.searchContent || ""
                    : item.dataset.searchTitle || "";
                return !query || haystack.toLocaleLowerCase("ko").includes(query);
            });
            var totalPages = Math.max(1, Math.ceil(matches.length / pageSize));
            var currentPage = Math.min(requestedPage, totalPages);
            var firstIndex = (currentPage - 1) * pageSize;
            var visibleItems = new Set(matches.slice(firstIndex, firstIndex + pageSize));

            items.forEach(function (item) {
                setHidden(item, !visibleItems.has(item));
            });
            emptyStates.forEach(function (emptyState) {
                setHidden(emptyState, matches.length !== 0);
            });
            if (count) {
                count.textContent = String(matches.length);
            }

            if (form) {
                var queryInput = form.querySelector('[name="q"]');
                var typeInput = form.querySelector('[name="type"]');
                if (queryInput) queryInput.value = params.get("q") || "";
                if (typeInput) typeInput.value = searchType;
            }

            if (!pagination) return;
            pagination.replaceChildren();
            if (matches.length === 0 || totalPages === 1) return;

            function addPageLink(label, page, active) {
                var link = document.createElement("a");
                var linkParams = new URLSearchParams(window.location.search);
                linkParams.set("page", String(page));
                link.href = "?" + linkParams.toString();
                link.textContent = label;
                if (active) link.classList.add("active");
                link.addEventListener("click", function (event) {
                    event.preventDefault();
                    updateUrl(linkParams);
                    render();
                    root.scrollIntoView({ behavior: "smooth", block: "start" });
                });
                pagination.appendChild(link);
            }

            if (currentPage > 1) {
                addPageLink("처음", 1, false);
                addPageLink("이전", currentPage - 1, false);
            }
            for (var page = 1; page <= totalPages; page += 1) {
                addPageLink(String(page), page, page === currentPage);
            }
            if (currentPage < totalPages) {
                addPageLink("다음", currentPage + 1, false);
                addPageLink("마지막", totalPages, false);
            }
        }

        if (form) {
            form.addEventListener("submit", function (event) {
                event.preventDefault();
                var formData = new FormData(form);
                var params = new URLSearchParams();
                var query = String(formData.get("q") || "").trim();
                var type = String(formData.get("type") || "title");
                if (query) params.set("q", query);
                if (form.querySelector('[name="type"]')) params.set("type", type);
                updateUrl(params);
                render();
            });
        }

        window.addEventListener("popstate", render);
        render();
    });
}());
