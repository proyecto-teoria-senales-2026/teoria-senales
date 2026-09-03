(() => {
  "use strict";

  const PASSING_SCORE = 60;
  const OBJECTIVE_PASSING_SCORE = 60;
  const content = document.querySelector("#application-content");
  const nameNode = document.querySelector("#student-name");
  const runtime = window.TeoriaSenalesScorm12;

  const guidedSteps = [
    {
      title: "Define la malla temporal y frecuencial",
      prompt: "Para el pulso centrado x(t) = 1 si |t| < 1, muestreado con Fs = 8 Hz y N = 16, calcula Δt y Δf.",
      formula: "Δt = 1/Fs &nbsp; · &nbsp; Δf = Fs/N",
      fields: [["dt", "Δt (s)"], ["df", "Δf (Hz)"]],
      expected: { dt: 0.125, df: 0.5 },
      hint: "Sustituye Fs = 8 y N = 16: Δt = 1/8 y Δf = 8/16.",
    },
    {
      title: "Escala la FFT",
      prompt: "Elige la operación que aproxima la transformada continua X(f) a partir de las muestras x[n].",
      formula: "X(fₖ) ≈ Δt · FFT{x[n]}",
      expected: { scale: "correct" },
      options: [["scale", "Operación de escalamiento", [["a", "FFT{x[n]} / Δt"], ["correct", "Δt · FFT{x[n]}"], ["c", "Fs · FFT{x[n]}"], ["d", "FFT{x[n]} sin escalamiento"]]]],
      hint: "El intervalo temporal Δt aporta las unidades y la escala de la suma que aproxima la integral.",
    },
    {
      title: "Centra el espectro",
      prompt: "Tras calcular la FFT, identifica el procedimiento que ubica la frecuencia cero en el centro y verifica los valores de referencia del pulso.",
      formula: "X(f) = 2 sinc(2f) &nbsp; · &nbsp; X(0) = 2 &nbsp; · &nbsp; primer cero: 0,5 Hz",
      fields: [["central", "X(0)"], ["zero", "Primer cero positivo (Hz)"]],
      expected: { shift: "center", central: 2, zero: 0.5 },
      options: [["shift", "Para centrar el espectro se usa:", [["left", "Una suma acumulada"], ["center", "fftshift"], ["right", "Una derivada temporal"]]]],
      hint: "fftshift reordena los bins de la FFT para mostrar f = 0 en el centro. El valor central coincide con el área del pulso.",
    },
    {
      title: "Interpreta la resolución espectral",
      prompt: "Manteniendo Fs fijo, indica qué ocurre con Δf cuando se aumenta N y selecciona la razón correcta.",
      formula: "Δf = Fs/N",
      expected: { resolution: "decreases" },
      options: [["resolution", "Al aumentar N con Fs fijo, Δf:", [["increases", "Aumenta: hay menos muestras"], ["decreases", "Disminuye: hay mayor resolución en frecuencia"], ["same", "No cambia"]]]],
      hint: "N aparece en el denominador de Δf = Fs/N; un valor mayor de N separa menos los bins de frecuencia.",
    },
  ];

  const questionBank = [
    ["C2-2-P01", "mc", "Con Fs = 8 Hz, ¿cuál es Δt?", "b", [["a", "0,5 s"], ["b", "0,125 s"], ["c", "8 s"], ["d", "16 s"]]],
    ["C2-2-P02", "mc", "Con Fs = 8 Hz y N = 16, ¿cuál es Δf?", "c", [["a", "8 Hz"], ["b", "2 Hz"], ["c", "0,5 Hz"], ["d", "0,125 Hz"]]],
    ["C2-2-P03", "mc", "¿Qué escala aproxima la transformada continua usando la FFT?", "b", [["a", "FFT{x[n]} / Δt"], ["b", "Δt · FFT{x[n]}"], ["c", "Fs · FFT{x[n]}"], ["d", "FFT{x[n]} sin escala"]]],
    ["C2-2-P04", "mc", "¿Qué función centra la frecuencia cero al visualizar la FFT?", "b", [["a", "ifft"], ["b", "fftshift"], ["c", "abs"], ["d", "real"]]],
    ["C2-2-P05", "mc", "Para x(t) = 1 si |t| < 1, ¿cuál es el valor teórico X(0)?", "d", [["a", "0"], ["b", "0,5"], ["c", "1"], ["d", "2"]]],
    ["C2-2-P06", "mc", "¿En qué frecuencia está el primer cero positivo de 2 sinc(2f)?", "b", [["a", "0,125 Hz"], ["b", "0,5 Hz"], ["c", "1 Hz"], ["d", "2 Hz"]]],
    ["C2-2-P07", "mc", "Si Fs se mantiene fijo y N aumenta, la resolución Δf:", "b", [["a", "Aumenta"], ["b", "Disminuye"], ["c", "No cambia"], ["d", "Se vuelve negativa"]]],
    ["C2-2-P08", "mc", "¿Qué parámetro determina directamente el intervalo de muestreo Δt?", "a", [["a", "La frecuencia de muestreo Fs"], ["b", "El número de puntos N"], ["c", "El primer cero"], ["d", "La fase"]]],
    ["C2-2-P09", "mc", "Después de fftshift, la frecuencia cero se muestra:", "c", [["a", "En el extremo derecho"], ["b", "En el extremo izquierdo"], ["c", "En el centro del eje"], ["d", "Fuera del gráfico"]]],
    ["C2-2-P10", "tf", "Multiplicar la FFT por Δt permite aproximar la escala de la transformada continua.", true],
    ["C2-2-P11", "tf", "Con Fs fijo, aumentar N empeora la resolución en frecuencia.", false],
    ["C2-2-P12", "tf", "La relación Δf = Fs/N permite obtener la separación entre bins de frecuencia.", true],
    ["C2-2-P13", "tf", "Una FFT sin escalamiento por Δt conserva automáticamente las unidades de la transformada continua.", false],
    ["C2-2-P14", "tf", "Para el pulso propuesto, X(0) coincide con el área de la señal temporal.", true],
    ["C2-2-P15", "tf", "Con una malla frecuencial más densa se facilita comparar la aproximación numérica con la referencia teórica.", true],
  ];

  function seededRandom(seed) { let value = 2166136261; for (let i = 0; i < seed.length; i += 1) value = Math.imul(value ^ seed.charCodeAt(i), 16777619); return () => { value += 0x6D2B79F5; let out = value; out = Math.imul(out ^ out >>> 15, out | 1); out ^= out + Math.imul(out ^ out >>> 7, out | 61); return ((out ^ out >>> 14) >>> 0) / 4294967296; }; }
  function sample(items, count, random) { const pool = [...items]; for (let i = pool.length - 1; i > 0; i -= 1) { const j = Math.floor(random() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; } return pool.slice(0, count); }
  function selectQuestions(seed) { const random = seededRandom(seed); const chosen = [...sample(questionBank.filter(q => q[1] === "mc"), 3, random), ...sample(questionBank.filter(q => q[1] === "tf"), 2, random)]; return sample(chosen, chosen.length, random); }
  function createState() { const identity = runtime.studentId() || runtime.studentName() || "sesion-local"; return { version: 1, seed: `${identity}-c2-2`, startedAt: new Date().toISOString(), completedAt: null, stage: 0, answers: {}, attempts: [0, 0, 0, 0], helpUsed: [false, false, false, false], evaluated: false, score: null, feedback: null }; }
  let state;
  const save = () => runtime.saveState(state);
  const progress = () => state.evaluated ? 100 : Math.round((state.stage / 5) * 100);
  const heading = current => `<div class="progress"><span>Paso ${current} de 5</span><span>${progress()} % completado</span></div><div class="progress-bar"><span style="width:${progress()}%"></span></div>`;
  const feedback = (message, kind) => message ? `<p class="feedback ${kind}">${message}</p>` : "";
  const numericEqual = (actual, expected) => Number.isFinite(actual) && Math.abs(actual - expected) <= 0.000001;
  function criterionForQuestion(id) { const n = Number(id.slice(-2)); if ([1, 2, 8, 12].includes(n)) return "C2_2_CR1"; if ([3, 10, 13].includes(n)) return "C2_2_CR2"; if ([4, 9].includes(n)) return "C2_2_CR3"; if ([5, 6, 14].includes(n)) return "C2_2_CR4"; return "C2_2_CR5"; }

  function renderIntro() { content.innerHTML = `<section class="card stack"><h2>Actividad guiada</h2><p>Aplica la FFT para aproximar la transformada continua de un pulso rectangular y contrasta la malla numérica con la referencia teórica.</p><div class="notice"><strong>Tu avance se guarda en Moodle.</strong> Puedes salir y continuar el mismo intento más tarde.</div><p class="small">La evaluación final selecciona cinco preguntas: tres de selección múltiple y dos de verdadero/falso. La nota se calcula sobre 5,0.</p><div class="actions"><button id="start">Iniciar ejercicio C-2-2</button></div></section>`; document.querySelector("#start").addEventListener("click", () => { state.stage = 1; state.feedback = null; save(); render(); }); }
  function renderGuidedStep(index) { const step = guidedSteps[index]; const saved = state.answers[index] || {}; const fields = (step.fields || []).map(([key, label]) => `<label>${label}<input data-field="${key}" value="${saved[key] ?? ""}" inputmode="decimal"></label>`).join(""); const optionSets = (step.options || []).map(([key, label, choices]) => `<fieldset><legend>${label}</legend><div class="options">${choices.map(([value, text]) => `<label class="option"><input type="radio" name="${key}" value="${value}" ${saved[key] === value ? "checked" : ""}>${text}</label>`).join("")}</div></fieldset>`).join(""); content.innerHTML = `<section class="card stack">${heading(index + 1)}<h2>${step.title}</h2><p>${step.prompt}</p><p class="formula">${step.formula}</p><form id="guided-form"><div class="input-grid">${fields}</div>${optionSets}<div class="actions"><button type="submit">Verificar respuesta</button><button class="secondary" type="button" id="help" ${state.helpUsed[index] ? "disabled" : ""}>Ver orientación</button></div></form>${feedback(state.feedback, state.feedbackKind || "info")}</section>`; document.querySelector("#guided-form").addEventListener("submit", event => { event.preventDefault(); validateGuidedStep(index); }); document.querySelector("#help").addEventListener("click", () => { state.helpUsed[index] = true; state.feedback = step.hint; state.feedbackKind = "info"; save(); render(); }); }
  function validateGuidedStep(index) { const step = guidedSteps[index]; const answer = {}; (step.fields || []).forEach(([key]) => { answer[key] = document.querySelector(`[data-field="${key}"]`).value; }); (step.options || []).forEach(([key]) => { answer[key] = document.querySelector(`input[name="${key}"]:checked`)?.value || ""; }); state.answers[index] = answer; const correct = Object.entries(step.expected).every(([key, expected]) => typeof expected === "number" ? numericEqual(Number(answer[key]), expected) : answer[key] === expected); if (correct) { state.stage += 1; state.feedback = null; state.feedbackKind = null; } else { state.attempts[index] += 1; state.feedback = `El resultado todavía no coincide. Intento ${state.attempts[index]} registrado. Revisa el procedimiento y vuelve a intentarlo.`; state.feedbackKind = "error"; } save(); runtime.setProgress(progress()); render(); }
  function renderEvaluation() { const questions = selectQuestions(state.seed); content.innerHTML = `<section class="card stack">${heading(5)}<h2>Evaluación final</h2><p>Responde las cinco preguntas asignadas. La calificación final se registra en Moodle en la escala de 0 a 100.</p><form id="evaluation-form" class="stack">${questions.map(([id, type, prompt, expected, options]) => `<fieldset><legend>${id} · ${prompt}</legend><div class="options">${type === "mc" ? options.map(([key, label]) => `<label class="option"><input type="radio" name="${id}" value="${key}">${key.toUpperCase()}. ${label}</label>`).join("") : `<label class="option"><input type="radio" name="${id}" value="true">Verdadero</label><label class="option"><input type="radio" name="${id}" value="false">Falso</label>`}</div></fieldset>`).join("")}<div class="actions"><button type="submit">Calificar y finalizar</button></div></form>${feedback(state.feedback, state.feedbackKind || "info")}</section>`; document.querySelector("#evaluation-form").addEventListener("submit", event => { event.preventDefault(); gradeEvaluation(questions); }); }
  function gradeEvaluation(questions) { let correctCount = 0; const unanswered = []; const criterionResults = {}; questions.forEach(([id, type, prompt, expected]) => { const response = document.querySelector(`input[name="${id}"]:checked`)?.value; if (response === undefined) { unanswered.push(id); return; } const normalized = type === "tf" ? response === "true" : response; const correct = normalized === expected; runtime.recordInteraction({ id, type: type === "tf" ? "true-false" : "choice", response: normalized, correct, weighting: 1 }); const criterion = criterionForQuestion(id); criterionResults[criterion] ||= { correct: 0, total: 0 }; criterionResults[criterion].total += 1; if (correct) { criterionResults[criterion].correct += 1; } }); if (unanswered.length) { state.feedback = `Responde todas las preguntas antes de calificar: ${unanswered.join(", ")}.`; state.feedbackKind = "error"; render(); return; } Object.values(criterionResults).forEach(result => { correctCount += result.correct; }); state.evaluated = true; state.score = correctCount * 20; state.completedAt = new Date().toISOString(); state.feedback = null; runtime.setProgress(100); Object.entries(criterionResults).forEach(([id, result]) => runtime.recordObjective({ id, score: (result.correct / result.total) * 100, passingScore: OBJECTIVE_PASSING_SCORE })); runtime.reportScore({ score: state.score, passingScore: PASSING_SCORE, completed: true }); save(); render(); }
  function renderResult() { const status = state.score >= PASSING_SCORE ? "Actividad aprobada" : "Actividad finalizada"; content.innerHTML = `<section class="card stack"><p class="eyebrow">Resultado registrado</p><h2>${status}</h2><p class="score">${state.score.toFixed(2).replace(".", ",")} / 100</p><p>La actividad envió a Moodle la nota, el estado de finalización, el avance, las interacciones y los resultados por criterio.</p><div class="notice">El docente consulta la nota y la fecha/hora oficial del intento directamente desde Moodle. No necesitas descargar ni entregar un archivo adicional.</div><div class="actions"><button id="finish">Finalizar y salir</button></div></section>`; document.querySelector("#finish").addEventListener("click", () => { runtime.finish(); document.querySelector("#finish").disabled = true; }); }
  function render() { nameNode.textContent = runtime.studentName() ? `Estudiante: ${runtime.studentName()}` : "Modo de prueba local"; if (state.evaluated) renderResult(); else if (state.stage === 0) renderIntro(); else if (state.stage <= 4) renderGuidedStep(state.stage - 1); else renderEvaluation(); }

  runtime.initialize();
  state = runtime.restoreState() || createState();
  render();
})();

