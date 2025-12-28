const form = document.getElementById("chat-form");
const output = document.getElementById("chat-output");
const loader = document.getElementById("loader");

function scrollToBottom() {
    output.scrollTo({
        top: output.scrollHeight,
        behavior: "smooth"
    });
}


form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const queryInput = document.getElementById("query-input");
    const query = queryInput.value.trim();
    if (!query) return;

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Show user message
    output.innerHTML += `
        <div class="chat-message user">
            <div class="bubble">${query}</div>
        </div>
    `;

    queryInput.value = "";
    loader.classList.remove("hidden");

    // Extract cid
    const parts = window.location.pathname.split("/");
    const cid = parts[3] || null;

    let url = "/budget/chatbot/";
    if (cid) url += cid + "/";

    let formData = new FormData();
    formData.append("query", query);

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "X-CSRFToken": csrfToken },
            body: formData,
        });

        const data = await response.json();

        if (data.cid) {
            history.replaceState({}, "", `/budget/chatbot/${data.cid}/`);
        }

        const markdownHTML = marked.parse(data.message);
        console.log(markdownHTML)
        output.innerHTML += `
            <div class="chat-message bot">
                <div class="bubble">${markdownHTML}</div>
            </div>
        `;

    } catch (err) {
        output.innerHTML += `
            <div class="chat-message bot error">
                <div class="bubble">⚠️ Something went wrong. Please try again.</div>
            </div>
        `;
    } finally {
        loader.classList.add("hidden");
        scrollToBottom();

    }
});
