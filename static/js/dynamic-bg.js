document.addEventListener("DOMContentLoaded", () => {

    const bg = document.createElement("div");
    bg.className = "interactive-bg";
    document.body.appendChild(bg);

    /* --------------------------
       설정값
    --------------------------- */
    const COUNT = 40;  // 물체 더 많게
    const COLORS = ["obj1","obj2","obj3","obj4","obj5","obj6","obj7"];
    const objects = [];

    let mouseX = window.innerWidth * 0.5;
    let mouseY = window.innerHeight * 0.5;

    /* 화면 따라 리사이즈 대응 */
    let W = window.innerWidth;
    let H = window.innerHeight;
    window.addEventListener("resize", () => {
        W = window.innerWidth;
        H = window.innerHeight;
    });


    /* --------------------------
       물체 생성
    --------------------------- */
    for (let i = 0; i < COUNT; i++) {
        const obj = document.createElement("div");
        obj.className = "floating-object";

        if (Math.random() > 0.5) obj.classList.add("circle");
        obj.classList.add(COLORS[i % COLORS.length]);

        // 초기 위치
        obj.x = Math.random() * W;
        obj.y = Math.random() * H;

        // 곡선 기반 속도
        obj.vx = (Math.random() * 0.6 + 0.3) * (Math.random() < 0.5 ? -1 : 1);
        obj.vy = (Math.random() * 0.6 + 0.3) * (Math.random() < 0.5 ? -1 : 1);

        obj.sx = Math.random() * 1000;
        obj.sy = Math.random() * 1000;

        bg.appendChild(obj);
        objects.push(obj);
    }


    /* --------------------------
       마우스 = 광원
    --------------------------- */
    window.addEventListener("mousemove", e => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });


    /* Math helper */
    const lerp = (a, b, t) => a + (b - a) * t;


    /* --------------------------
       애니메이션
    --------------------------- */
    function animate(t) {

        objects.forEach(obj => {

            /* 곡선 + 부드러운 흐름 */
            obj.sx += 0.002;
            obj.sy += 0.002;

            obj.x += obj.vx + Math.sin(obj.sx) * 0.5;
            obj.y += obj.vy + Math.cos(obj.sy) * 0.5;

            // 화면 넘어가면 반대 이동
            if (obj.x > W + 40) obj.x = -40;
            if (obj.x < -40) obj.x = W + 40;
            if (obj.y > H + 40) obj.y = -40;
            if (obj.y < -40) obj.y = H + 40;

            obj.style.transform = `translate3d(${obj.x}px, ${obj.y}px, 0)`;


            /* --------------------------
               CodePen 기반 그림자 모델
            --------------------------- */
            const dx = obj.x - mouseX;
            const dy = obj.y - mouseY;
            const dist = Math.sqrt(dx*dx + dy*dy);

            // 부드러운 falloff
            const shadowLen = dist * 0.25;
            const blur = Math.min(dist * 0.3, 90);
            const alpha = Math.max(0.55 - dist / 800, 0.1);

            // 깜빡임 제거 (lerp로 부드럽게)
            const sx = lerp(obj._sx || 0, dx / 4, 0.15);
            const sy = lerp(obj._sy || 0, dy / 4, 0.15);

            obj._sx = sx;
            obj._sy = sy;

            obj.style.boxShadow = `
                ${sx}px ${sy}px ${blur}px rgba(0,0,0,${alpha})
            `;
        });

        requestAnimationFrame(animate);
    }

    animate();

});
