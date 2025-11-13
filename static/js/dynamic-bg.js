// 배경 컨테이너 생성
document.addEventListener("DOMContentLoaded", function () {
    const bg = document.createElement("div");
    bg.className = "interactive-bg";
    document.body.appendChild(bg);

    // 오브젝트 여러 개 생성
    const colors = ["obj-blue", "obj-purple", "obj-red"];
    const objectCount = 12;

    const objects = [];
    for (let i = 0; i < objectCount; i++) {
        const obj = document.createElement("div");
        obj.className = "floating-object";

        if (Math.random() > 0.5) obj.classList.add("circle");
        obj.classList.add(colors[i % colors.length]);

        obj.style.top = Math.random() * 90 + "vh";
        obj.style.left = Math.random() * 90 + "vw";

        bg.appendChild(obj);
        objects.push(obj);
    }

    // 마우스 움직임에 따라 그림자 변경
    window.addEventListener("mousemove", (e) => {
        const x = e.clientX;
        const y = e.clientY;

        objects.forEach(obj => {
            const rect = obj.getBoundingClientRect();
            const objX = rect.left + rect.width / 2;
            const objY = rect.top + rect.height / 2;

            const angleX = (x - objX) / 20;
            const angleY = (y - objY) / 20;

            obj.style.boxShadow = `
                ${angleX}px ${angleY}px 25px rgba(0,0,0,0.6),
                inset ${-angleX / 2}px ${-angleY / 2}px 20px rgba(255,255,255,0.1)
            `;
        });
    });
});
