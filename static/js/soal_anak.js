// soal_anak.js
// Fungsionalitas tab, validasi, random, dan bantuan opsi serupa untuk modul observasi anak

// Fungsi untuk menampilkan/menyembunyikan bantuan opsi serupa
function toggleHelp(id) {
    const element = document.getElementById(id);
    if (element) {
        element.classList.toggle('hidden');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('assessment-form');
    const submitButton = document.getElementById('submit-button');
    const randomFillButton = document.getElementById('random-fill-button');
    const tabs = document.querySelectorAll('.tab-button');
    const tabPanels = document.querySelectorAll('.tab-panel');
    const nextTabButtons = document.querySelectorAll('.next-tab-button');

    const totalQuestions = new Set(Array.from(form.querySelectorAll('input[type="radio"]')).map(r => r.name)).size;

    function checkFormCompleteness() {
        const answeredQuestions = new Set(Array.from(form.querySelectorAll('input[type="radio"]:checked')).map(r => r.name)).size;
        submitButton.disabled = answeredQuestions !== totalQuestions;
    }

    function activateTab(tabButton) {
        tabs.forEach(btn => {
            btn.setAttribute('aria-selected', 'false');
            btn.classList.remove('text-blue-600', 'border-blue-600', 'bg-blue-50');
            btn.classList.add('border-transparent', 'hover:text-gray-600', 'hover:border-gray-300');
        });
        tabPanels.forEach(panel => panel.classList.add('hidden'));

        tabButton.setAttribute('aria-selected', 'true');
        tabButton.classList.add('text-blue-600', 'border-blue-600', 'bg-blue-50');
        const targetPanel = document.querySelector(tabButton.dataset.tabsTarget);
        if (targetPanel) {
            targetPanel.classList.remove('hidden');
        }
        form.scrollIntoView({ behavior: 'smooth' });
    }

    tabs.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            activateTab(button);
        });
    });

    nextTabButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const nextTab = document.getElementById(button.dataset.nextTabId);
            if (nextTab) activateTab(nextTab);
        });
    });
    
    randomFillButton.addEventListener('click', () => {
        const radioGroups = {};
        form.querySelectorAll('input[type="radio"]').forEach(radio => {
            if (!radioGroups[radio.name]) radioGroups[radio.name] = [];
            radioGroups[radio.name].push(radio);
        });
        for (const groupName in radioGroups) {
            const group = radioGroups[groupName];
            const randomIndex = Math.floor(Math.random() * group.length);
            group[randomIndex].checked = true;
        }
        checkFormCompleteness();
    });

    form.addEventListener('change', checkFormCompleteness);

    if (tabs.length > 0) activateTab(tabs[0]);
    checkFormCompleteness();
});
