// FinMind AI Application Logic, Goal Management & Export Engine

class FinMindApp {
    constructor() {
        this.data = null;
        this.forecastChart = null;
        this.categoryChart = null;
        this.activeTab = 'overview';
        this.theme = localStorage.getItem('finmind_theme') || 'dark';

        this.init();
    }

    async init() {
        try {
            const response = await fetch('data.json');
            this.data = await response.json();
            
            // Apply saved theme
            this.applyTheme(this.theme);

            // Check for saved local profile overrides
            const savedIncome = localStorage.getItem('finmind_income');
            if (savedIncome) {
                this.data.monthly_income = parseFloat(savedIncome);
            }
            const savedBurn = localStorage.getItem('finmind_burn');
            if (savedBurn) {
                this.data.monthly_burn = parseFloat(savedBurn);
            }
            this.recalculateSavingsRate();

            this.renderKPIs();
            this.renderGoals();
            this.renderCharts();
            this.renderLedgerTable(this.data.transactions);
            this.setupEventListeners();
            this.setupScenarioSimulator();
        } catch (error) {
            console.error("Error loading FinMind data:", error);
            this.showToast("Error loading financial ledger data", "error");
        }
    }

    switchTab(tabName) {
        this.activeTab = tabName;
        
        // Hide all tab panels
        document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.add('hidden'));
        
        // Deactivate all tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
            btn.setAttribute('aria-selected', 'false');
        });

        // Activate target panel and button
        const targetPanel = document.getElementById(`tab-${tabName}`);
        const targetBtn = document.getElementById(`tab-btn-${tabName}`);

        if (targetPanel) targetPanel.classList.remove('hidden');
        if (targetBtn) {
            targetBtn.classList.add('active');
            targetBtn.setAttribute('aria-selected', 'true');
        }

        // Resize charts if switching to Overview
        if (tabName === 'overview') {
            setTimeout(() => {
                if (this.forecastChart) this.forecastChart.resize();
                if (this.categoryChart) this.categoryChart.resize();
            }, 50);
        }
    }

    applyTheme(theme) {
        this.theme = theme;
        localStorage.setItem('finmind_theme', theme);
        const btnToggle = document.getElementById('btn-theme-toggle');
        if (theme === 'light') {
            document.body.classList.add('light-theme');
            if (btnToggle) btnToggle.innerHTML = '☀️ Light';
        } else {
            document.body.classList.remove('light-theme');
            if (btnToggle) btnToggle.innerHTML = '🌙 Dark';
        }
    }

    toggleTheme() {
        const newTheme = this.theme === 'dark' ? 'light' : 'dark';
        this.applyTheme(newTheme);
        this.showToast(`Switched to ${newTheme.toUpperCase()} theme`, "info");
    }

    showToast(message, type = "info") {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = type === 'error' ? '⚠️' : type === 'warning' ? '🔔' : '✅';
        toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;

        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(50px)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    }

    recalculateSavingsRate() {
        if (!this.data) return;
        const income = this.data.monthly_income;
        const burn = this.data.monthly_burn;
        if (income > 0) {
            this.data.savings_rate = Math.round(((income - burn) / income) * 1000) / 10;
        } else {
            this.data.savings_rate = 0;
        }
    }

    renderKPIs() {
        if (!this.data) return;
        document.getElementById('kpi-balance').innerText = `$${this.data.current_balance.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('kpi-income').innerText = `$${this.data.monthly_income.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('kpi-burn').innerText = `$${this.data.monthly_burn.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('kpi-savings').innerText = `${this.data.savings_rate}%`;

        const burnRatio = Math.round((this.data.monthly_burn / this.data.monthly_income) * 1000) / 10;
        document.getElementById('kpi-burn-ratio').innerText = `${burnRatio}% of Monthly Cashflow`;
    }

    setupScenarioSimulator() {
        const purchaseSlider = document.getElementById('sim-purchase');
        const expenseSlider = document.getElementById('sim-expense');
        const salarySlider = document.getElementById('sim-salary');

        const valPurchase = document.getElementById('val-sim-purchase');
        const valExpense = document.getElementById('val-sim-expense');
        const valSalary = document.getElementById('val-sim-salary');
        const badge = document.getElementById('sim-risk-badge');

        if (!purchaseSlider || !expenseSlider || !salarySlider) return;

        const updateSimulation = () => {
            const purchase = parseFloat(purchaseSlider.value);
            const expenseDelta = parseFloat(expenseSlider.value);
            const salaryDelta = parseFloat(salarySlider.value);

            valPurchase.innerText = `$${purchase.toLocaleString()}`;
            valExpense.innerText = `${expenseDelta >= 0 ? '+' : ''}$${expenseDelta.toLocaleString()}`;
            valSalary.innerText = `${salaryDelta >= 0 ? '+' : ''}$${salaryDelta.toLocaleString()}`;

            const baseBalance = this.data.current_balance;
            const baseIncome = this.data.monthly_income;
            const baseBurn = this.data.monthly_burn;

            const adjBalance = baseBalance - purchase;
            const adjIncome = baseIncome + salaryDelta;
            const adjBurn = baseBurn + expenseDelta;
            const netCashflow = adjIncome - adjBurn;

            const projected30d = adjBalance + netCashflow;

            if (projected30d < 0) {
                badge.innerText = "Status: CRITICAL (Deficit Risk)";
                badge.className = "sim-impact-badge critical";
            } else if (projected30d < (adjBurn * 1.5)) {
                badge.innerText = "Status: WARNING (Low Buffer)";
                badge.className = "sim-impact-badge warning";
            } else {
                badge.innerText = "Status: HEALTHY";
                badge.className = "sim-impact-badge healthy";
            }

            // Overlay scenario curve on chart
            this.updateForecastChartWithScenario(purchase, netCashflow);
        };

        purchaseSlider.addEventListener('input', updateSimulation);
        expenseSlider.addEventListener('input', updateSimulation);
        salarySlider.addEventListener('input', updateSimulation);
    }

    updateForecastChartWithScenario(purchase, netCashflow) {
        if (!this.forecastChart || !this.data.forecasts) return;

        const forecastDates = this.data.forecasts.map(f => f.date);
        const initialAdjusted = this.data.current_balance - purchase;
        const dailyDelta = netCashflow / 30.0;

        const scenarioBalances = forecastDates.map((_, idx) => {
            return Math.round((initialAdjusted + (dailyDelta * (idx + 1))) * 100) / 100;
        });

        // Add or update secondary dataset for scenario simulation
        if (this.forecastChart.data.datasets.length > 1) {
            this.forecastChart.data.datasets[1].data = scenarioBalances;
        } else {
            this.forecastChart.data.datasets.push({
                label: 'Scenario Projected Balance ($)',
                data: scenarioBalances,
                borderColor: '#6366f1',
                borderWidth: 2,
                borderDash: [5, 5],
                fill: false,
                tension: 0.3,
                pointBackgroundColor: '#6366f1'
            });
        }

        this.forecastChart.update();
    }

    renderGoals() {
        const container = document.getElementById('goals-container');
        if (!container || !this.data.goals) return;

        container.innerHTML = '';

        this.data.goals.forEach(goal => {
            const percent = Math.min(100, Math.round((goal.current_amount / goal.target_amount) * 100));
            const card = document.createElement('div');
            card.className = 'goal-card';

            card.innerHTML = `
                <div class="goal-header">
                    <span class="goal-title">${goal.title}</span>
                    <span class="goal-category">${goal.category || 'Goal'}</span>
                </div>
                <div class="goal-values">
                    <span class="goal-current">$${goal.current_amount.toLocaleString()}</span>
                    <span class="goal-target">Target: $${goal.target_amount.toLocaleString()} (${percent}%)</span>
                </div>
                <div class="goal-progress-bar">
                    <div class="goal-progress-fill" style="width: ${percent}%; background-color: ${goal.color || '#10b981'};"></div>
                </div>
                <div class="goal-footer">
                    <span>Contrib: +$${goal.monthly_contribution}/mo</span>
                    <span>Target Date: ${goal.target_date}</span>
                </div>
            `;

            container.appendChild(card);
        });
    }

    renderCharts() {
        if (!this.data) return;

        // 1. Forecast Line Chart
        const forecastCtx = document.getElementById('forecastChart').getContext('2d');
        const forecastDates = this.data.forecasts.map(f => f.date);
        const forecastBalances = this.data.forecasts.map(f => f.predicted_balance);

        const gradient = forecastCtx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, 'rgba(16, 185, 129, 0.35)');
        gradient.addColorStop(1, 'rgba(16, 185, 129, 0.0)');

        if (this.forecastChart) this.forecastChart.destroy();

        this.forecastChart = new Chart(forecastCtx, {
            type: 'line',
            data: {
                labels: forecastDates,
                datasets: [{
                    label: '30-Day Balance Forecast ($)',
                    data: forecastBalances,
                    borderColor: '#10b981',
                    borderWidth: 3,
                    backgroundColor: gradient,
                    fill: true,
                    tension: 0.3,
                    pointBackgroundColor: '#10b981',
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: true, labels: { color: '#a1a1aa', font: { family: 'Outfit', size: 12 } } },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            label: function(context) { return ` ${context.dataset.label}: $${context.raw.toLocaleString()}`; }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#a1a1aa', font: { family: 'JetBrains Mono', size: 10 } }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#a1a1aa', font: { family: 'JetBrains Mono', size: 10 } }
                    }
                }
            }
        });

        // 2. Category Spending Doughnut Chart
        const categoryCtx = document.getElementById('categoryChart').getContext('2d');
        const catMap = {};
        this.data.transactions.forEach(t => {
            if (t.type === 'EXPENSE') {
                catMap[t.category] = (catMap[t.category] || 0) + t.amount;
            }
        });

        const catLabels = Object.keys(catMap);
        const catValues = Object.values(catMap);
        const catColors = ['#6366f1', '#f59e0b', '#ef4444', '#ec4899', '#3b82f6', '#8b5cf6', '#14b8a6'];

        if (this.categoryChart) this.categoryChart.destroy();

        this.categoryChart = new Chart(categoryCtx, {
            type: 'doughnut',
            data: {
                labels: catLabels,
                datasets: [{
                    data: catValues,
                    backgroundColor: catColors,
                    borderWidth: 2,
                    borderColor: '#18181b'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: { color: '#a1a1aa', font: { family: 'Outfit', size: 12 } }
                    }
                },
                cutout: '70%'
            }
        });
    }

    renderLedgerTable(transactions) {
        const tbody = document.getElementById('ledger-body');
        tbody.innerHTML = '';

        const recent = transactions.slice(-25).reverse();

        recent.forEach(t => {
            const tr = document.createElement('tr');
            
            const isInc = t.type === 'INCOME';
            const amountColor = isInc ? 'text-emerald' : 'text-main';
            const amountPrefix = isInc ? '+' : '-';

            tr.innerHTML = `
                <td style="font-family: var(--font-mono); color: var(--text-subtle);">${t.id}</td>
                <td style="font-family: var(--font-mono);">${t.date}</td>
                <td><strong>${t.merchant}</strong></td>
                <td><span class="tag-cat">${t.category}</span></td>
                <td><span style="font-size: 0.75rem; font-weight: 600; color: ${isInc ? 'var(--accent-emerald)' : 'var(--text-muted)'}">${t.type}</span></td>
                <td class="${amountColor}" style="font-family: var(--font-mono); font-weight: 700;">${amountPrefix}$${t.amount.toFixed(2)}</td>
                <td>${t.is_anomaly ? `<span class="tag-anomaly">⚠️ ${t.notes}</span>` : `<span style="color: var(--text-subtle); font-size: 0.8rem;">Normal</span>`}</td>
            `;

            tbody.appendChild(tr);
        });
    }

    setupEventListeners() {
        // Theme Toggle
        const btnThemeToggle = document.getElementById('btn-theme-toggle');
        if (btnThemeToggle) {
            btnThemeToggle.addEventListener('click', () => this.toggleTheme());
        }

        // Search & Category Filter
        const searchInput = document.getElementById('tx-search');
        const filterSelect = document.getElementById('tx-filter');

        const applyFilter = () => {
            const query = searchInput.value.toLowerCase();
            const category = filterSelect.value;

            const filtered = this.data.transactions.filter(t => {
                const matchesQuery = t.merchant.toLowerCase().includes(query) || t.category.toLowerCase().includes(query);
                const matchesCategory = category === 'ALL' || t.category === category;
                return matchesQuery && matchesCategory;
            });

            this.renderLedgerTable(filtered);
        };

        searchInput.addEventListener('input', applyFilter);
        filterSelect.addEventListener('change', applyFilter);

        // Export Dropdown Toggle
        const btnExport = document.getElementById('btn-export-dropdown');
        const exportMenu = document.getElementById('export-menu');
        btnExport.addEventListener('click', (e) => {
            e.stopPropagation();
            exportMenu.classList.toggle('hidden');
        });
        document.addEventListener('click', () => exportMenu.classList.add('hidden'));

        // Chat Modal Drawer
        const chatModal = document.getElementById('chat-modal');
        document.getElementById('btn-open-chat').addEventListener('click', () => {
            chatModal.classList.remove('hidden');
        });

        document.getElementById('btn-close-chat').addEventListener('click', () => {
            chatModal.classList.add('hidden');
        });

        // Goal Modal
        const goalModal = document.getElementById('goal-modal');
        document.getElementById('btn-close-goal').addEventListener('click', () => {
            goalModal.classList.add('hidden');
        });

        // Profile Modal
        const profileModal = document.getElementById('profile-modal');
        document.getElementById('btn-close-profile').addEventListener('click', () => {
            profileModal.classList.add('hidden');
        });

        // Chat Send
        const chatInput = document.getElementById('chat-input');
        const btnSend = document.getElementById('btn-send-chat');

        const sendMsg = () => {
            const text = chatInput.value.trim();
            if (!text) return;
            this.handleUserChatMessage(text);
            chatInput.value = '';
        };

        btnSend.addEventListener('click', sendMsg);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMsg();
        });
    }

    openEditProfileModal() {
        document.getElementById('profile-income').value = this.data.monthly_income;
        const burnInput = document.getElementById('profile-burn');
        if (burnInput) burnInput.value = this.data.monthly_burn;
        document.getElementById('profile-modal').classList.remove('hidden');
    }

    saveProfileChanges() {
        const newIncome = parseFloat(document.getElementById('profile-income').value);
        const newBurn = parseFloat(document.getElementById('profile-burn').value);

        if (isNaN(newIncome) || newIncome <= 0) {
            alert('Please enter a valid monthly salary amount.');
            return;
        }
        if (isNaN(newBurn) || newBurn < 0) {
            alert('Please enter a valid monthly burn rate / expense budget.');
            return;
        }

        this.data.monthly_income = newIncome;
        this.data.monthly_burn = newBurn;
        localStorage.setItem('finmind_income', newIncome);
        localStorage.setItem('finmind_burn', newBurn);

        this.recalculateSavingsRate();
        this.renderKPIs();
        this.renderCharts();

        document.getElementById('profile-modal').classList.add('hidden');
        this.showToast(`Profile updated: Income $${newIncome.toLocaleString()}/mo, Burn $${newBurn.toLocaleString()}/mo`, "success");
        
        // Notify chat
        this.sendQuickPrompt(`I updated my monthly salary to $${newIncome.toLocaleString()} and monthly expense budget to $${newBurn.toLocaleString()}. Recalculate my budget!`);
    }

    openNewGoalModal() {
        document.getElementById('goal-modal').classList.remove('hidden');
    }

    saveNewGoal() {
        const title = document.getElementById('goal-title').value.trim();
        const target = parseFloat(document.getElementById('goal-target').value);
        const current = parseFloat(document.getElementById('goal-current').value) || 0;
        const monthly = parseFloat(document.getElementById('goal-monthly').value);
        const date = document.getElementById('goal-date').value;

        if (!title || isNaN(target) || isNaN(monthly) || !date) {
            alert('Please fill out all goal fields correctly.');
            return;
        }

        const colors = ['#10b981', '#6366f1', '#f59e0b', '#ec4899', '#8b5cf6'];
        const newGoal = {
            id: `GOAL-${Date.now()}`,
            title: title,
            target_amount: target,
            current_amount: current,
            monthly_contribution: monthly,
            target_date: date,
            category: 'Custom Goal',
            color: colors[this.data.goals.length % colors.length]
        };

        this.data.goals.push(newGoal);
        this.renderGoals();

        document.getElementById('goal-modal').classList.add('hidden');
        document.getElementById('goal-title').value = '';
        document.getElementById('goal-target').value = '';
        document.getElementById('goal-current').value = '0';
        document.getElementById('goal-monthly').value = '';
        document.getElementById('goal-date').value = '';

        this.showToast(`New Goal Vault created: ${title}`, "success");
    }

    exportCSV() {
        if (!this.data || !this.data.transactions) return;

        let csvContent = "data:text/csv;charset=utf-8,";
        csvContent += "Transaction_ID,Date,Merchant,Category,Type,Amount,Is_Anomaly,Audit_Notes\n";

        this.data.transactions.forEach(t => {
            const row = [
                t.id,
                t.date,
                `"${t.merchant.replace(/"/g, '""')}"`,
                `"${t.category}"`,
                t.type,
                t.amount.toFixed(2),
                t.is_anomaly ? "YES" : "NO",
                `"${(t.notes || '').replace(/"/g, '""')}"`
            ].join(",");
            csvContent += row + "\n";
        });

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", `FinMind_BigQuery_Ledger_Export_${new Date().toISOString().slice(0,10)}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        this.showToast("CSV Ledger exported successfully", "success");
    }

    exportPDF() {
        this.showToast("Preparing printable audit report...", "info");
        setTimeout(() => window.print(), 500);
    }

    sendQuickPrompt(text) {
        document.getElementById('chat-modal').classList.remove('hidden');
        this.handleUserChatMessage(text);
    }

    handleUserChatMessage(userText) {
        const chatBody = document.getElementById('chat-messages');

        const userDiv = document.createElement('div');
        userDiv.className = 'chat-bubble user';
        userDiv.innerText = userText;
        chatBody.appendChild(userDiv);
        chatBody.scrollTop = chatBody.scrollHeight;

        setTimeout(() => {
            const aiDiv = document.createElement('div');
            aiDiv.className = 'chat-bubble ai';

            const lower = userText.toLowerCase();
            let aiReply = "";

            if (lower.includes("updated my monthly salary") || lower.includes("salary")) {
                aiReply = `🎉 <strong>Salary Update Recognized!</strong><br>I have recalculated your financial metrics for your new salary of <strong>$${this.data.monthly_income.toLocaleString()}</strong>/mo.<br>• Your new Net Savings Rate is <strong>${this.data.savings_rate}%</strong>.<br>• Monthly Surplus Cash: <strong>$${(this.data.monthly_income - this.data.monthly_burn).toLocaleString()}</strong>.<br>Your extra cash flow can now accelerate your savings goals!`;
            } else if (lower.includes("what if") || lower.includes("car") || lower.includes("purchase") || lower.includes("scenario")) {
                aiReply = `🎛️ <strong>Scenario Engine Active:</strong><br>I ran a What-If scenario on your ledger. Switch to the <strong>🎛️ "What-If" Simulator</strong> tab to see interactive sliders and live balance projection curve overlays!`;
            } else if (lower.includes("save") || lower.includes("saving") || lower.includes("500")) {
                aiReply = "💡 <strong>FinMind AI Savings Plan:</strong><br>1. Cancel dormant subscriptions (Forgotten Gym & AWS Sandbox) → Save <strong>$138.99/mo</strong>.<br>2. Reduce Dining out expense by 15% → Save <strong>$180.00/mo</strong>.<br>3. Switch Verizon fiber plan to promo rate → Save <strong>$35.00/mo</strong>.<br><strong>Total Monthly Savings: $353.99/mo ($4,247/yr)!</strong>";
            } else if (lower.includes("subscription") || lower.includes("dormant") || lower.includes("unused")) {
                aiReply = "🔍 <strong>Auditor Agent Summary:</strong><br>Found 2 active subscriptions with zero usage in 60 days:<br>• <strong>Forgotten Gym Membership:</strong> $49.99/mo<br>• <strong>AWS Cloud Services Sandbox:</strong> $89.00/mo<br><em>Click 'Auto-Cancel' to stop auto-billing.</em>";
            } else if (lower.includes("forecast") || lower.includes("crunch") || lower.includes("end-of-month")) {
                aiReply = "📈 <strong>30-Day Cashflow Projection:</strong><br>Your projected balance at day 30 is <strong>$25,315.04</strong>. You have 0 high-risk crunch alerts. Next major income deposit: $4,250.00 on the 1st.";
            } else {
                aiReply = `🤖 <strong>FinMind Co-pilot:</strong> I analyzed your query "${userText}". Based on your BigQuery financial ledger, your net savings rate is ${this.data.savings_rate}%. Would you like me to generate a personalized tax optimization strategy or model a major purchase scenario?`;
            }

            aiDiv.innerHTML = aiReply;
            chatBody.appendChild(aiDiv);
            chatBody.scrollTop = chatBody.scrollHeight;
        }, 500);
    }

    showAuditDetails() {
        this.switchTab('agents');
        this.sendQuickPrompt("Show me my dormant subscriptions");
    }

    showForecastDetails() {
        this.switchTab('overview');
        this.sendQuickPrompt("Forecast my end-of-month balance");
    }
}

let app;
window.addEventListener('DOMContentLoaded', () => {
    app = new FinMindApp();
});
