
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto('https://www.fortnite.com/item-shop', { waitUntil: 'networkidle' });
    const data = await page.evaluate(() => {
        const sections = Array.from(document.querySelectorAll('[data-component="ShopSection"]'));
        return sections.map(section => {
            const category = section.querySelector('h2')?.innerText || "Без категории";
            const items = Array.from(section.querySelectorAll('[data-component="ShopCard"]')).map(card => ({
                title: card.querySelector('h3')?.innerText || "Без названия",
                price: card.querySelector('[data-test-id="currency-price"]')?.innerText || "Неизвестно",
                image: card.querySelector('img')?.src || ""
            }));
            return { category, items };
        });
    });
    fs.writeFileSync("shop_data.json", JSON.stringify(data, null, 2));
    console.log(JSON.stringify(data));
    await browser.close();
})();
