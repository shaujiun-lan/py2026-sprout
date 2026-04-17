const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');

let width = window.innerWidth;
let height = window.innerHeight;
canvas.width = width;
canvas.height = height;

let particles = [];

function update_particles() {
    particles = [];
    let particle_color_1 = getComputedStyle(document.querySelector('.main-particles')).color;
    let particle_color_2 = getComputedStyle(document.querySelector('.side-particles')).color;
    for (let i = 0; i < 90; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            radius: Math.random() * 2 + 1,
            speedX: (Math.random() - 0.5) * 0.3,
            speedY: (Math.random() - 0.5) * 0.3,
            color: Math.random() < 0.3 ? particle_color_1 : particle_color_2
        });
    }
}

update_particles();

function draw() {
    ctx.clearRect(0, 0, width, height);

    for (let p of particles) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();

        p.x += p.speedX;
        p.y += p.speedY;

        if (p.x < 0 || p.x > width) p.speedX *= -1;
        if (p.y < 0 || p.y > height) p.speedY *= -1;
    }

    requestAnimationFrame(draw);
}

draw();

window.addEventListener('resize', () => {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
});

window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > height * 0.07) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

let copy_msg = document.getElementById('copy_msg');

function show_copied(e, suc) {

    if (suc) {
        e.classList.remove('suc_def');e.classList.add('suc');
        setTimeout(()=>{e.classList.remove('suc'); e.classList.add('suc_def')}, 500);
    } else {
        e.classList.remove('fail_def');e.classList.add('fail');
        setTimeout(()=>{e.classList.remove('fail'); e.classList.add('fail_def')}, 500);
    }

}

function copy_code(e) {
    let range = document.createRange();
    range.selectNode(e);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    try {
        document.execCommand('copy');
        show_copied(e, 1);
    } catch (err) {
        show_copied(e, 0);
    }
    window.getSelection().removeAllRanges();
}

document.querySelectorAll('#copyable').forEach( (preElement) => {
    preElement.addEventListener('click', () => {
        copy_code(preElement);
    });
});

const lightThemeColor = document.getElementById('light-theme');
const darkThemeColor = document.getElementById('dark-theme');
const cuteThemeColor = document.getElementById('cute-theme');
const techThemeColor = document.getElementById('tech-theme');
const greekThemeColor = document.getElementById('greek-theme');

function selectTheme(selectedTheme) {
    const themes = document.querySelectorAll('.theme-color');
    themes.forEach(theme => {
        theme.classList.remove('selected');
    });
    selectedTheme.classList.add('selected');
}

lightThemeColor.addEventListener('click', () => {
    document.body.className = '';
    update_particles();
    selectTheme(lightThemeColor);
});

darkThemeColor.addEventListener('click', () => {
    document.body.className = 'dark';
    update_particles();
    selectTheme(darkThemeColor);
});

cuteThemeColor.addEventListener('click', () => {
    document.body.className = 'cute';
    update_particles();
    selectTheme(cuteThemeColor);
});

techThemeColor.addEventListener('click', () => {
    document.body.className = 'tech';
    update_particles();
    selectTheme(techThemeColor);
});

greekThemeColor.addEventListener('click', () => {
    document.body.className = 'greek';
    update_particles();
    selectTheme(greekThemeColor);
});

selectTheme(lightThemeColor);