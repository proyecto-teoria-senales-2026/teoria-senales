(() => {
  "use strict";

  const PASSING_SCORE = 60;
  const OBJECTIVE_PASSING_SCORE = 60;
  const content = document.querySelector("#application-content");
  const nameNode = document.querySelector("#student-name");
  const runtime = window.TeoriaSenalesScorm12;

  const guidedSteps = [
    {
      title: "Reconoce impulso, escalón y rampa",
      prompt: "Lee las expresiones y completa los valores solicitados.",
      formula: "δ[0] = 1; &nbsp; u[-1] = 0; &nbsp; r[n] = n·u[n]",
      fields: [["impulse", "δ[0]"], ["step", "u[-1]"], ["ramp", "r[3]"]],
      expected: { impulse: 1, step: 0, ramp: 3 },
      hint: "Ubica primero n = 0. El impulso solo vale 1 allí; el escalón es cero para n < 0 y la rampa r[n] vale n para n ≥ 0.",
      criterion: "C1_1_CR1",
    },
    {
      title: "Calcula el efecto de la amplitud",
      prompt: "Evalúa las señales en el índice indicado. El factor que multiplica la señal modifica su amplitud.",
      formula: "3δ[0]; &nbsp; 2u[4]; &nbsp; r[3]",
      fields: [["impulse", "3δ[0]"], ["step", "2u[4]"], ["ramp", "r[3]"]],
      expected: { impulse: 3, step: 2, ramp: 3 },
      hint: "Primero calcula el valor de la señal básica y luego aplica el factor de amplitud.",
      criterion: "C1_1_CR2",
    },
    {
      title: "Interpreta la señal exponencial",
      prompt: "Para x[n] = (1/2)ⁿu[n], calcula dos muestras e identifica su comportamiento.",
      formula: "x[n] = (1/2)ⁿu[n]",
      fields: [["x0", "x[0]"], ["x2", "x[2]"]],
      expected: { x0: 1, x2: 0.25, behavior: "decrease" },
      options: [["decrease", "Disminuye hacia cero"], ["constant", "Permanece constante"], ["growth", "Crece sin límite"]],
      hint: "Evalúa la potencia para n = 0 y n = 2. La base 1/2 está entre cero y uno.",
      criterion: "C1_1_CR2",
    },
    {
      title: "Halla el periodo y las muestras senoidales",
      prompt: "Para x[n] = sin((π/2)n), indica el periodo fundamental y las primeras cinco muestras.",
      formula: "ω₀N₀ = 2πk; &nbsp; x[n] = sin((π/2)n)",
      fields: [["period", "Periodo N₀"], ["samples", "x[0], x[1], x[2], x[3], x[4]"]],
      expected: { period: 4, samples: [0, 1, 0, -1, 0] },
      hint: "Busca el menor entero positivo N₀ que cumpla (π/2)N₀ = 2π. Separa las cinco muestras con comas.",
      criterion: "C1_1_CR3",
    },
  ];

  const questionBank = [
    ["C1-1-P01", "mc", "¿En qué índice vale 1 el impulso unitario δ[n]?", "b", [["a", "n = -1"], ["b", "n = 0"], ["c", "n = 1"], ["d", "En todos los índices"]]],
    ["C1-1-P02", "mc", "¿Cuál es el valor del escalón unitario u[n] para n < 0?", "a", [["a", "0"], ["b", "1"], ["c", "n"], ["d", "-1"]]],
    ["C1-1-P03", "mc", "¿Qué expresión representa la rampa unitaria discreta?", "c", [["a", "δ[n]"], ["b", "u[n - 1]"], ["c", "n·u[n]"], ["d", "cos(n)"]]],
    ["C1-1-P04", "mc", "Si x[n] = 3δ[n], ¿cuál es x[0]?", "d", [["a", "0"], ["b", "1"], ["c", "2"], ["d", "3"]]],
    ["C1-1-P05", "mc", "Si x[n] = 2u[n], ¿cuál es x[4]?", "c", [["a", "0"], ["b", "1"], ["c", "2"], ["d", "4"]]],
    ["C1-1-P06", "mc", "Si x[n] = r[n], ¿cuál es x[3]?", "d", [["a", "0"], ["b", "1"], ["c", "2"], ["d", "3"]]],
    ["C1-1-P07", "mc", "¿Cuál es el periodo de x[n] = sin((π/2)n)?", "b", [["a", "2 muestras"], ["b", "4 muestras"], ["c", "π muestras"], ["d", "No es periódica"]]],
    ["C1-1-P08", "mc", "¿Qué parámetro controla el valor máximo de una señal senoidal?", "a", [["a", "La amplitud"], ["b", "El índice inicial"], ["c", "La duración del archivo"], ["d", "El nombre de la señal"]]],
    ["C1-1-P09", "mc", "¿Qué sucede con x[n] = (1/2)ⁿu[n] cuando n aumenta desde n = 0?", "c", [["a", "Crece sin límite"], ["b", "Permanece constante"], ["c", "Disminuye hacia cero"], ["d", "Alterna entre 1 y -1"]]],
    ["C1-1-P10", "tf", "El impulso unitario δ[n] vale cero para todo n distinto de cero.", true],
    ["C1-1-P11", "tf", "El escalón unitario u[n] vale cero en n = 0.", false],
    ["C1-1-P12", "tf", "La rampa unitaria r[n] es cero para n < 0.", true],
    ["C1-1-P13", "tf", "Multiplicar una señal por 2 duplica su amplitud.", true],
    ["C1-1-P14", "tf", "Toda señal senoidal de tiempo discreto es periódica para cualquier frecuencia angular.", false],
    ["C1-1-P15", "tf", "El impulso unitario δ[n] tiene duración finita porque solo es distinto de cero en n = 0.", true],
  ];

  function seededRandom(seed) {
    let value = 2166136261;
    for (let index = 0; index < seed.length; index += 1) value = Math.imul(value ^ seed.charCodeAt(index), 16777619);
    return () => {
      value += 0x6D2B79F5;
      let output = value;
      output = Math.imul(output ^ output >>> 15, output | 1);
      output ^= output + Math.imul(output ^ output >>> 7, output | 61);
      return ((output ^ output >>> 14) >>> 0) / 4294967296;
    };
  }

  function sample(items, count, random) {
    const pool = [...items];
    for (let index = pool.length - 1; index > 0; index -= 1) {
      const replacement = Math.floor(random() * (index + 1));
      [pool[index], pool[replacement]] = [pool[replacement], pool[index]];
    }
    return pool.slice(0, count);
  }

  function selectQuestions(seed) {
    const random = seededRandom(seed);
    const selected = [...sample(questionBank.filter((question) => question[1] === "mc"), 3, random), ...sample(questionBank.filter((question) => question[1] === "tf"), 2, random)];
    return sample(selected, selected.length, random);
  }

  function createState() {
    const identity = runtime.studentId() || runtime.studentName() || "sesion-local";
    return { version: 2, seed: `${identity}-c1-1`, startedAt: new Date().toISOString(), completedAt: null, stage: 0, answers: {}, attempts: [0, 0, 0, 0], guidedPoints: [0, 0, 0, 0], helpUsed: [false, false, false, false], evaluated: false, points: 0, score: null, feedback: null };
  }

  let state;
  function save() { runtime.saveState(state); }
  function progress() { return state.evaluated ? 100 : Math.round((state.stage / 5) * 100); }
  function heading(current) { return `<div class="progress"><span>Paso ${current} de 5</span><span>${progress()} % completado</span></div><div class="progress-bar"><span style="width:${progress()}%"></span></div>`; }
  function feedback(message, kind) { return message ? `<p class="feedback ${kind}">${message}</p>` : ""; }
  function numericEqual(actual, expected) { return Number.isFinite(actual) && Math.abs(actual - expected) <= 0.000001; }
  function parseSequence(value) { const values = String(value || "").trim().split(/[;,\s]+/).filter(Boolean).map(Number); return values.length === 5 && values.every(Number.isFinite) ? values : null; }
  function formatDateTime(value) { return new Intl.DateTimeFormat("es-CO", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value)); }
  function criterionForQuestion(questionId) {
    const number = Number(questionId.slice(-2));
    if ([1, 2, 3, 10, 11, 15].includes(number)) return "C1_1_CR1";
    if ([4, 5, 6, 9, 12, 13].includes(number)) return "C1_1_CR2";
    return "C1_1_CR3";
  }

  function renderIntro() {
    content.innerHTML = `<section class="card stack"><h2>Actividad guiada</h2><p>Reconoce y representa impulso, escalón, rampa, exponencial y senoidal mediante cuatro pasos guiados y una evaluación final.</p><div class="notice"><strong>Tu avance se guarda en Moodle.</strong> Puedes salir y continuar el mismo intento más tarde.</div><p><strong>Puntaje de los pasos guiados:</strong> cada paso vale 3 puntos si se responde correctamente en el primer intento y 2 puntos si se corrige después.</p><p class="small">La evaluación final selecciona cinco preguntas del banco: tres de selección múltiple y dos de verdadero/falso.</p><div class="actions"><button id="start">Iniciar ejercicio C-1-1</button></div></section>`;
    document.querySelector("#start").addEventListener("click", () => { state.stage = 1; state.feedback = null; save(); render(); });
  }

  function renderGuidedStep(index) {
    const step = guidedSteps[index];
    const saved = state.answers[index] || {};
    const fields = step.fields.map(([key, label]) => `<label>${label}<input data-field="${key}" value="${saved[key] ?? ""}" placeholder="${key === "samples" ? "Escribe los valores separados por comas" : "Escribe un valor"}" inputmode="decimal" autocomplete="off"></label>`).join("");
    const options = step.options ? `<fieldset><legend>Cuando n aumenta, la señal:</legend><div class="options">${step.options.map(([key, label]) => `<label class="option"><input type="radio" name="behavior" value="${key}" ${saved.behavior === key ? "checked" : ""}>${label}</label>`).join("")}</div></fieldset>` : "";
    content.innerHTML = `<section class="card stack">${heading(index + 1)}<h2>${step.title}</h2><p>${step.prompt}</p><p class="small">Puntaje: 3 puntos al acertar en el primer intento; 2 puntos al corregir después.</p><p class="formula">${step.formula}</p><form id="guided-form"><div class="input-grid">${fields}</div>${options}<div class="actions"><button type="submit">Verificar respuesta</button><button class="secondary" type="button" id="help" ${state.helpUsed[index] ? "disabled" : ""}>Ver orientación</button></div></form>${feedback(state.feedback, state.feedbackKind || "info")}</section>`;
    document.querySelector("#guided-form").addEventListener("submit", (event) => { event.preventDefault(); validateGuidedStep(index); });
    document.querySelector("#help").addEventListener("click", () => { state.helpUsed[index] = true; state.feedback = step.hint; state.feedbackKind = "info"; save(); render(); });
  }

  function validateGuidedStep(index) {
    const step = guidedSteps[index];
    const answer = {};
    step.fields.forEach(([key]) => { answer[key] = document.querySelector(`[data-field="${key}"]`).value; });
    if (step.options) answer.behavior = document.querySelector("input[name=behavior]:checked")?.value || "";
    state.answers[index] = answer;
    let correct;
    if (index === 3) {
      const samples = parseSequence(answer.samples);
      correct = numericEqual(Number(answer.period), step.expected.period) && samples && samples.every((value, position) => numericEqual(value, step.expected.samples[position]));
    } else {
      correct = Object.entries(step.expected).every(([key, expected]) => key === "behavior" ? answer[key] === expected : numericEqual(Number(answer[key]), expected));
    }
    state.attempts[index] += 1;
    const interactionResponse = step.fields.map(([key]) => answer[key]).join(" | ");
    runtime.recordInteraction({ id: `C1-1-G0${index + 1}-${state.attempts[index]}`, type: "fill-in", response: interactionResponse, correct, weighting: 3 });
    if (correct) {
      state.guidedPoints[index] = state.attempts[index] === 1 ? 3 : 2;
      runtime.recordObjective({ id: step.criterion, score: (state.guidedPoints[index] / 3) * 100, passingScore: OBJECTIVE_PASSING_SCORE });
      state.stage += 1;
      state.feedback = null;
      state.feedbackKind = null;
    } else {
      runtime.recordObjective({ id: step.criterion, score: 0, passingScore: OBJECTIVE_PASSING_SCORE });
      state.feedback = `El resultado todavía no coincide. Intento ${state.attempts[index]} registrado. Revisa el procedimiento y vuelve a intentarlo.`;
      state.feedbackKind = "error";
    }
    save(); runtime.setProgress(progress()); render();
  }

  function renderEvaluation() {
    const questions = selectQuestions(state.seed);
    content.innerHTML = `<section class="card stack">${heading(5)}<h2>Evaluación final</h2><p>Responde las cinco preguntas asignadas. La calificación final se registra en Moodle en la escala de 0 a 100.</p><p class="small"><strong>Distribución:</strong> pasos guiados: hasta 12 puntos; selección múltiple: 6 puntos; verdadero/falso: 2 puntos.</p><form id="evaluation-form" class="stack">${questions.map(([id, type, prompt, expected, options]) => `<fieldset><legend>${id} · ${prompt}</legend><div class="options">${type === "mc" ? options.map(([key, label]) => `<label class="option"><input type="radio" name="${id}" value="${key}">${key.toUpperCase()}. ${label}</label>`).join("") : `<label class="option"><input type="radio" name="${id}" value="true">Verdadero</label><label class="option"><input type="radio" name="${id}" value="false">Falso</label>`}</div></fieldset>`).join("")}<div class="actions"><button type="submit">Calificar y finalizar</button></div></form>${feedback(state.feedback, state.feedbackKind || "info")}</section>`;
    document.querySelector("#evaluation-form").addEventListener("submit", (event) => { event.preventDefault(); gradeEvaluation(questions); });
  }

  function gradeEvaluation(questions) {
    let conceptualPoints = 0;
    const unanswered = [];
    const submitted = questions.map(([id, type, prompt, expected]) => {
      const response = document.querySelector(`input[name="${id}"]:checked`)?.value;
      if (response === undefined) unanswered.push(id);
      return { id, type, expected, response };
    });
    if (unanswered.length) {
      state.feedback = `Responde todas las preguntas antes de calificar: ${unanswered.join(", ")}.`;
      state.feedbackKind = "error";
      render();
      return;
    }
    const criterionResults = {};
    submitted.forEach(({ id, type, expected, response }) => {
      const normalized = type === "tf" ? response === "true" : response;
      const correct = normalized === expected;
      const weighting = type === "tf" ? 1 : 2;
      runtime.recordInteraction({ id, type: type === "tf" ? "true-false" : "choice", response: normalized, correct, weighting });
      const criterion = criterionForQuestion(id);
      criterionResults[criterion] ||= { correct: 0, total: 0 };
      criterionResults[criterion].total += 1;
      if (correct) criterionResults[criterion].correct += 1;
      if (correct) conceptualPoints += weighting;
    });
    state.evaluated = true;
    state.points = state.guidedPoints.reduce((total, value) => total + value, 0) + conceptualPoints;
    state.score = Math.round((state.points / 20) * 100);
    state.completedAt = new Date().toISOString();
    state.feedback = null;
    runtime.setProgress(100);
    Object.entries(criterionResults).forEach(([id, result]) => {
      runtime.recordObjective({ id, score: (result.correct / result.total) * 100, passingScore: OBJECTIVE_PASSING_SCORE });
    });
    runtime.reportScore({ score: state.score, passingScore: PASSING_SCORE, completed: true });
    save();
    render();
  }

  function renderResult() {
    const status = state.score >= PASSING_SCORE ? "Actividad aprobada" : "Actividad finalizada";
    content.innerHTML = `<section class="card stack"><p class="eyebrow">Resultado registrado</p><h2>${status}</h2><p class="score">${state.score.toFixed(2).replace(".", ",")} / 100</p><p>${state.points} / 20 puntos</p><p>Finalización registrada: <strong>${formatDateTime(state.completedAt || new Date().toISOString())}</strong>.</p><p>La actividad envió a Moodle la nota, el estado de finalización, el avance, las interacciones y los resultados por criterio.</p><div class="notice">El docente consulta el resultado y la fecha/hora oficial del intento directamente desde Moodle. No necesitas descargar ni entregar un archivo adicional.</div><div class="actions"><button id="finish">Finalizar y salir</button></div><p id="finish-status" class="small" aria-live="polite"></p></section>`;
    document.querySelector("#finish").addEventListener("click", () => {
      const button = document.querySelector("#finish");
      const finishStatus = document.querySelector("#finish-status");
      button.disabled = true;
      button.textContent = "Guardando y saliendo…";
      save();
      runtime.commit();
      const finished = runtime.finish();
      finishStatus.textContent = finished ? "Sesión finalizada. Regresando a Moodle…" : "Moodle no confirmó el cierre, pero el estado ya fue guardado. Regresando…";
      setTimeout(() => {
        if (!leaveScormPlayer()) {
          button.textContent = "Sesión finalizada";
          finishStatus.textContent = "La sesión quedó guardada. Usa el control de salida del reproductor de Moodle para volver al curso.";
        }
      }, 150);
    });
  }

  function moodleReturnUrl() {
    const candidates = [];
    let frame = window;
    for (let depth = 0; depth < 10; depth += 1) {
      try {
        candidates.push(frame.document.referrer, frame.location.href);
        if (frame === frame.parent) break;
        frame = frame.parent;
      } catch (_) {
        break;
      }
    }
    for (const value of candidates) {
      if (!value) continue;
      try {
        const url = new URL(value, window.location.href);
        if (url.origin !== window.location.origin) continue;
        if (url.pathname.includes("/mod/scorm/view.php") || url.pathname.includes("/course/view.php")) return url.href;
        if (url.pathname.includes("/mod/scorm/player.php")) {
          const courseModule = url.searchParams.get("cm") || url.searchParams.get("cmid");
          if (courseModule) return new URL(`/mod/scorm/view.php?id=${encodeURIComponent(courseModule)}`, url.origin).href;
        }
      } catch (_) {
        continue;
      }
    }
    return "";
  }

  function leaveScormPlayer() {
    const target = moodleReturnUrl();
    try {
      if (target) { window.top.location.assign(target); return true; }
      if (window.top.history.length > 1) { window.top.history.back(); return true; }
    } catch (_) {
      if (window.history.length > 1) { window.history.back(); return true; }
    }
    return false;
  }

  function render() {
    nameNode.textContent = runtime.studentName() ? `Estudiante: ${runtime.studentName()}` : "Modo de prueba local";
    if (state.evaluated) renderResult();
    else if (state.stage === 0) renderIntro();
    else if (state.stage <= 4) renderGuidedStep(state.stage - 1);
    else renderEvaluation();
  }

  runtime.initialize();
  state = runtime.restoreState() || createState();
  if (!Array.isArray(state.guidedPoints)) {
    state.guidedPoints = [0, 0, 0, 0];
    for (let index = 0; index < 4; index += 1) {
      if (state.stage > index + 1 && state.attempts?.[index] > 0) state.guidedPoints[index] = state.attempts[index] === 1 ? 3 : 2;
    }
  }
  if (!Number.isFinite(state.points)) state.points = 0;
  render();
})();
