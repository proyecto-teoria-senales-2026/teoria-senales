(() => {
  "use strict";

  const PASSING_SCORE = 60;
  const OBJECTIVE_PASSING_SCORE = 60;
  const content = document.querySelector("#application-content");
  const nameNode = document.querySelector("#student-name");
  const runtime = window.TeoriaSenalesScorm12;

  const guidedSteps = [
    {
      title: "Reconoce el pulso rectangular",
      prompt: "Para x(t) = 1 en el intervalo −1 ≤ t ≤ 1 y cero fuera de él, identifica el límite inicial, el límite final y la duración total.",
      formula: "x(t) = 1, si −1 ≤ t ≤ 1; &nbsp; x(t) = 0, en otro caso",
      fields: [["start", "Límite inicial (s)"], ["end", "Límite final (s)"], ["duration", "Duración T (s)"]],
      expected: { start: -1, end: 1, duration: 2 },
      hint: "La duración es la diferencia entre los extremos del soporte: 1 − (−1) = 2 s.",
    },
    {
      title: "Obtén la transformada rectangular-sinc",
      prompt: "Con la convención X(f) = ∫x(t)e^(−j2πft)dt, selecciona la expresión correspondiente al pulso de amplitud 1 y duración T = 2 s.",
      formula: "X(f) = T sinc(fT), donde sinc(u) = sin(πu)/(πu)",
      expected: { transform: "correct" },
      options: [["transform", "Expresión de X(f)", [["incorrect1", "sinc(2f)"], ["correct", "2 sinc(2f)"], ["incorrect2", "2 cos(2f)"], ["incorrect3", "sinc(f/2)"]]]],
      hint: "En la expresión general T sinc(fT), sustituye T = 2. El factor T también multiplica la magnitud.",
    },
    {
      title: "Identifica valores y ceros del espectro",
      prompt: "Usa X(f) = 2 sinc(2f). Determina el valor en frecuencia cero y el primer cero positivo.",
      formula: "X(0) = área del pulso; &nbsp; ceros: f = k/T, k ≠ 0",
      fields: [["central", "X(0)"], ["zero", "Primer cero positivo (Hz)"]],
      expected: { central: 2, zero: 0.5 },
      hint: "El valor central es el área: amplitud por duración. Para los ceros usa 1/T = 1/2 Hz.",
    },
    {
      title: "Interpreta magnitud y fase",
      prompt: "Relaciona la duración temporal con el espectro y reconoce cuándo no se define la fase.",
      formula: "Mayor T → ceros más cercanos; &nbsp; fase no definida cuando |X(f)| = 0",
      expected: { width: "narrower", phase: "undefined" },
      options: [
        ["width", "Si aumenta T, el espectro:", [["wider", "Tiene ceros más separados"], ["narrower", "Tiene ceros más cercanos"], ["same", "No cambia"]]],
        ["phase", "En un cero exacto del espectro, la fase:", [["zero", "Siempre es cero"], ["undefined", "No está definida"], ["pi", "Siempre es π"]]],
      ],
      hint: "La separación entre ceros es 1/T. En los ceros la magnitud es nula y la fase no está definida.",
    },
  ];

  const questionBank = [
    ["C2-1-P01", "mc", "Para un pulso rectangular de amplitud A y duración T, ¿cuál expresión corresponde a su transformada?", "a", [["a", "AT sinc(fT)"], ["b", "A sinc(f)/T"], ["c", "AT cos(fT)"], ["d", "A/T"]]],
    ["C2-1-P02", "mc", "Para T = 2 s y A = 1, ¿cuál es X(f)?", "b", [["a", "sinc(2f)"], ["b", "2 sinc(2f)"], ["c", "2 sinc(f)"], ["d", "sinc(f/2)"]]],
    ["C2-1-P03", "mc", "¿Cuál es el primer cero positivo de 2 sinc(2f)?", "b", [["a", "0,25 Hz"], ["b", "0,5 Hz"], ["c", "1 Hz"], ["d", "2 Hz"]]],
    ["C2-1-P04", "mc", "¿Cuál es el valor X(0) del pulso de amplitud 1 y duración 2 s?", "c", [["a", "0"], ["b", "1"], ["c", "2"], ["d", "π"]]],
    ["C2-1-P05", "mc", "Al aumentar la duración T de un pulso, la separación entre ceros del espectro:", "b", [["a", "Aumenta"], ["b", "Disminuye"], ["c", "No cambia"], ["d", "Es infinita"]]],
    ["C2-1-P06", "mc", "Para el pulso propuesto, el soporte temporal es:", "a", [["a", "[−1, 1] s"], ["b", "[0, 2] s"], ["c", "[−2, 2] s"], ["d", "[−0,5, 0,5] s"]]],
    ["C2-1-P07", "mc", "¿Cuál relación describe la fase de un espectro real que cambia de signo?", "d", [["a", "Siempre vale π/2"], ["b", "No depende del signo"], ["c", "Siempre vale cero"], ["d", "Puede ser 0 o π, según el signo"]]],
    ["C2-1-P08", "mc", "Los ceros de T sinc(fT), excepto f = 0, se ubican en:", "c", [["a", "f = kT"], ["b", "f = T/k"], ["c", "f = k/T"], ["d", "f = k + T"]]],
    ["C2-1-P09", "mc", "El valor X(0) de una señal corresponde a:", "a", [["a", "El área de la señal en el tiempo"], ["b", "El primer cero"], ["c", "La fase máxima"], ["d", "La duración dividida entre dos"]]],
    ["C2-1-P10", "tf", "La magnitud del espectro de un pulso rectangular tiene forma sinc.", true],
    ["C2-1-P11", "tf", "La fase está definida en un cero exacto de la magnitud.", false],
    ["C2-1-P12", "tf", "Para el pulso propuesto, la duración total es 2 s.", true],
    ["C2-1-P13", "tf", "Un pulso de mayor duración tiene ceros más separados en frecuencia.", false],
    ["C2-1-P14", "tf", "Con A = 1 y T = 2, el valor X(0) es 2.", true],
    ["C2-1-P15", "tf", "La relación rectangular-sinc conecta una señal temporal con su espectro en frecuencia.", true],
  ];

  function seededRandom(seed) { let value = 2166136261; for (let i = 0; i < seed.length; i += 1) value = Math.imul(value ^ seed.charCodeAt(i), 16777619); return () => { value += 0x6D2B79F5; let out = value; out = Math.imul(out ^ out >>> 15, out | 1); out ^= out + Math.imul(out ^ out >>> 7, out | 61); return ((out ^ out >>> 14) >>> 0) / 4294967296; }; }
  function sample(items, count, random) { const pool = [...items]; for (let i = pool.length - 1; i > 0; i -= 1) { const j = Math.floor(random() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; } return pool.slice(0, count); }
  function selectQuestions(seed) { const random = seededRandom(seed); const picked = [...sample(questionBank.filter(q => q[1] === "mc"), 3, random), ...sample(questionBank.filter(q => q[1] === "tf"), 2, random)]; return sample(picked, picked.length, random); }
  function createState() { const identity = runtime.studentId() || runtime.studentName() || "sesion-local"; return { version: 1, seed: `${identity}-c2-1`, startedAt: new Date().toISOString(), completedAt: null, stage: 0, answers: {}, attempts: [0, 0, 0, 0], helpUsed: [false, false, false, false], evaluated: false, score: null, feedback: null }; }
  let state;
  const save = () => runtime.saveState(state);
  const progress = () => state.evaluated ? 100 : Math.round((state.stage / 5) * 100);
  const heading = current => `<div class="progress"><span>Paso ${current} de 5</span><span>${progress()} % completado</span></div><div class="progress-bar"><span style="width:${progress()}%"></span></div>`;
  const feedback = (message, kind) => message ? `<p class="feedback ${kind}">${message}</p>` : "";
  const numericEqual = (actual, expected) => Number.isFinite(actual) && Math.abs(actual - expected) <= 0.000001;
  function criterionForQuestion(id) { const number = Number(id.slice(-2)); if ([1, 2, 10].includes(number)) return "C2_1_CR2"; if ([3, 4, 8, 9, 14].includes(number)) return "C2_1_CR3"; if ([7, 11].includes(number)) return "C2_1_CR4"; if ([5, 13, 15].includes(number)) return "C2_1_CR5"; return "C2_1_CR1"; }
  function renderIntro() { content.innerHTML = `<section class="card stack"><h2>Actividad guiada</h2><p>Relaciona un pulso rectangular de tiempo continuo con su transformada de Fourier, su magnitud, fase y ceros del espectro.</p><div class="notice"><strong>Tu avance se guarda en Moodle.</strong> Puedes salir y continuar el mismo intento más tarde.</div><p class="small">La evaluación final selecciona cinco preguntas: tres de selección múltiple y dos de verdadero/falso. La nota se calcula sobre 5,0.</p><div class="actions"><button id="start">Iniciar ejercicio C-2-1</button></div></section>`; document.querySelector("#start").addEventListener("click", () => { state.stage = 1; state.feedback = null; save(); render(); }); }
  function renderGuidedStep(index) { const step = guidedSteps[index]; const saved = state.answers[index] || {}; const fields = step.fields ? step.fields.map(([key, label]) => `<label>${label}<input data-field="${key}" value="${saved[key] ?? ""}" inputmode="decimal"></label>`).join("") : ""; const optionSets = step.options ? step.options.map(([key, label, choices]) => `<fieldset><legend>${label}</legend><div class="options">${choices.map(([value, text]) => `<label class="option"><input type="radio" name="${key}" value="${value}" ${saved[key] === value ? "checked" : ""}>${text}</label>`).join("")}</div></fieldset>`).join("") : ""; content.innerHTML = `<section class="card stack">${heading(index + 1)}<h2>${step.title}</h2><p>${step.prompt}</p><p class="formula">${step.formula}</p><form id="guided-form"><div class="input-grid">${fields}</div>${optionSets}<div class="actions"><button type="submit">Verificar respuesta</button><button class="secondary" type="button" id="help" ${state.helpUsed[index] ? "disabled" : ""}>Ver orientación</button></div></form>${feedback(state.feedback, state.feedbackKind || "info")}</section>`; document.querySelector("#guided-form").addEventListener("submit", event => { event.preventDefault(); validateGuidedStep(index); }); document.querySelector("#help").addEventListener("click", () => { state.helpUsed[index] = true; state.feedback = step.hint; state.feedbackKind = "info"; save(); render(); }); }
  function validateGuidedStep(index) { const step = guidedSteps[index]; const answer = {}; (step.fields || []).forEach(([key]) => { answer[key] = document.querySelector(`[data-field="${key}"]`).value; }); (step.options || []).forEach(([key]) => { answer[key] = document.querySelector(`input[name="${key}"]:checked`)?.value || ""; }); state.answers[index] = answer; const correct = Object.entries(step.expected).every(([key, expected]) => typeof expected === "number" ? numericEqual(Number(answer[key]), expected) : answer[key] === expected); if (correct) { state.stage += 1; state.feedback = null; state.feedbackKind = null; } else { state.attempts[index] += 1; state.feedback = `El resultado todavía no coincide. Intento ${state.attempts[index]} registrado. Revisa el procedimiento y vuelve a intentarlo.`; state.feedbackKind = "error"; } save(); runtime.setProgress(progress()); render(); }
  function renderEvaluation() { const questions = selectQuestions(state.seed); content.innerHTML = `<section class="card stack">${heading(5)}<h2>Evaluación final</h2><p>Responde las cinco preguntas asignadas. La calificación final se registra en Moodle en la escala de 0 a 100.</p><form id="evaluation-form" class="stack">${questions.map(([id, type, prompt, expected, options]) => `<fieldset><legend>${id} · ${prompt}</legend><div class="options">${type === "mc" ? options.map(([key, label]) => `<label class="option"><input type="radio" name="${id}" value="${key}">${key.toUpperCase()}. ${label}</label>`).join("") : `<label class="option"><input type="radio" name="${id}" value="true">Verdadero</label><label class="option"><input type="radio" name="${id}" value="false">Falso</label>`}</div></fieldset>`).join("")}<div class="actions"><button type="submit">Calificar y finalizar</button></div></form>${feedback(state.feedback, state.feedbackKind || "info")}</section>`; document.querySelector("#evaluation-form").addEventListener("submit", event => { event.preventDefault(); gradeEvaluation(questions); }); }
  function gradeEvaluation(questions) { let correctCount = 0; const unanswered = []; const criterionResults = {}; questions.forEach(([id, type, prompt, expected]) => { const response = document.querySelector(`input[name="${id}"]:checked`)?.value; if (response === undefined) { unanswered.push(id); return; } const normalized = type === "tf" ? response === "true" : response; const correct = normalized === expected; runtime.recordInteraction({ id, type: type === "tf" ? "true-false" : "choice", response: normalized, correct, weighting: 1 }); const criterion = criterionForQuestion(id); criterionResults[criterion] ||= { correct: 0, total: 0 }; criterionResults[criterion].total += 1; if (correct) { criterionResults[criterion].correct += 1; correctCount += 1; } }); if (unanswered.length) { state.feedback = `Responde todas las preguntas antes de calificar: ${unanswered.join(", ")}.`; state.feedbackKind = "error"; render(); return; } state.evaluated = true; state.score = correctCount * 20; state.completedAt = new Date().toISOString(); state.feedback = null; runtime.setProgress(100); Object.entries(criterionResults).forEach(([id, result]) => runtime.recordObjective({ id, score: (result.correct / result.total) * 100, passingScore: OBJECTIVE_PASSING_SCORE })); runtime.reportScore({ score: state.score, passingScore: PASSING_SCORE, completed: true }); save(); render(); }
  function renderResult() { const status = state.score >= PASSING_SCORE ? "Actividad aprobada" : "Actividad finalizada"; content.innerHTML = `<section class="card stack"><p class="eyebrow">Resultado registrado</p><h2>${status}</h2><p class="score">${state.score.toFixed(2).replace(".", ",")} / 100</p><p>La actividad envió a Moodle la nota, el estado de finalización, el avance, las interacciones y los resultados por criterio.</p><div class="notice">El docente consulta la nota y la fecha/hora oficial del intento directamente desde Moodle. No necesitas descargar ni entregar un archivo adicional.</div><div class="actions"><button id="finish">Finalizar y salir</button></div></section>`; document.querySelector("#finish").addEventListener("click", () => { runtime.finish(); document.querySelector("#finish").disabled = true; }); }
  function render() { nameNode.textContent = runtime.studentName() ? `Estudiante: ${runtime.studentName()}` : "Modo de prueba local"; if (state.evaluated) renderResult(); else if (state.stage === 0) renderIntro(); else if (state.stage <= 4) renderGuidedStep(state.stage - 1); else renderEvaluation(); }

  runtime.initialize();
  state = runtime.restoreState() || createState();
  render();
})();

