import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Modello di Ising ferromagnetico",
    layout="wide"
)

st.title("Modello di Ising ferromagnetico")

st.latex(r"""
H=-J\sum_{\langle i,j\rangle}s_i s_j,
\qquad s_i=\pm1,
\qquad J>0
""")

st.write(
    "Modello di Ising bidimensionale con dinamica di Metropolis. "
    "Gli spin vicini tendono ad allinearsi, mentre la temperatura "
    "introduce fluttuazioni."
)


# =========================================================
# DIMENSIONE DELLA RETE
# =========================================================

L = 50

# =========================================================
# STATO INIZIALE
# =========================================================

initial_state = st.radio(
    "Stato iniziale",
    ["Casuale", "Ordinato"],
    horizontal=True
)

ordered = "true" if initial_state == "Ordinato" else "false"


# =========================================================
# COMPONENTE HTML / JAVASCRIPT
# =========================================================

html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<style>

body {{
    margin: 0;
    padding: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: transparent;
    color: #333;
}}

.wrapper {{
    width: 100%;
}}


/* =====================================================
   CONTROLLI
   ===================================================== */

.controls {{

    display: flex;

    align-items: center;

    gap: 22px;

    flex-wrap: wrap;

    margin-bottom: 18px;

}}

.control-group {{

    display: flex;

    align-items: center;

    gap: 8px;

}}

.control-label {{

    font-size: 14px;

    color: #555;

    white-space: nowrap;

}}

input[type="range"] {{

    width: 150px;

    cursor: pointer;

}}

.value {{

    display: inline-block;

    width: 45px;

    font-size: 14px;

    font-weight: 500;

}}


button {{

    border: 1px solid #aaa;

    background: #f5f4ef;

    border-radius: 6px;

    padding: 7px 15px;

    font-size: 14px;

    cursor: pointer;

}}

button:hover {{

    background: #e8e6df;

}}


/* =====================================================
   LAYOUT
   ===================================================== */

.main {{

    display: flex;

    gap: 30px;

    align-items: flex-start;

}}


.left {{

    flex: 0 0 auto;

}}


.right {{

    width: 320px;

    flex: 0 0 320px;

}}


/* =====================================================
   CANVAS RETE
   ===================================================== */

#ising {{

    display: block;

    border: 1px solid #c9c7c0;

    border-radius: 5px;

    background: #faf9f5;

    max-width: 100%;

}}


/* =====================================================
   METRICHE
   ===================================================== */

.metric {{

    margin-bottom: 16px;

}}

.metric-title {{

    font-size: 13px;

    color: #777;

    margin-bottom: 3px;

}}

.metric-value {{

    font-size: 24px;

    font-weight: 500;

}}


.bar-container {{

    width: 230px;

    height: 10px;

    background: #e7e5df;

    border: 1px solid #ccc;

    margin-top: 6px;

}}

.bar {{

    height: 100%;

    width: 0%;

    background: #657762;

}}


/* =====================================================
   GRAFICO
   ===================================================== */

.chart-container {{

    margin-top: 22px;

}}

.chart-title {{

    font-size: 13px;

    color: #777;

    margin-bottom: 5px;

}}

#chart {{

    width: 320px;

    height: 190px;

    border: 1px solid #ddd;

    background: white;

    display: block;

}}


/* =====================================================
   LEGENDA
   ===================================================== */

.chart-legend {{

    display: flex;

    gap: 18px;

    margin-top: 7px;

    font-size: 12px;

    color: #666;

}}

.legend-item {{

    display: flex;

    align-items: center;

    gap: 5px;

}}

.legend-line {{

    width: 24px;

    height: 2px;

}}

.legend-m {{

    background: #777;

}}

.legend-abs {{

    background: #465b48;

}}


.info {{

    margin-top: 12px;

    font-size: 12px;

    color: #777;

    line-height: 1.5;

}}

</style>

</head>


<body>


<div class="wrapper">


<!-- =====================================================
     CONTROLLI
     ===================================================== -->

<div class="controls">


    <button id="play">
        ▶ Play
    </button>


    <button id="reset">
        ↻ Reset
    </button>


    <div class="control-group">

        <span class="control-label">
            T/J
        </span>

        <input
            type="range"
            id="temperature"
            min="0.1"
            max="5.0"
            step="0.1"
            value="2.0"
        >

        <span
            class="value"
            id="temperatureValue"
        >
            2.0
        </span>

    </div>


    <div class="control-group">

        <span class="control-label">
            Velocità
        </span>

        <input
            type="range"
            id="speed"
            min="1"
            max="20"
            step="1"
            value="5"
        >

        <span
            class="value"
            id="speedValue"
        >
            5
        </span>

    </div>


    <div class="control-group">

        <span class="control-label">
            Rete
        </span>

        <input
            type="range"
            id="size"
            min="10"
            max="150"
            step="1"
            value="{L}"
        >

        <span
            class="value"
            id="sizeValue"
        >
            {L}
        </span>

    </div>


</div>


<!-- =====================================================
     SIMULAZIONE
     ===================================================== -->

<div class="main">


<div class="left">

    <canvas id="ising"></canvas>

</div>


<div class="right">


    <div class="metric">

        <div class="metric-title">
            Sweep
        </div>

        <div
            class="metric-value"
            id="sweep"
        >
            0
        </div>

    </div>


    <div class="metric">

        <div class="metric-title">
            Magnetizzazione M/N
        </div>

        <div
            class="metric-value"
            id="magnetization"
        >
            0.000
        </div>

    </div>


    <div class="metric">

        <div class="metric-title">
            |M|/N
        </div>

        <div
            class="metric-value"
            id="absmagnetization"
        >
            0.000
        </div>


        <div class="bar-container">

            <div
                class="bar"
                id="magbar"
            ></div>

        </div>

    </div>


    <div class="metric">

        <div class="metric-title">
            Energia per spin
        </div>

        <div
            class="metric-value"
            id="energy"
        >
            0.000
        </div>

    </div>


    <!-- =================================================
         GRAFICO
         ================================================= -->

    <div class="chart-container">

        <div class="chart-title">
            Magnetizzazione nel tempo
        </div>

        <canvas id="chart"></canvas>


        <div class="chart-legend">

            <div class="legend-item">

                <div
                    class="legend-line legend-m"
                ></div>

                <span>
                    M/N
                </span>

            </div>


            <div class="legend-item">

                <div
                    class="legend-line legend-abs"
                ></div>

                <span>
                    |M|/N
                </span>

            </div>

        </div>


    </div>


    <div class="info">

        <b>↑</b> spin +1 &nbsp;&nbsp;

        <b>↓</b> spin −1

        <br><br>

        Temperatura critica:

        <b>T<sub>c</sub>/J ≈ 2.269</b>

    </div>


</div>


</div>


</div>


<script>


// ========================================================
// PARAMETRI
// ========================================================

let L = {L};

const J = 1.0;

const ordered = {ordered};


// ========================================================
// CANVAS PRINCIPALE
// ========================================================

const canvas =
    document.getElementById("ising");

const ctx =
    canvas.getContext("2d");


// Dimensione massima della visualizzazione

const maxCanvasSize = 760;


// ========================================================
// CANVAS GRAFICO
// ========================================================

const chart =
    document.getElementById("chart");

const chartCtx =
    chart.getContext("2d");

chart.width = 320;

chart.height = 190;


// ========================================================
// CONTROLLI
// ========================================================

const playButton =
    document.getElementById("play");

const resetButton =
    document.getElementById("reset");


const temperatureSlider =
    document.getElementById("temperature");

const temperatureValue =
    document.getElementById("temperatureValue");


const speedSlider =
    document.getElementById("speed");

const speedValue =
    document.getElementById("speedValue");


const sizeSlider =
    document.getElementById("size");

const sizeValue =
    document.getElementById("sizeValue");


// ========================================================
// METRICHE
// ========================================================

const sweepElement =
    document.getElementById("sweep");

const magnetizationElement =
    document.getElementById("magnetization");

const absMagnetizationElement =
    document.getElementById("absmagnetization");

const energyElement =
    document.getElementById("energy");

const barElement =
    document.getElementById("magbar");


// ========================================================
// STATO
// ========================================================

let T = 2.0;

let speed = 5;

let spins = [];

let sweep = 0;

let running = false;

let animationID = null;


// Magnetizzazione ed energia vengono mantenute
// incrementalmente.

let M = 0;

let E = 0;


// ========================================================
// STORICO GRAFICO
// ========================================================

let historyM = [];

let historyAbsM = [];

const maxHistory = 500;


// ========================================================
// DIMENSIONAMENTO CANVAS
// ========================================================

function resizeCanvas() {{

    const size =
        Math.floor(
            maxCanvasSize / L
        );

    canvas.width =
        size * L;

    canvas.height =
        size * L;

}}


// ========================================================
// INIZIALIZZAZIONE
// ========================================================

function initialize() {{

    resizeCanvas();


    spins = new Array(L);


    M = 0;

    E = 0;


    for (let i = 0; i < L; i++) {{

        spins[i] =
            new Int8Array(L);


        for (let j = 0; j < L; j++) {{

            let s;


            if (ordered) {{

                s = 1;

            }} else {{

                s =
                    Math.random() < 0.5
                    ? -1
                    : 1;

            }}


            spins[i][j] = s;

            M += s;

        }}

    }}


    // Energia iniziale.
    //
    // Ogni legame viene contato una sola volta:
    // destra + basso.

    for (let i = 0; i < L; i++) {{

        for (let j = 0; j < L; j++) {{

            const s =
                spins[i][j];


            const right =
                spins[i][
                    (j + 1) % L
                ];


            const down =
                spins[
                    (i + 1) % L
                ][j];


            E +=
                -J * s * (
                    right + down
                );

        }}

    }}


    sweep = 0;


    historyM = [];

    historyAbsM = [];


    updateDisplay();

    draw();

    drawChart();

}}


// ========================================================
// BORDI PERIODICI
// ========================================================

function getSpin(i, j) {{

    if (i < 0)
        i += L;

    if (i >= L)
        i -= L;

    if (j < 0)
        j += L;

    if (j >= L)
        j -= L;


    return spins[i][j];

}}


// ========================================================
// METROPOLIS
// ========================================================

function metropolisSweep() {{

    const N = L * L;


    for (let n = 0; n < N; n++) {{

        const i =
            Math.floor(
                Math.random() * L
            );

        const j =
            Math.floor(
                Math.random() * L
            );


        const s =
            spins[i][j];


        const neighbours =

            getSpin(i + 1, j) +

            getSpin(i - 1, j) +

            getSpin(i, j + 1) +

            getSpin(i, j - 1);


        const deltaE =
            2 * J * s * neighbours;


        if (
            deltaE <= 0 ||
            Math.random()
            < Math.exp(
                -deltaE / T
            )
        ) {{

            // ------------------------------------------------
            // AGGIORNAMENTO INCREMENTALE
            // ------------------------------------------------

            spins[i][j] = -s;


            // Magnetizzazione

            M += -2 * s;


            // Energia

            E += deltaE;

        }}

    }}


    sweep++;

}}


// ========================================================
// AGGIORNA DISPLAY
// ========================================================

function updateDisplay() {{

    const N = L * L;


    const m =
        M / N;


    const absM =
        Math.abs(m);


    const e =
        E / N;


    sweepElement.textContent =
        sweep.toLocaleString();


    magnetizationElement.textContent =
        m.toFixed(3);


    absMagnetizationElement.textContent =
        absM.toFixed(3);


    energyElement.textContent =
        e.toFixed(3);


    barElement.style.width =
        (absM * 100) + "%";


    // storico

    historyM.push(m);

    historyAbsM.push(absM);


    if (
        historyM.length
        > maxHistory
    ) {{

        historyM.shift();

        historyAbsM.shift();

    }}

}}


// ========================================================
// DISEGNO RETE
// ========================================================

function draw() {{

    const size =
        canvas.width / L;


    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    // ----------------------------------------------------
    // CELLE
    // ----------------------------------------------------

    for (let i = 0; i < L; i++) {{

        for (let j = 0; j < L; j++) {{

            const x =
                j * size;

            const y =
                i * size;


            if (
                spins[i][j] === 1
            ) {{

                ctx.fillStyle =
                    "#A9B9A4";

            }} else {{

                ctx.fillStyle =
                    "#D6D0C6";

            }}


            ctx.fillRect(
                x,
                y,
                size,
                size
            );

        }}

    }}


    // ----------------------------------------------------
    // FRECCE
    // ----------------------------------------------------

    /*
       Le frecce vengono mantenute anche per L=150.

       Quando la cella è piccola:
       - freccia più corta
       - tratto più sottile

       In questo modo non spariscono
       semplicemente perché L è grande.
    */


    const arrowLength =
        Math.max(
            0.45,
            size * 0.30
        );


    const center =
        size / 2;


    ctx.strokeStyle =
        "#444";

    ctx.fillStyle =
        "#444";


    ctx.lineWidth =
        Math.max(
            0.6,
            Math.min(
                2.0,
                size * 0.075
            )
        );


    /*
       Per reti molto grandi la punta
       diventa molto piccola.
    */

    const head =
        Math.max(
            0.7,
            Math.min(
                3.5,
                size * 0.13
            )
        );


    for (let i = 0; i < L; i++) {{

        for (let j = 0; j < L; j++) {{

            const cx =
                j * size + center;

            const cy =
                i * size + center;


            const direction =
                spins[i][j];


            const startY =
                cy + direction * arrowLength;


            const endY =
                cy - direction * arrowLength;


            // asta

            ctx.beginPath();

            ctx.moveTo(
                cx,
                startY
            );

            ctx.lineTo(
                cx,
                endY
            );

            ctx.stroke();


            // punta

            ctx.beginPath();

            ctx.moveTo(
                cx,
                endY
            );


            ctx.lineTo(
                cx - head,
                endY
                + direction * head
            );


            ctx.lineTo(
                cx + head,
                endY
                + direction * head
            );


            ctx.closePath();

            ctx.fill();

        }}

    }}

}}


// ========================================================
// GRAFICO
// ========================================================

function drawChart() {{

    const w =
        chart.width;

    const h =
        chart.height;


    chartCtx.clearRect(
        0,
        0,
        w,
        h
    );


    chartCtx.fillStyle =
        "#ffffff";

    chartCtx.fillRect(
        0,
        0,
        w,
        h
    );


    const left = 34;

    const right = 8;

    const top = 10;

    const bottom = 24;


    const plotW =
        w - left - right;

    const plotH =
        h - top - bottom;


    // ----------------------------------------------------
    // GRIGLIA
    // ----------------------------------------------------

    chartCtx.strokeStyle =
        "#e5e5e5";

    chartCtx.lineWidth = 1;


    for (let k = 0; k <= 4; k++) {{

        const y =
            top +
            k * plotH / 4;


        chartCtx.beginPath();

        chartCtx.moveTo(
            left,
            y
        );

        chartCtx.lineTo(
            w - right,
            y
        );

        chartCtx.stroke();

    }}


    // ----------------------------------------------------
    // VALORI ASSE Y
    // ----------------------------------------------------

    chartCtx.fillStyle =
        "#777";

    chartCtx.font =
        "11px Arial";

    chartCtx.textAlign =
        "right";


    chartCtx.fillText(
        "1",
        left - 6,
        top + 4
    );


    chartCtx.fillText(
        "0",
        left - 6,
        top +
        plotH / 2 +
        4
    );


    chartCtx.fillText(
        "-1",
        left - 6,
        top +
        plotH +
        4
    );


    // ----------------------------------------------------
    // ASSI
    // ----------------------------------------------------

    chartCtx.strokeStyle =
        "#999";


    chartCtx.beginPath();

    chartCtx.moveTo(
        left,
        top
    );

    chartCtx.lineTo(
        left,
        top + plotH
    );

    chartCtx.lineTo(
        w - right,
        top + plotH
    );

    chartCtx.stroke();


    // ----------------------------------------------------
    // DISEGNO SERIE
    // ----------------------------------------------------

    function drawSeries(
        data,
        color,
        width
    ) {{

        if (data.length < 2)
            return;


        chartCtx.strokeStyle =
            color;

        chartCtx.lineWidth =
            width;


        chartCtx.beginPath();


        for (
            let i = 0;
            i < data.length;
            i++
        ) {{

            const x =
                left
                +
                i /
                (maxHistory - 1)
                *
                plotW;


            const value =
                data[i];


            const y =
                top
                +
                (1 - (value + 1) / 2)
                *
                plotH;


            if (i === 0) {{

                chartCtx.moveTo(
                    x,
                    y
                );

            }} else {{

                chartCtx.lineTo(
                    x,
                    y
                );

            }}

        }}


        chartCtx.stroke();

    }}


    // M/N

    drawSeries(
        historyM,
        "#777777",
        1.5
    );


    // |M|/N

    drawSeries(
        historyAbsM,
        "#465B48",
        2
    );

}}


// ========================================================
// ANIMAZIONE
// ========================================================

function animate() {{

    if (!running)
        return;


    /*
       speed = 1  → 1 sweep/frame
       speed = 20 → 20 sweep/frame

       requestAnimationFrame mantiene
       l'animazione sincronizzata con
       il refresh del browser.
    */


    const sweepsPerFrame =
        speed;


    for (
        let k = 0;
        k < sweepsPerFrame;
        k++
    ) {{

        metropolisSweep();

    }}


    draw();

    updateDisplay();

    drawChart();


    animationID =
        requestAnimationFrame(
            animate
        );

}}


// ========================================================
// PLAY / PAUSA
// ========================================================

playButton.addEventListener(
    "click",
    function() {{

        running = !running;


        if (running) {{

            playButton.textContent =
                "⏸ Pausa";


            animationID =
                requestAnimationFrame(
                    animate
                );

        }} else {{

            playButton.textContent =
                "▶ Play";


            if (
                animationID !== null
            ) {{

                cancelAnimationFrame(
                    animationID
                );

            }}

        }}

    }}
);


// ========================================================
// RESET
// ========================================================

resetButton.addEventListener(
    "click",
    function() {{

        running = false;


        playButton.textContent =
            "▶ Play";


        if (
            animationID !== null
        ) {{

            cancelAnimationFrame(
                animationID
            );

        }}


        initialize();

    }}
);


// ========================================================
// TEMPERATURA
// ========================================================

temperatureSlider.addEventListener(
    "input",
    function() {{

        T =
            parseFloat(
                this.value
            );


        temperatureValue.textContent =
            T.toFixed(1);

    }}
);


// ========================================================
// VELOCITÀ
// ========================================================

speedSlider.addEventListener(
    "input",
    function() {{

        speed =
            parseInt(
                this.value
            );


        speedValue.textContent =
            speed;

    }}
);


// ========================================================
// DIMENSIONE DELLA RETE
// ========================================================

sizeSlider.addEventListener(
    "input",
    function() {{

        const newL =
            parseInt(
                this.value
            );


        sizeValue.textContent =
            newL;


        /*
           Per cambiare dimensione
           bisogna ricostruire la rete.
        */

        if (newL !== L) {{

            L = newL;

            running = false;

            playButton.textContent =
                "▶ Play";


            if (
                animationID !== null
            ) {{

                cancelAnimationFrame(
                    animationID
                );

            }}


            initialize();

        }}

    }}
);


// ========================================================
// AVVIO
// ========================================================

initialize();

</script>

</body>

</html>
"""


components.html(
    html,
    height=900,
    scrolling=False
)