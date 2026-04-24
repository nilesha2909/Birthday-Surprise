const data = window.SURPRISE_DATA || {};
let currentQuestionIndex = 0;
let quizScore = 0;
let selectedAnswer = false;

document.addEventListener("DOMContentLoaded", () => {
    if (window.AOS) AOS.init({ duration: 850, once: true });

    startCountdown();
    initLoveChart();
    initLoveMessageGenerator();
    initQuiz();
    initButtons();
});

function startCountdown() {
    const countdownScreen = document.getElementById("countdown-screen");
    const memoryScreen = document.getElementById("memory-screen");
    const number = document.getElementById("countdown-number");

    if (!number) return;

    let count = data.countdownStart || 10;
    number.textContent = count;

    const timer = setInterval(() => {
        count -= 1;
        number.textContent = count;

        if (count <= 0) {
            clearInterval(timer);
            if (window.confetti) {
                confetti({ particleCount: 160, spread: 90, origin: { y: 0.62 } });
            }
            setTimeout(() => {
                countdownScreen.classList.add("hidden");
                memoryScreen.classList.remove("hidden");
                startMemorySwiper();
            }, 700);
        }
    }, 800);
}

function startMemorySwiper() {
    const card = document.getElementById("birthday-note-card");
    if (window.Swiper) {
        new Swiper(".memory-swiper", {
            loop: false,
            autoplay: {
                delay: 2300,
                disableOnInteraction: false
            },
            effect: "fade",
            fadeEffect: { crossFade: true },
            speed: 900,
            on: {
                reachEnd: () => {
                    setTimeout(() => {
                        document.getElementById("memory-swiper-wrap")?.classList.add("hidden");
                        card?.classList.remove("hidden");
                    }, 2600);
                }
            }
        });
    } else {
        setTimeout(() => card?.classList.remove("hidden"), 3000);
    }
}

function startMusic() {
    const music = document.getElementById("bgMusic");
    if (!music) return;

    music.volume = 0;
    music.play().then(() => {
        const fade = setInterval(() => {
            if (music.volume < 0.35) {
                music.volume = Math.min(0.35, music.volume + 0.02);
            } else {
                clearInterval(fade);
            }
        }, 160);
    }).catch(() => {});
}

function fadeOutMusic() {
    const music = document.getElementById("bgMusic");
    if (!music) return;

    const fade = setInterval(() => {
        if (music.volume > 0.04) {
            music.volume = Math.max(0, music.volume - 0.025);
        } else {
            music.pause();
            clearInterval(fade);
        }
    }, 120);
}

function initButtons() {
    const enterStoryBtn = document.getElementById("enter-story-btn");
    const mainContent = document.getElementById("main-content");
    const memoryScreen = document.getElementById("memory-screen");

    enterStoryBtn?.addEventListener("click", () => {
        startMusic();
        memoryScreen.classList.add("hidden");
        mainContent.classList.remove("hidden");
        setTimeout(() => document.getElementById("main-content")?.scrollIntoView({ behavior: "smooth" }), 100);
    });

    document.getElementById("secret-surprise-btn")?.addEventListener("click", () => {
        document.getElementById("proposal-modal")?.classList.remove("hidden");
    });

    document.getElementById("yes-btn")?.addEventListener("click", () => {
        document.getElementById("proposal-modal")?.classList.add("hidden");
        fadeOutMusic();
        setTimeout(() => {
            document.getElementById("final-surprise")?.classList.remove("hidden");
            if (window.confetti) {
                confetti({ particleCount: 120, spread: 90, origin: { y: 0.7 } });
            }
        }, 900);
    });

    const noBtn = document.getElementById("no-btn");
    noBtn?.addEventListener("mouseover", moveNoButton);
    noBtn?.addEventListener("click", moveNoButton);

    document.getElementById("show-closing-btn")?.addEventListener("click", () => {
        document.getElementById("final-surprise")?.classList.add("hidden");
        const closing = document.getElementById("closing-section");
        closing?.classList.remove("hidden");
        setTimeout(() => closing?.scrollIntoView({ behavior: "smooth" }), 80);
    });

    document.getElementById("replay-btn")?.addEventListener("click", () => {
        window.location.reload();
    });
}

function moveNoButton() {
    const btn = document.getElementById("no-btn");
    if (!btn) return;

    btn.style.position = "relative";
    const x = Math.floor(Math.random() * 180) - 90;
    const y = Math.floor(Math.random() * 120) - 60;
    btn.style.transform = `translate(${x}px, ${y}px)`;
}

function initLoveChart() {
    const ctx = document.getElementById("loveChart");
    if (!ctx || !window.Chart) return;

    new Chart(ctx, {
        type: "line",
        data: {
            labels: data.happinessLabels || [],
            datasets: [{
                label: "Happiness Over Time ❤️",
                data: data.happinessValues || [],
                tension: 0.45,
                fill: true,
                borderColor: "#ff6cab",
                backgroundColor: "rgba(255, 108, 171, 0.14)",
                pointBackgroundColor: "#fff",
                pointBorderColor: "#ff6cab",
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { labels: { color: "#fff6fb" } }
            },
            scales: {
                x: {
                    ticks: { color: "#f0ccd9" },
                    grid: { color: "rgba(255,255,255,0.08)" }
                },
                y: {
                    min: 0,
                    max: 100,
                    ticks: { color: "#f0ccd9" },
                    grid: { color: "rgba(255,255,255,0.08)" }
                }
            }
        }
    });
}

function initLoveMessageGenerator() {
    const btn = document.getElementById("generate-message-btn");
    const box = document.getElementById("love-message");
    const messages = data.loveMessages || [];

    btn?.addEventListener("click", () => {
        if (!messages.length || !box) return;
        const message = messages[Math.floor(Math.random() * messages.length)];
        box.textContent = message;
        box.classList.remove("hidden");
    });
}

function initQuiz() {
    renderQuestion();
    document.getElementById("next-question-btn")?.addEventListener("click", () => {
        if (!selectedAnswer) return;
        currentQuestionIndex += 1;
        selectedAnswer = false;
        renderQuestion();
    });
}

function renderQuestion() {
    const container = document.getElementById("quiz-container");
    const nextBtn = document.getElementById("next-question-btn");
    const quiz = data.quiz || [];
    if (!container || !quiz.length) return;

    if (currentQuestionIndex >= quiz.length) {
        container.innerHTML = `
            <div class="quiz-question">Score: ${quizScore}/${quiz.length}</div>
            <p class="quiz-feedback">Result: Perfect Husband ❤️</p>
        `;
        if (nextBtn) nextBtn.classList.add("hidden");
        return;
    }

    const q = quiz[currentQuestionIndex];
    container.innerHTML = `
        <div class="quiz-question">${q.question}</div>
        <div class="quiz-options">
            ${q.options.map((opt, i) => `<button class="quiz-option" data-index="${i}">${opt}</button>`).join("")}
        </div>
        <div class="quiz-feedback hidden" id="quiz-feedback"></div>
    `;

    if (nextBtn) {
        nextBtn.classList.remove("hidden");
        nextBtn.textContent = currentQuestionIndex === quiz.length - 1 ? "Finish" : "Next";
    }

    container.querySelectorAll(".quiz-option").forEach(btn => {
        btn.addEventListener("click", () => {
            if (selectedAnswer) return;
            selectedAnswer = true;
            const index = Number(btn.dataset.index);
            const feedback = document.getElementById("quiz-feedback");

            if (index === q.answer) {
                quizScore += 1;
                btn.classList.add("correct");
                if (feedback) feedback.textContent = q.response;
            } else {
                btn.classList.add("wrong");
                const correct = container.querySelector(`[data-index="${q.answer}"]`);
                correct?.classList.add("correct");
                if (feedback) feedback.textContent = "Almost 😄 but I still love you.";
            }

            feedback?.classList.remove("hidden");
        });
    });
}
