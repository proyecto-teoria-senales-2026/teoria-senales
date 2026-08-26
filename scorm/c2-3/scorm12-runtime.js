/*
 * Runtime común SCORM 1.2 para las actividades de Teoría de Señales.
 * No depende de bibliotecas externas y puede ejecutarse localmente sin LMS.
 */
(function attachTeoriaSenalesScormRuntime(global) {
  "use strict";

  const MAX_API_DEPTH = 10;
  const MAX_SUSPEND_DATA_CHARS = 3800;
  let api = null;
  let initialized = false;
  let startedAt = null;

  function findApiInWindow(targetWindow) {
    let current = targetWindow;
    for (let depth = 0; current && depth < MAX_API_DEPTH; depth += 1) {
      try {
        if (current.API) return current.API;
        if (current.parent && current.parent !== current) {
          current = current.parent;
        } else {
          break;
        }
      } catch (_) {
        break;
      }
    }
    return null;
  }

  function findApi() {
    return findApiInWindow(global) || findApiInWindow(global.opener);
  }

  function call(method, ...args) {
    if (!api || typeof api[method] !== "function") return "false";
    return api[method](...args);
  }

  function getLastError() {
    if (!api) return "API no disponible";
    const code = call("LMSGetLastError");
    if (code === "0") return "";
    return `${code}: ${call("LMSGetErrorString", code)} — ${call("LMSGetDiagnostic", code)}`;
  }

  function setValue(element, value) {
    if (!initialized) return false;
    const ok = call("LMSSetValue", element, String(value)) === "true";
    if (!ok) console.warn(`No fue posible guardar ${element}.`, getLastError());
    return ok;
  }

  function getValue(element) {
    if (!initialized) return "";
    return call("LMSGetValue", element);
  }

  function commit() {
    if (!initialized) return false;
    const ok = call("LMSCommit", "") === "true";
    if (!ok) console.warn("No fue posible sincronizar con Moodle.", getLastError());
    return ok;
  }

  function formatSessionTime(milliseconds) {
    const totalSeconds = Math.max(0, Math.floor(milliseconds / 1000));
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    const pad = (number) => String(number).padStart(2, "0");
    return `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
  }

  function initialize() {
    if (initialized) return true;
    api = findApi();
    if (!api) {
      console.info("Actividad abierta sin LMS SCORM: el avance no se sincronizará.");
      return false;
    }
    initialized = call("LMSInitialize", "") === "true";
    if (!initialized) {
      console.warn("No fue posible inicializar SCORM.", getLastError());
      return false;
    }
    startedAt = Date.now();
    const status = getValue("cmi.core.lesson_status");
    if (!status || status === "not attempted") {
      setValue("cmi.core.lesson_status", "incomplete");
      commit();
    }
    return true;
  }

  function studentName() {
    return initialized ? getValue("cmi.core.student_name") : "";
  }

  function studentId() {
    return initialized ? getValue("cmi.core.student_id") : "";
  }

  function restoreState() {
    const serialized = getValue("cmi.suspend_data");
    if (!serialized) return null;
    try {
      return JSON.parse(serialized);
    } catch (_) {
      console.warn("El avance almacenado no tiene un formato válido.");
      return null;
    }
  }

  function saveState(state) {
    if (!initialized) return false;
    const serialized = JSON.stringify(state);
    if (serialized.length > MAX_SUSPEND_DATA_CHARS) {
      console.warn("El avance supera el límite seguro de SCORM 1.2 y no se guardará.");
      return false;
    }
    return setValue("cmi.suspend_data", serialized) && commit();
  }

  function setProgress(progress) {
    if (!initialized) return false;
    const bounded = Math.max(0, Math.min(100, Math.round(progress)));
    return setValue("cmi.core.lesson_location", String(bounded));
  }

  function recordInteraction(interaction) {
    if (!initialized) return false;
    const index = getValue("cmi.interactions._count") || "0";
    const prefix = `cmi.interactions.${index}`;
    const type = interaction.type === "true-false"
      ? "true-false"
      : (interaction.type === "numeric" || interaction.type === "fill-in")
        ? "fill-in"
        : "choice";
    const response = interaction.type === "true-false"
      ? (interaction.response ? "true" : "false")
      : String(interaction.response);
    const result = interaction.correct ? "correct" : "wrong";
    return [
      setValue(`${prefix}.id`, interaction.id),
      setValue(`${prefix}.type`, type),
      setValue(`${prefix}.student_response`, response),
      setValue(`${prefix}.result`, result),
      setValue(`${prefix}.weighting`, interaction.weighting || 1),
    ].every(Boolean);
  }

  function recordObjective({ id, score, passingScore = 60 }) {
    if (!initialized) return false;
    const index = getValue("cmi.objectives._count") || "0";
    const prefix = `cmi.objectives.${index}`;
    const raw = Math.max(0, Math.min(100, Math.round(score * 100) / 100));
    const status = raw >= passingScore ? "passed" : "failed";
    return [
      setValue(`${prefix}.id`, id),
      setValue(`${prefix}.score.min`, "0"),
      setValue(`${prefix}.score.max`, "100"),
      setValue(`${prefix}.score.raw`, raw),
      setValue(`${prefix}.status`, status),
    ].every(Boolean);
  }

  function reportScore({ score, passingScore = 3, maxScore = 5, completed = true }) {
    if (!initialized) return false;
    const raw = Math.max(0, Math.min(maxScore, Math.round(score * 100) / 100));
    const status = completed ? (raw >= passingScore ? "passed" : "failed") : "incomplete";
    const results = [
      setValue("cmi.core.score.min", "0"),
      setValue("cmi.core.score.max", String(maxScore)),
      setValue("cmi.core.score.raw", raw),
      setValue("cmi.core.lesson_status", status),
    ];
    return results.every(Boolean) && commit();
  }

  function finish() {
    if (!initialized) return true;
    if (startedAt) setValue("cmi.core.session_time", formatSessionTime(Date.now() - startedAt));
    commit();
    const ok = call("LMSFinish", "") === "true";
    initialized = false;
    api = null;
    return ok;
  }

  global.TeoriaSenalesScorm12 = Object.freeze({
    initialize,
    isConnected: () => initialized,
    studentName,
    studentId,
    restoreState,
    saveState,
    setProgress,
    recordInteraction,
    recordObjective,
    reportScore,
    commit,
    finish,
  });

  global.addEventListener("pagehide", finish, { once: true });
})(window);
