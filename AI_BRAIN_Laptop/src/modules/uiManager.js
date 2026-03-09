export class UIManager {
    constructor() {
        this.toggleSideBar = document.getElementById("toggleSidebar");
        this.alertBox = document.getElementById("epp");
        this.controlBtn = document.getElementById("ctrl");
        this.controlBox = document.getElementById("ctrlBox")
        this.logsBtn = document.getElementById("logs");
        this.logsBox = document.getElementById("logsBox");
    }

    showSideBar() {
        this.toggleSideBar.addEventListener("click", () => {
        document.body.classList.toggle("sidebar-collapsed");
        });
    } 

    detectAlarm() {
        this.alertBox.innerHTML = "EPP NO DETECTADO. SONANDO ALARMA...";
        this.alertBox.style.background = 'linear-gradient(135deg, #7a0020, #a30028)';
        this.alertBox.style.borderColor = '#ff4455';
        this.alertBox.style.color = '#ffcccc';
    }

    normalStatus() {
        this.alertBox.innerHTML = "EPP DETECTADO. SEGURIDAD GARANTIZADA";
        this.alertBox.style.background = 'linear-gradient(135deg, #064e06, #0d7d0d)';
        this.alertBox.style.borderColor = '#44cc44';
        this.alertBox.style.color = '#ccffcc';
    }

    updateStatus(msg, action) {
        if (!this.alertBox) return;
        this.alertBox.textContent = msg;

        const styles = {
            'ALARM':   { bg: 'linear-gradient(135deg, #7a0020, #a30028)', border: '#ff4455', color: '#ffcccc' },
            'STOP':    { bg: 'linear-gradient(135deg, #6b4f00, #8a6500)', border: '#ffcc44', color: '#fff3cd' },
            'FORWARD': { bg: 'linear-gradient(135deg, #064e06, #0d7d0d)', border: '#44cc44', color: '#ccffcc' },
            'LEFT':    { bg: 'linear-gradient(135deg, #0a2a5c, #0d3d7d)', border: '#4488ff', color: '#cce0ff' },
            'RIGHT':   { bg: 'linear-gradient(135deg, #0a2a5c, #0d3d7d)', border: '#4488ff', color: '#cce0ff' },
            'SLOW':    { bg: 'linear-gradient(135deg, #5c3a0a, #7d4f0d)', border: '#ff9944', color: '#ffe0cc' }
        };
        const s = styles[action] || { bg: 'linear-gradient(135deg, #1a1a2e, #16213e)', border: 'rgba(255,255,255,0.08)', color: '#8892a4' };
        this.alertBox.style.background = s.bg;
        this.alertBox.style.borderColor = s.border;
        this.alertBox.style.color = s.color;
    }

    showControl() {
        if (this.controlBtn && this.controlBox) {
            this.controlBtn.addEventListener("click", () => {
                this.controlBox.classList.toggle("visible");
                this.controlBtn.classList.toggle("active");
            });
        }
    }
    showLogs() {
        this.logsBtn.addEventListener("click", () => {
            this.logsBox.style.opacity = 100;
            this.logsBtn.style.background = "var(--alert-color)";
        } )
    }
    }