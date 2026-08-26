(() => {
  "use strict";

  const PASSING_SCORE = 3;
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
      title: "Recupera el orden y escala de reconstrucción",
      prompt: "El espectro fue centrado para visualizarlo. Selecciona el orden y la expresión necesarios antes de reconstruir la señal.",
      formula: "xrec[n] ≈ (1/Δt) · IFFT{X[k]}",
      expected: { order: "ifftshift", scale: "inverse" },
      options: [["order", "Antes de aplicar IFFT al espectro centrado:", [["fftshift", "Se aplica fftshift de nuevo"], ["ifftshift", "Se aplica ifftshift"], ["none", "No se modifica el orden"]]], ["scale", "Escala de reconstrucción:", [["direct", "Δt · IFFT{X[k]}"], ["inverse", "(1/Δt) · IFFT{X[k]}"], ["none", "IFFT{X[k]} sin escala"]]]],
      hint: "fftshift solo centra la visualización. Antes de IFFT se recupera el orden con ifftshift y se compensa la escala con 1/Δt.",
    },
    {
      title: "Verifica la reconstrucción temporal",
      prompt: "Completa las amplitudes esperadas de la señal reconstruida para el pulso teórico x(t) = 1 si |t| < 1 s.",
      formula: "xrec[n] ≈ 1 dentro del soporte &nbsp; · &nbsp; xrec[n] ≈ 0 fuera del soporte",
      fields: [["inside", "Amplitud dentro del soporte"], ["outside", "Amplitud fuera del soporte"]],
      expected: { inside: 1, outside: 0 },
      hint: "La reconstrucción debe conservar la amplitud unitaria del pulso y tender a cero fuera de su soporte.",
    },
    {
      title: "Interpreta la aproximación numérica",
      prompt: "Selecciona la explicación adecuada para pequeñas diferencias entre la señal teórica y la reconstrucción numérica.",
      formula: "Muestreo finito y número limitado de bins",
      expected: { cause: "finite" },
      options: [["cause", "Las pequeñas diferencias se explican principalmente por:", [["finite", "El muestreo finito y la aproximación numérica"], ["wrong", "Que la IFFT no puede reconstruir señales"], ["zero", "Que la frecuencia de muestreo siempre es cero"]]]],
      hint: "Una reconstrucción numérica usa una cantidad finita de muestras y bins; esto puede producir diferencias pequeñas sin invalidar el procedimiento.",
    },
  ];

  const questionBank = [
    ["C2-4-P01", "mc", "Con Fs = 8 Hz, ¿cuál es Δt?", "b", [["a", "0,5 s"], ["b", "0,125 s"], ["c", "8 s"], ["d", "16 s"]]],
    ["C2-4-P02", "mc", "Con Fs = 8 Hz y N = 16, ¿cuál es Δf?", "c", [["a", "8 Hz"], ["b", "2 Hz"], ["c", "0,5 Hz"], ["d", "0,125 Hz"]]],
    ["C2-4-P03", "mc", "¿Qué factor acompaña a la IFFT para reconstruir x[n] cuando X[k] se obtuvo como Δt·FFT{x[n]}?", "b", [["a", "Δt"], ["b", "1/Δt"], ["c", "Δf"], ["d", "1/N solamente"]]],
    ["C2-4-P04", "mc", "Si el espectro se visualiza con fftshift, ¿qué operación se aplica antes de IFFT?", "b", [["a", "fftshift"], ["b", "ifftshift"], ["c", "abs"], ["d", "real"]]],
    ["C2-4-P05", "mc", "Para el pulso teórico, la amplitud dentro del soporte reconstruido debe ser aproximadamente:", "c", [["a", "0"], ["b", "0,5"], ["c", "1"], ["d", "8"]]],
    ["C2-4-P06", "mc", "La IFFT transforma principalmente información del dominio:", "b", [["a", "Temporal al temporal"], ["b", "Frecuencial al temporal"], ["c", "Temporal al frecuencial"], ["d", "Espacial al temporal"]]],
    ["C2-4-P07", "mc", "¿Qué se debe comparar para validar la reconstrucción?", "b", [["a", "Solo el nombre del archivo"], ["b", "El soporte y la amplitud con la señal teórica"], ["c", "Únicamente Δf"], ["d", "El color del gráfico"]]],
    ["C2-4-P08", "mc", "Con Fs fijo, si N aumenta, Δf:", "a", [["a", "Disminuye"], ["b", "Aumenta"], ["c", "No cambia"], ["d", "Se vuelve negativa"]]],
    ["C2-4-P09", "mc", "Un espectro muestreado permite obtener mediante IFFT:", "a", [["a", "Una aproximación de la señal temporal"], ["b", "Una derivada exacta siempre"], ["c", "Una señal sin unidades"], ["d", "Solo una frecuencia"]]],
    ["C2-4-P10", "tf", "El factor 1/Δt compensa la escala usada en la FFT directa.", true],
    ["C2-4-P11", "tf", "fftshift cambia la información del espectro.", false],
    ["C2-4-P12", "tf", "El uso de una cantidad finita de muestras puede producir diferencias pequeñas frente a la señal teórica.", true],
    ["C2-4-P13", "tf", "La IFFT permite volver de bins de frecuencia a muestras temporales.", true],
    ["C2-4-P14", "tf", "Para el pulso ideal, la señal reconstruida debe ser aproximadamente cero fuera del soporte.", true],
    ["C2-4-P15", "tf", "Con Fs fijo, aumentar N empeora necesariamente la resolución Δf.", false],
  ];

  function seededRandom(seed) { let value = 2166136261; for (let i = 0; i < seed.length; i += 1) value = Math.imul(value ^ seed.charCodeAt(i), 16777619); return () => { value += 0x6D2B79F5; let out = value; out = Math.imul(out ^ out >>> 15, out | 1); out ^= out + Math.imul(out ^ out >>> 7, out | 61); return ((out ^ out >>> 14) >>> 0) / 4294967296; }; }
  function sample(items, count, random) { const pool = [...items]; for (let i = pool.length - 1; i > 0; i -= 1) { const j = Math.floor(random() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; } return pool.slice(0, count); }
  function selectQuestions(seed) { const random = seededRandom(seed); const chosen = [...sample(questionBank.filter(q => q[1] === "mc"), 3, random), ...sample(questionBank.filter(q => q[1] === "tf"), 2, random)]; return sample(chosen, chosen.length, random); }
  function createState() { const identity = runtime.studentId() || runtime.studentName() || "sesion-local"; return { version: 1, seed: `${identity}-c2-4`, startedAt: new Date().toISOString(), completedAt: null, stage: 0, answers: {}, attempts: [0, 0, 0, 0], helpUsed: [false, false, false, false], evaluated: false, score: null, feedback: null }; }
  let state;
  const save = () => runtime.saveState(state);
  const progress = () => state.evaluated ? 100 : Math.round((state.stage / 5) * 100);
  const heading = current => `<div class="progress"><span>Paso ${current} de 5</span><span>${progress()} % completado</span></div><div class="progress-bar"><span style="width:${progress()}%"></span></div>`;
  const feedback = (message, kind) => message ? `<p class="feedback ${kind}">${message}</p>` : "";
  const numericEqual = (actual, expected) => Number.isFinite(actual) && Math.abs(actual - expected) <= 0.000001;
  function criterionForQuestion(id) { const n = Number(id.slice(-2)); if ([1, 2].includes(n)) return "C2_4_CR1"; if ([3, 4, 10, 11].includes(n)) return "C2_4_CR2"; if ([5, 6, 13].includes(n)) return "C2_4_CR3"; if ([7, 9, 14].includes(n)) return "C2_4_CR4"; return "C2_4_CR5"; }

  function renderIntro() { content.innerHTML = `<section class="card stack"><h2>Actividad guiada</h2><p>Reconstruye en el tiempo un pulso rectangular a partir de su espectro, aplicando la IFFT, el orden correcto de los bins y el escalamiento requerido.</p><div class="notice"><strong>Tu avance se guarda en Moodle.</strong> Puedes salir y continuar el mismo intento más tarde.</div><p class="small">La evaluación final selecciona cinco preguntas: tres de selección múltiple y dos de verdadero/falso. La nota se calcula sobre 5,0.</p><div class="actions"><button id="start">Iniciar ejercicio C-2-4</button></div></section>`; document.querySelector("#start").addEventListener("click", () => { state.stage = 1; state.feedback = null; save(); render(); }); }
  function renderGuidedStep(index) { const step = guidedSteps[index]; const saved = state.answers[index] || {}; const fields = (step.fields || []).map(([key, label]) => `<label>${label}<input data-field="${key}" value="${saved[key] ?? ""}" inputmode="decimal"></label>`).join(""); const optionSets = (step.options || []).map(([key, label, choices]) => `<fieldset><legend>${label}</legend><div class="options">${choices.map(([value, text]) => `<label class="option"><input type="radio" name="${key}" value="${value}" ${saved[key] === value ? "checked" : ""}>${text}</label>`).join("")}</div></fieldset>`).join(""); content.innerHTML = `<section class="card stack">${heading(index + 1)}<h2>${step.title}</h2><p>${step.prompt}</p><p class="formula">${step.formula}</p><form id="guided-form"><div class="input-grid">${fields}</div>${optionSets}<div class="actions"><button type="submit">Verificar respuesta</button><button class="secondary" type="button" id="help" ${state.helpUsed[index] ? "disabled" : ""}>Ver orientación</button></div></form>${feedback(state.feedback, state.feedbackKind || "info")}</section>`; document.querySelector("#guided-form").addEventListener("submit", event => { event.preventDefault(); validateGuidedStep(index); }); document.querySelector("#help").addEventListener("click", () => { state.helpUsed[index] = true; state.feedback = step.hint; state.feedbackKind = "info"; save(); render(); }); }
  function validateGuidedStep(index) { const step = guidedSteps[index]; const answer = {}; (step.fields || []).forEach(([key]) => { answer[key] = document.querySelector(`[data-field="${key}"]`).value; }); (step.options || []).forEach(([key]) => { answer[key] = document.querySelector(`input[name="${key}"]:checked`)?.value || ""; }); state.answers[index] = answer; const correct = Object.entries(step.expected).every(([key, expected]) => typeof expected === "number" ? numericEqual(Number(answer[key]), expected) : answer[key] === expected); if (correct) { state.stage += 1; state.feedback = null; state.feedbackKind = null; } else { state.attempts[index] += 1; state.feedback = `El resultado todavía no coincide. Intento ${state.attempts[index]} registrado. Revisa el procedimiento y vuelve a intentarlo.`; state.feedbackKind = "error"; } save(); runtime.setProgress(progress()); render(); }
  function renderEvaluation() { const questions = selectQuestions(state.seed); content.innerHTML = `<section class="card stack">${heading(5)}<h2>Evaluación final</h2><p>Responde las cinco preguntas asignadas. La calificación final se registra en Moodle en la escala de 0,0 a 5,0.</p><form id="evaluation-form" class="stack">${questions.map(([id, type, prompt, expected, options]) => `<fieldset><legend>${id} · ${prompt}</legend><div class="options">${type === "mc" ? options.map(([key, label]) => `<label class="option"><input type="radio" name="${id}" value="${key}">${key.toUpperCase()}. ${label}</label>`).join("") : `<label class="option"><input type="radio" name="${id}" value="true">Verdadero</label><label class="option"><input type="radio" name="${id}" value="false">Falso</label>`}</div></fieldset>`).join("")}<div class="actions"><button type="submit">Calificar y finalizar</button></div></form>${feedback(state.feedback, state.feedbackKind || "info")}</section>`; document.querySelector("#evaluation-form").addEventListener("submit", event => { event.preventDefault(); gradeEvaluation(questions); }); }
  function gradeEvaluation(questions) { let correctCount = 0; const unanswered = []; const criterionResults = {}; questions.forEach(([id, type, prompt, expected]) => { const response = document.querySelector(`input[name="${id}"]:checked`)?.value; if (response === undefined) { unanswered.push(id); return; } const normalized = type === "tf" ? response === "true" : response; const correct = normalized === expected; runtime.recordInteraction({ id, type: type === "tf" ? "true-false" : "choice", response: normalized, correct, weighting: 1 }); const criterion = criterionForQuestion(id); criterionResults[criterion] ||= { correct: 0, total: 0 }; criterionResults[criterion].total += 1; if (correct) { criterionResults[criterion].correct += 1; } }); if (unanswered.length) { state.feedback = `Responde todas las preguntas antes de calificar: ${unanswered.join(", ")}.`; state.feedbackKind = "error"; render(); return; } Object.values(criterionResults).forEach(result => { correctCount += result.correct; }); state.evaluated = true; state.score = correctCount; state.completedAt = new Date().toISOString(); state.feedback = null; runtime.setProgress(100); Object.entries(criterionResults).forEach(([id, result]) => runtime.recordObjective({ id, score: (result.correct / result.total) * 100, passingScore: OBJECTIVE_PASSING_SCORE })); runtime.reportScore({ score: state.score, passingScore: PASSING_SCORE, maxScore: 5, completed: true }); save(); render(); }
  function renderResult() { const status = state.score >= PASSING_SCORE ? "Actividad aprobada" : "Actividad finalizada"; content.innerHTML = `<section class="card stack"><p class="eyebrow">Resultado registrado</p><h2>${status}</h2><p class="score">${state.score.toFixed(2).replace(".", ",")} / 5,0</p><p>La actividad envió a Moodle la nota, el estado de finalización, el avance, las interacciones y los resultados por criterio.</p><div class="notice">El docente consulta la nota y la fecha/hora oficial del intento directamente desde Moodle. No necesitas descargar ni entregar un archivo adicional.</div><div class="actions"><button id="finish">Finalizar y salir</button></div></section>`; document.querySelector("#finish").addEventListener("click", () => { runtime.finish(); document.querySelector("#finish").disabled = true; }); }
  function render() { nameNode.textContent = runtime.studentName() ? `Estudiante: ${runtime.studentName()}` : "Modo de prueba local"; if (state.evaluated) renderResult(); else if (state.stage === 0) renderIntro(); else if (state.stage <= 4) renderGuidedStep(state.stage - 1); else renderEvaluation(); }

  runtime.initialize();
  state = runtime.restoreState() || createState();
  render();
})();
