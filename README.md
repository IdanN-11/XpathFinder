# 🔍 AI XPath Finder

AI XPath Finder is an **AI-powered utility** that generates **stable, optimized XPath expressions** from a given **HTML structure**.  
It is built to help **QA Automation Engineers** reduce time spent creating and debugging XPath locators for UI automation.

---

## 🚀 Why AI XPath Finder?

Writing reliable XPath is:
- Time-consuming
- Error-prone
- Often causes flaky automation tests

This tool uses an **AI agent** to analyze HTML DOM structure and return **robust, maintainable XPath locators** suitable for automation frameworks.

---

## ✨ Features

- Generate **unique and reliable XPath** from raw HTML
- Prefers **stable attributes** (`id`, `name`, `data-*`)
- Avoids brittle index-based XPath
- Supports:
  - Relative XPath
  - Attribute-based XPath
  - Text-based XPath
- Optimized for **Selenium, Playwright, Cypress**
- AI-driven logic for smarter locator selection

---

## 🧠 How It Works

1. User provides an **HTML snippet**
2. AI agent analyzes:
   - DOM hierarchy
   - Tag uniqueness
   - Attributes & text content
3. Tool generates the **best possible XPath**
4. Output can be directly used in automation scripts

---

## 📥 Input Example

```html
<div class="login-form">
    <input type="text" id="username" name="user"/>
    <input type="password" name="password"/>
    <button class="btn primary">Login</button>
</div>
