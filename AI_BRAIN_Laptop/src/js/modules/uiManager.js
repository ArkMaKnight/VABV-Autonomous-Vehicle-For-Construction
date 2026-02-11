export class UIManager {
    constructor() {
        this.toggleSideBar = document.getElementById("togglesidebar");
      
    }

    showSideBar() {
        this.toggleSideBar.addEventListener("click", () => {
        document.body.classList.toggle("sidebar-collapsed");
        });
    } 

    detectAlarm() {

    }

    NormalStatus() {

    }

    showControl() {
        
    }
    }