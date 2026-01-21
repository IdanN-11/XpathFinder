async function generate() {
    const url = document.getElementById("url").value;
    const html = document.getElementById("html").value;
    const prompt = document.getElementById("prompt").value;

    document.getElementById("output").innerText = "⏳ Processing...";

    const res = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, html, prompt })
    });

    const data = await res.json();
    document.getElementById("output").innerText =
        JSON.stringify(data, null, 2);
}
