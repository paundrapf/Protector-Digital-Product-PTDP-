/* Fluid Shader & Marquee Animation */

document.addEventListener('DOMContentLoaded', () => {
    initFluidBackground();
    initMarquee();
});

function initMarquee() {
    const marqueeContent = document.querySelector('.marquee-content');
    if (!marqueeContent) return;
    
    // Clone content to ensure seamless loop
    const content = marqueeContent.innerHTML;
    marqueeContent.innerHTML = content + content + content + content;
}

function initFluidBackground() {
    const canvas = document.getElementById('fluid-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height;
    let time = 0;

    // Configuration
    const blobs = [
        { x: 0.2, y: 0.2, r: 0.3, color: '#FF4D6D', speed: 0.002 }, // Pink
        { x: 0.8, y: 0.3, r: 0.4, color: '#3B82F6', speed: 0.003 }, // Blue
        { x: 0.5, y: 0.8, r: 0.35, color: '#10B981', speed: 0.0025 } // Green
    ];

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }

    window.addEventListener('resize', resize);
    resize();

    function draw() {
        ctx.clearRect(0, 0, width, height);
        
        // Create a soft blur effect
        ctx.filter = 'blur(80px)';
        ctx.globalAlpha = 0.6;

        blobs.forEach((blob, i) => {
            // Move blobs
            blob.x += Math.sin(time * blob.speed + i) * 0.002;
            blob.y += Math.cos(time * blob.speed + i) * 0.002;

            // Draw blob
            ctx.beginPath();
            ctx.fillStyle = blob.color;
            const x = blob.x * width;
            const y = blob.y * height;
            const r = blob.r * Math.min(width, height);
            ctx.arc(x, y, r, 0, Math.PI * 2);
            ctx.fill();
        });

        ctx.filter = 'none';
        time += 1;
        requestAnimationFrame(draw);
    }

    draw();
}
