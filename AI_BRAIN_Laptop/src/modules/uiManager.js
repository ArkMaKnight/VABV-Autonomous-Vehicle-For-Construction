export class UIManager {
    constructor() {
        this.toggleSideBar = document.getElementById("togglesidebar");
        alertBox = document.getElementById("epp");
    }

    showSideBar() {
        this.toggleSideBar.addEventListener("click", () => {
        document.body.classList.toggle("sidebar-collapsed");
        });
    } 

    detectAlarm() {
        alertBox.innerHTML = "EPP NO DETECTADO. SONANDO ALARMA...";
        alertBox.style.backgroundColor = 'var(--alert-color)';
        alertBox.style.color = 'var(--text-alarm)';
    }

    normalStatus() {
        alertBox.innerHTML = "EPP DETECTADO. SEGURIDAD GARANTIZADA";
        alertBox.backgroundColor = "var(--green-dark)";
        alertBox.style.color = "var(--no-alert-text)";
    }

    showControl() {
        
    }
    }