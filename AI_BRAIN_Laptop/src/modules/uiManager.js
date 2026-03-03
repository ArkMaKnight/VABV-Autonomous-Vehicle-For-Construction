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
        this.alertBox.style.backgroundColor = 'var(--alert-color)';
        this.alertBox.style.color = 'var(--text-alarm)';
    }

    normalStatus() {
        this.alertBox.innerHTML = "EPP DETECTADO. SEGURIDAD GARANTIZADA";
        this.alertBox.style.backgroundColor = "var(--green-dark)";
        this.alertBox.style.color = "var(--no-alert-text)";
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