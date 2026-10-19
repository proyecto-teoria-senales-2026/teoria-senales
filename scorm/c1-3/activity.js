(() => {
  "use strict";

  const PASSING_SCORE = 60;
  const OBJECTIVE_PASSING_SCORE = 60;
  const content = document.querySelector("#application-content");
  const nameNode = document.querySelector("#student-name");
  const runtime = window.TeoriaSenalesScorm12;
  const guidedSteps = [
    { title: "Periodo y frecuencia fundamental", prompt: "El pulso rectangular se repite cada 2π. Calcula T₀ y ω₀ = 2π/T₀.", formula: "x(t + 2π) = x(t); &nbsp; ω₀ = 2π/T₀", fields: [["period", "Periodo fundamental T₀"], ["omega", "Frecuencia angular ω₀"]], expected: { period: 6.283185307179586, omega: 1 }, hint: "El periodo de la señal es 2π. Sustituye ese valor en ω₀ = 2π/T₀." },
    { title: "Término constante y simetría", prompt: "La señal vale 1 para |t| ≤ π/2 y es par.", formula: "a₀ = (2/T₀)∫x(t)dt; &nbsp; valor medio = a₀/2", fields: [["a0", "Coeficiente a₀"], ["mean", "Valor medio a₀/2"], ["b1", "Coeficiente b₁"]], expected: { a0: 1, mean: 0.5, b1: 0 }, hint: "El área del pulso en un periodo es π. Como la señal es par, todos los coeficientes bₙ son cero." },
    { title: "Coeficientes de los armónicos", prompt: "Evalúa aₙ para n = 1, 2 y 3.", formula: "aₙ = (2/(πn)) sen(nπ/2); &nbsp; bₙ = 0", fields: [["a1", "Coeficiente a₁"], ["a2", "Coeficiente a₂"], ["a3", "Coeficiente a₃"]], expected: { a1: 2 / Math.PI, a2: 0, a3: -2 / (3 * Math.PI) }, hint: "Sustituye cada orden n. Para n = 2 el seno vale cero; para n = 3 el seno es negativo." },
    { title: "Espectros de amplitud y fase", prompt: "Usa los coeficientes anteriores para interpretar los armónicos primero y tercero.", formula: "Aₙ = √(aₙ²+bₙ²); &nbsp; φₙ = atan2(-bₙ,aₙ)", fields: [["A1", "Amplitud A₁"], ["phi1", "Fase φ₁ [rad]"], ["A3", "Amplitud A₃"], ["phi3", "Fase φ₃ [rad]"]], expected: { A1: 2 / Math.PI, phi1: 0, A3: 2 / (3 * Math.PI), phi3: Math.PI }, hint: "La amplitud siempre es no negativa. Si bₙ = 0 y aₙ es positivo, la fase es 0; si aₙ es negativo, la fase es π." },
  ];
  const questionBank = [
    ["C1-3-P01","mc","¿Cuál es la forma de la serie trigonométrica usada?","b",[["a","x(t)=a₀+Σaₙsen(nω₀t)"],["b","x(t)=a₀/2+Σ[aₙcos(nω₀t)+bₙsen(nω₀t)]"],["c","x(t)=Σbₙ"],["d","x(t)=a₀/2"]]],
    ["C1-3-P02","mc","Si T₀ = 2π, ¿cuál es ω₀?","a",[["a","1 rad/s"],["b","2 rad/s"],["c","π rad/s"],["d","2π rad/s"]]],
    ["C1-3-P03","mc","¿Qué integral calcula a₀?","c",[["a","(1/T₀)∫x(t)dt"],["b","∫x²(t)dt"],["c","(2/T₀)∫x(t)dt"],["d","(2/T₀)∫x(t)sen(ω₀t)dt"]]],
    ["C1-3-P04","mc","Como el pulso rectangular es par, ¿qué ocurre con bₙ?","d",[["a","bₙ=1"],["b","bₙ=aₙ"],["c","bₙ=-aₙ"],["d","bₙ=0 para todo n"]]],
    ["C1-3-P05","mc","Para aₙ=(2/(πn))sen(nπ/2), ¿cuánto vale a₁?","b",[["a","0"],["b","2/π"],["c","1/π"],["d","-2/π"]]],
    ["C1-3-P06","mc","¿Cuánto vale a₂?","a",[["a","0"],["b","1/π"],["c","2/π"],["d","-2/(3π)"]]],
    ["C1-3-P07","mc","¿Cuál es la amplitud del armónico n?","c",[["a","aₙ+bₙ"],["b","aₙ-bₙ"],["c","√(aₙ²+bₙ²)"],["d","atan2(-bₙ,aₙ)"]]],
    ["C1-3-P08","mc","Si b₃=0 y a₃<0, ¿cuál es la fase?","d",[["a","0"],["b","π/2"],["c","-π/2"],["d","π"]]],
    ["C1-3-P09","mc","¿Qué representa a₀/2?","a",[["a","El valor medio o componente continua"],["b","La frecuencia fundamental"],["c","La fase del primer armónico"],["d","El periodo fundamental"]]],
    ["C1-3-P10","tf","La frecuencia angular fundamental cumple ω₀=2π/T₀.",true],
    ["C1-3-P11","tf","En la convención usada, el término constante es a₀/2.",true],
    ["C1-3-P12","tf","Una señal par puede tener coeficientes bₙ distintos de cero.",false],
    ["C1-3-P13","tf","Para el pulso, los armónicos pares tienen aₙ=0.",true],
    ["C1-3-P14","tf","La amplitud Aₙ puede ser negativa.",false],
    ["C1-3-P15","tf","La fase de un armónico con amplitud cero se considera indefinida.",true],
  ];

  function seededRandom(seed) { let value = 2166136261; for (let i = 0; i < seed.length; i += 1) value = Math.imul(value ^ seed.charCodeAt(i), 16777619); return () => { value += 0x6D2B79F5; let out = value; out = Math.imul(out ^ out >>> 15, out | 1); out ^= out + Math.imul(out ^ out >>> 7, out | 61); return ((out ^ out >>> 14) >>> 0) / 4294967296; }; }
  function sample(items, count, random) { const pool = [...items]; for (let i = pool.length - 1; i > 0; i -= 1) { const j = Math.floor(random() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; } return pool.slice(0, count); }
  function selectQuestions(seed) { const random = seededRandom(seed); const selected = [...sample(questionBank.filter((q) => q[1] === "mc"), 3, random), ...sample(questionBank.filter((q) => q[1] === "tf"), 2, random)]; return sample(selected, selected.length, random); }
  function criterionForQuestion(id) { const n = Number(id.slice(-2)); return [1, 2, 9, 10, 11].includes(n) ? "C1_3_CR1" : [3, 4, 5, 6, 12, 13].includes(n) ? "C1_3_CR2" : "C1_3_CR3"; }
  function createState() { const identity = runtime.studentId() || runtime.studentName() || "sesion-local"; return { version: 2, seed: `${identity}-c-1-3`, startedAt: new Date().toISOString(), completedAt: null, stage: 0, answers: {}, attempts: [0, 0, 0, 0], guidedPoints: [0, 0, 0, 0], helpUsed: [false, false, false, false], evaluated: false, points: 0, score: null, feedback: null, feedbackKind: "info" }; }
  let state;
  const save = () => runtime.saveState(state);
  const progress = () => state.evaluated ? 100 : Math.round((state.stage / 5) * 100);
  const heading = (current) => `<div class="progress"><span>Paso ${current} de 5</span><a class="guide-link" href="guia_estudiante_C-1-3.pdf" target="_blank" rel="noopener">Ver guía del estudiante</a><span>${progress()} % completado</span></div><div class="progress-bar"><span style="width:${progress()}%"></span></div>`;
  const feedback = (message, kind) => message ? `<p class="feedback ${kind}">${message}</p>` : "";
  const numericEqual = (actual, expected) => Number.isFinite(actual) && Math.abs(actual - expected) <= 0.001;
  const formatDateTime = (value) => { try { return new Intl.DateTimeFormat("es-CO", { dateStyle: "medium", timeStyle: "medium" }).format(new Date(value)); } catch (_) { return value; } };

  function renderIntro() {
    content.innerHTML = `<section class="card stack"><h2>Actividad guiada</h2><p>Calcula la serie trigonométrica de Fourier de un pulso rectangular e interpreta sus espectros.</p><div class="notice"><strong>Tu avance se guarda en Moodle.</strong> Puedes salir y continuar el mismo intento más tarde.</div><div class="guide-access"><h3>Guía del estudiante C-1-3</h3><p>Consulta la guía antes de comenzar. Permanecerá disponible durante todo el recorrido.</p><a class="button-link secondary" href="guia_estudiante_C-1-3.pdf" target="_blank" rel="noopener">Ver guía del estudiante</a></div><p><strong>Puntaje de los pasos guiados:</strong> cada paso vale 3 puntos si se responde correctamente en el primer intento y 2 puntos si se corrige después.</p><p class="small">La evaluación final selecciona cinco preguntas del banco: tres de selección múltiple y dos de verdadero/falso.</p><div class="actions"><button id="start">Iniciar ejercicio C-1-3</button></div></section>`;
    document.querySelector("#start").addEventListener("click", () => { state.stage = 1; state.feedback = null; save(); render(); });
  }

  function renderGuidedStep(index) {
    const step = guidedSteps[index]; const saved = state.answers[index] || {};
    const fields = (step.fields || []).map(([key, label]) => `<label>${label}<input data-field="${key}" value="${saved[key] ?? ""}" placeholder="Escribe un valor" inputmode="decimal" autocomplete="off"></label>`).join("");
    const options = (step.options || []).map(([key, label, choices]) => `<fieldset><legend>${label}</legend><div class="options">${choices.map(([value, text]) => `<label class="option"><input type="radio" name="${key}" value="${value}" ${saved[key] === value ? "checked" : ""}>${text}</label>`).join("")}</div></fieldset>`).join("");
    const decimalNotice = (step.fields || []).length ? '<p class="notice"><strong>Importante:</strong> utiliza punto (.) como separador decimal. Ejemplo: 1.5</p>' : "";
    content.innerHTML = `<section class="card stack">${heading(index + 1)}<h2>${step.title}</h2><p>${step.prompt}</p><p class="small">Puntaje: 3 puntos al acertar en el primer intento; 2 puntos al corregir después.</p>${decimalNotice}<p class="formula">${step.formula}</p><form id="guided-form"><div class="input-grid">${fields}</div>${options}<div class="actions"><button type="submit">Verificar respuesta</button><button class="secondary" type="button" id="help" ${state.helpUsed[index] ? "disabled" : ""}>Ver orientación</button></div></form>${feedback(state.feedback, state.feedbackKind || "info")}</section>`;
    document.querySelector("#guided-form").addEventListener("submit", (event) => { event.preventDefault(); validateGuidedStep(index); });
    document.querySelector("#help").addEventListener("click", () => { state.helpUsed[index] = true; state.feedback = step.hint; state.feedbackKind = "info"; save(); render(); });
  }

  function validateGuidedStep(index) {
    const step = guidedSteps[index]; const answer = {};
    (step.fields || []).forEach(([key]) => { answer[key] = document.querySelector(`[data-field="${key}"]`).value; });
    (step.options || []).forEach(([key]) => { answer[key] = document.querySelector(`input[name="${key}"]:checked`)?.value || ""; });
    state.answers[index] = answer; state.attempts[index] += 1;
    const correct = Object.entries(step.expected).every(([key, expected]) => typeof expected === "number" ? numericEqual(Number(answer[key]), expected) : answer[key] === expected);
    runtime.recordInteraction({ id: `C1_3_PASO_${index + 1}_${state.attempts[index]}`, type: "fill-in", response: JSON.stringify(answer), correct, weighting: 1 });
    if (correct) { state.guidedPoints[index] = state.attempts[index] === 1 ? 3 : 2; runtime.recordObjective({ id: `C1_3_CR${Math.min(index + 1, 3)}`, score: (state.guidedPoints[index] / 3) * 100, passingScore: OBJECTIVE_PASSING_SCORE }); state.stage += 1; state.feedback = null; state.feedbackKind = null; }
    else { state.feedback = `El resultado todavía no coincide. Intento ${state.attempts[index]} registrado. Revisa el procedimiento y vuelve a intentarlo.`; state.feedbackKind = "error"; }
    save(); runtime.setProgress(progress()); render();
  }

  function renderEvaluation() {
    const questions = selectQuestions(state.seed);
    content.innerHTML = `<section class="card stack">${heading(5)}<h2>Evaluación final</h2><p>Responde las cinco preguntas asignadas. La calificación final se registra en Moodle en la escala de 0 a 100.</p><p class="small"><strong>Distribución:</strong> pasos guiados: hasta 12 puntos; selección múltiple: 6 puntos; verdadero/falso: 2 puntos.</p><form id="evaluation-form" class="stack">${questions.map(([id, type, prompt, expected, options]) => `<fieldset><legend>${id} · ${prompt}</legend><div class="options">${type === "mc" ? options.map(([key, label]) => `<label class="option"><input type="radio" name="${id}" value="${key}">${key.toUpperCase()}. ${label}</label>`).join("") : `<label class="option"><input type="radio" name="${id}" value="true">Verdadero</label><label class="option"><input type="radio" name="${id}" value="false">Falso</label>`}</div></fieldset>`).join("")}<div class="actions"><button type="submit">Calificar y finalizar</button></div></form>${feedback(state.feedback, state.feedbackKind || "info")}</section>`;
    document.querySelector("#evaluation-form").addEventListener("submit", (event) => { event.preventDefault(); gradeEvaluation(questions); });
  }

  function gradeEvaluation(questions) {
    let conceptualPoints = 0; const unanswered = []; const criterionResults = {};
    questions.forEach(([id, type, prompt, expected]) => { const response = document.querySelector(`input[name="${id}"]:checked`)?.value; if (response === undefined) { unanswered.push(id); return; } const normalized = type === "tf" ? response === "true" : response; const correct = normalized === expected; const weighting = type === "mc" ? 2 : 1; runtime.recordInteraction({ id, type: type === "tf" ? "true-false" : "choice", response: normalized, correct, weighting }); const criterion = criterionForQuestion(id); criterionResults[criterion] ||= { correct: 0, total: 0 }; criterionResults[criterion].total += 1; if (correct) { criterionResults[criterion].correct += 1; conceptualPoints += weighting; } });
    if (unanswered.length) { state.feedback = `Responde todas las preguntas antes de calificar: ${unanswered.join(", ")}.`; state.feedbackKind = "error"; render(); return; }
    state.evaluated = true; state.points = state.guidedPoints.reduce((total, value) => total + value, 0) + conceptualPoints; state.score = Math.round((state.points / 20) * 100); state.completedAt = new Date().toISOString(); state.feedback = null; runtime.setProgress(100); Object.entries(criterionResults).forEach(([id, result]) => runtime.recordObjective({ id, score: (result.correct / result.total) * 100, passingScore: OBJECTIVE_PASSING_SCORE })); runtime.reportScore({ score: state.score, passingScore: PASSING_SCORE, completed: true }); save(); render();
  }

  function renderResult() {
    const status = state.score >= PASSING_SCORE ? "Actividad aprobada" : "Actividad finalizada";
    content.innerHTML = `<section class="card stack"><p class="eyebrow">Resultado registrado</p><h2>${status}</h2><p class="score">${state.score.toFixed(2).replace(".", ",")} / 100</p><p>${state.points} / 20 puntos</p><p>Finalización registrada: <strong>${formatDateTime(state.completedAt || new Date().toISOString())}</strong>.</p><p>La actividad envió a Moodle la nota, el estado de finalización, el avance, las interacciones y los resultados por criterio.</p><div class="notice">El docente consulta el resultado y la fecha/hora oficial del intento directamente desde Moodle. No necesitas descargar ni entregar un archivo adicional.</div><div class="actions"><button id="finish">Finalizar y salir</button></div><p id="finish-status" class="small" aria-live="polite"></p></section>`;
    document.querySelector("#finish").addEventListener("click", () => { const button = document.querySelector("#finish"); const finishStatus = document.querySelector("#finish-status"); button.disabled = true; button.textContent = "Guardando y saliendo…"; save(); runtime.commit(); const finished = runtime.finish(); finishStatus.textContent = finished ? "Sesión finalizada. Regresando a Moodle…" : "Moodle no confirmó el cierre, pero el estado ya fue guardado. Regresando…"; setTimeout(() => { if (!leaveScormPlayer()) { button.textContent = "Sesión finalizada"; finishStatus.textContent = "La sesión quedó guardada. Usa el control de salida del reproductor de Moodle para volver al curso."; } }, 150); });
  }

  function moodleReturnUrl() { const candidates = []; let frame = window; for (let depth = 0; depth < 10; depth += 1) { try { candidates.push(frame.document.referrer, frame.location.href); if (frame === frame.parent) break; frame = frame.parent; } catch (_) { break; } } for (const value of candidates) { if (!value) continue; try { const url = new URL(value, window.location.href); if (url.origin !== window.location.origin) continue; if (url.pathname.includes("/mod/scorm/view.php") || url.pathname.includes("/course/view.php")) return url.href; if (url.pathname.includes("/mod/scorm/player.php")) { const courseModule = url.searchParams.get("cm") || url.searchParams.get("cmid"); if (courseModule) return new URL(`/mod/scorm/view.php?id=${encodeURIComponent(courseModule)}`, url.origin).href; } } catch (_) { continue; } } return ""; }
  function leaveScormPlayer() { const target = moodleReturnUrl(); try { if (target) { window.top.location.assign(target); return true; } if (window.top.history.length > 1) { window.top.history.back(); return true; } } catch (_) { if (window.history.length > 1) { window.history.back(); return true; } } return false; }
  function render() { nameNode.textContent = runtime.studentName() ? `Estudiante: ${runtime.studentName()}` : "Modo de prueba local"; if (state.evaluated) renderResult(); else if (state.stage === 0) renderIntro(); else if (state.stage <= 4) renderGuidedStep(state.stage - 1); else renderEvaluation(); }

  runtime.initialize(); state = runtime.restoreState() || createState();
  if (!Array.isArray(state.guidedPoints)) { state.guidedPoints = [0, 0, 0, 0]; for (let index = 0; index < 4; index += 1) if (state.stage > index + 1 && state.attempts?.[index] > 0) state.guidedPoints[index] = state.attempts[index] === 1 ? 3 : 2; }
  if (!Number.isFinite(state.points)) state.points = 0;
  if (!Array.isArray(state.helpUsed)) state.helpUsed = state.help || [false, false, false, false];
  render();
})();
