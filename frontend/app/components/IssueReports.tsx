"use client";

import { useEffect, useRef, useState } from "react";
import { clearIssueReports, exportIssueReports, getIssueReports, saveIssueReport, type IssueReport, type IssueReportSection, type ReportScreenshot } from "../lib/api";
import { captureReportLocation, describeReportLocation, type ReportLocation } from "../lib/reportLocation";

const labels: Record<IssueReportSection, string> = { learning: "Обучение", cheats: "Шпаргалки", exercises: "Упражнения", homework: "Домашнее задание", reading: "Чтение", review: "Ошибки", vocabulary: "Слова" };

export function IssueReports({ section }: { section: IssueReportSection }) {
  const dialog = useRef<HTMLDialogElement>(null);
  const [open, setOpen] = useState(false);
  const [area, setArea] = useState(section);
  const [location, setLocation] = useState<ReportLocation>({});
  const [description, setDescription] = useState("");
  const [screenshots, setScreenshots] = useState<ReportScreenshot[]>([]);
  const [readingFiles, setReadingFiles] = useState(false);
  const [reports, setReports] = useState<IssueReport[]>([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  useEffect(() => {
    if (!open) return;
    let cancelled = false;
    setLoading(true); setError("");
    void getIssueReports().then((items) => { if (!cancelled) setReports(items); }).catch((cause) => { if (!cancelled) setError(cause instanceof Error ? cause.message : "Не удалось загрузить обращения."); }).finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [open]);
  const show = () => { if (!description.trim() && !screenshots.length && !readingFiles) { setArea(section); setLocation(captureReportLocation(section)); } setMessage(""); setOpen(true); dialog.current?.showModal(); };
  const download = async () => {
    setError(""); setSaving(true);
    try {
      const result = await exportIssueReports();
      const bytes = Uint8Array.from(atob(result.data), (character) => character.charCodeAt(0));
      const url = URL.createObjectURL(new Blob([bytes], { type: "application/zip" }));
      const anchor = document.createElement("a"); anchor.href = url; anchor.download = "SlovoKrok_обращения.zip"; document.body.appendChild(anchor); anchor.click(); anchor.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      setMessage("Файл скачан. Отправьте его владельцу курса удобным способом.");
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось скачать обращения."); }
    finally { setSaving(false); }
  };
  const attach = async (files: File[]) => {
    if (saving || readingFiles) return;
    setError(""); setReadingFiles(true);
    try {
      if (screenshots.length + files.length > 3) throw new Error("Можно приложить до 3 скриншотов.");
      const images: ReportScreenshot[] = [];
      for (const file of files) {
        if (!["image/png", "image/jpeg", "image/webp"].includes(file.type) || file.size > 2 * 1024 * 1024) throw new Error("Выберите PNG, JPEG или WebP до 2 МБ каждый.");
        const data = await new Promise<string>((resolve, reject) => {
          const reader = new FileReader(); reader.onload = () => resolve(String(reader.result).split(",")[1]); reader.onerror = () => reject(new Error("Не удалось прочитать скриншот.")); reader.readAsDataURL(file);
        });
        images.push({ name: file.name.slice(0, 255), mime: file.type as ReportScreenshot["mime"], data });
      }
      setScreenshots((current) => [...current, ...images]);
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось прикрепить скриншот."); }
    finally { setReadingFiles(false); }
  };
  const clear = async () => {
    if (!window.confirm("Удалить все сохранённые обращения и их скриншоты? Сначала скачайте архив, если хотите их сохранить.")) return;
    setSaving(true); setError(""); setMessage("");
    try { await clearIssueReports(); setReports([]); setMessage("Список обращений очищен."); }
    catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось очистить обращения."); }
    finally { setSaving(false); }
  };
  const captureScreen = async () => {
    if (saving || readingFiles || screenshots.length >= 3) return;
    if (!navigator.mediaDevices?.getDisplayMedia) { setError("Этот браузер не поддерживает снимок экрана. Откройте приложение в Chrome или Edge."); return; }
    setReadingFiles(true); setError(""); setMessage("");
    let stream: MediaStream | undefined;
    let frameTimeout: ReturnType<typeof setTimeout> | undefined;
    const panel = dialog.current;
    const video = document.createElement("video");
    try {
      // Hide the report form so the captured application remains visible.
      if (panel) { panel.style.visibility = "hidden"; panel.classList.add("course-report-capturing"); }
      stream = await navigator.mediaDevices.getDisplayMedia({ video: true, audio: false });
      video.srcObject = stream; video.muted = true;
      await Promise.race([
        (async () => { await video.play(); if (typeof video.requestVideoFrameCallback === "function") await new Promise<void>((resolve) => video.requestVideoFrameCallback(() => resolve())); })(),
        new Promise<never>((_, reject) => { frameTimeout = setTimeout(() => reject(new Error("Не удалось получить изображение экрана. Попробуйте ещё раз.")), 10000); }),
      ]);
      if (!video.videoWidth || !video.videoHeight) throw new Error("Не удалось получить изображение экрана.");
      const canvas = document.createElement("canvas");
      const scale = Math.min(1, 1920 / video.videoWidth, 1080 / video.videoHeight);
      canvas.width = Math.round(video.videoWidth * scale); canvas.height = Math.round(video.videoHeight * scale);
      const context = canvas.getContext("2d");
      if (!context) throw new Error("Не удалось создать снимок экрана.");
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      let mime: ReportScreenshot["mime"] = "image/png";
      let data = canvas.toDataURL(mime).split(",")[1];
      if (data.length > 2796200) { mime = "image/jpeg"; data = canvas.toDataURL(mime, 0.85).split(",")[1]; }
      if (data.length > 2796200) throw new Error("Снимок слишком большой. Выберите окно приложения вместо всего экрана.");
      setScreenshots((current) => [...current, { name: `SlovoKrok_${Date.now()}.${mime === "image/png" ? "png" : "jpg"}`, mime, data }]);
      setMessage("Снимок прикреплён. Проверьте его перед сохранением обращения.");
    } catch (cause) {
      if (cause instanceof DOMException && cause.name === "NotAllowedError") setMessage("Снимок отменён или доступ к экрану не разрешён.");
      else setError(cause instanceof Error ? cause.message : "Не удалось сделать снимок экрана.");
    } finally {
      stream?.getTracks().forEach((track) => track.stop());
      if (frameTimeout) clearTimeout(frameTimeout);
      video.pause(); video.srcObject = null;
      if (panel) { panel.style.visibility = ""; panel.classList.remove("course-report-capturing"); }
      setReadingFiles(false);
    }
  };
  return <>
    <button type="button" onClick={show} aria-label="Сообщить об ошибке" title="Сообщить об ошибке"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9h.5a8.5 8.5 0 0 1 8 8v.5Z" /><path d="M12 7v5" /><circle cx="12" cy="15.5" r=".5" fill="currentColor" stroke="none" /></svg></button>
    <dialog ref={dialog} className="course-report-dialog" aria-labelledby="issue-report-title" onClose={() => setOpen(false)} onCancel={(event) => { if (saving || readingFiles) event.preventDefault(); }}>
      <div className="course-section-heading"><h3 id="issue-report-title">Сообщить об ошибке</h3><button type="button" disabled={saving || readingFiles} onClick={() => dialog.current?.close()} aria-label="Закрыть обращения">Закрыть</button></div>
      <p>Опишите, что произошло и что вы ожидали. Обращение сохранится на этом компьютере. Чтобы передать его владельцу, скачайте файл и отправьте вручную.</p>
      <form onSubmit={async (event) => {
        event.preventDefault(); if (saving || loading || readingFiles || description.trim().length < 5) return;
        setSaving(true); setMessage(""); setError("");
        try { const report = await saveIssueReport(area, description.trim(), location, screenshots); setReports((current) => [report, ...current.filter((item) => item.id !== report.id)]); setDescription(""); setScreenshots([]); setMessage("Обращение сохранено. Оно ещё не отправлено владельцу."); }
        catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось сохранить обращение."); }
        finally { setSaving(false); }
      }}>
        <div><strong>Место определено автоматически: {labels[area]}</strong><p style={{ whiteSpace: "pre-wrap" }}>{describeReportLocation(location)}</p></div>
        <label>Описание проблемы<textarea rows={5} maxLength={4000} value={description} disabled={saving} onChange={(event) => setDescription(event.target.value)} placeholder="Например: в упражнении выбрал правильный ответ, но проверка показала ошибку…" /></label>
        <div><strong>Скриншоты · {screenshots.length}/3</strong><button type="button" disabled={saving || readingFiles || screenshots.length >= 3} onClick={() => void captureScreen()}>{readingFiles ? "Готовлю снимок…" : "Снимок экрана"}</button></div>
        <small>Выберите вкладку или окно SlovoKrok в окне браузера. Снимок прикрепится автоматически.</small>
        <details><summary>Прикрепить готовый файл</summary><input aria-label="Готовый скриншот" type="file" accept="image/png,image/jpeg,image/webp" multiple disabled={saving || readingFiles} onChange={(event) => { void attach(Array.from(event.target.files ?? [])); event.target.value = ""; }} /></details>
        <small>До 3 изображений по 2 МБ. В архив попадёт всё, что видно на скриншоте.</small>
        <div className="course-report-images">{screenshots.map((image, index) => <figure key={`${index}-${image.name}`}><img src={`data:${image.mime};base64,${image.data}`} alt={image.name} /><figcaption>{image.name}</figcaption><button type="button" disabled={saving || readingFiles} onClick={() => setScreenshots((items) => items.filter((_, position) => position !== index))}>Убрать</button></figure>)}</div>
        <button type="submit" disabled={saving || loading || readingFiles || description.trim().length < 5}>{readingFiles ? "Прикрепляю…" : saving ? "Сохраняю…" : "Сохранить обращение"}</button>
      </form>
      {message && <p role="status">{message}</p>}{error && <p role="alert" className="course-persistence-error">{error}</p>}
      <div className="course-section-heading"><h4>Сохранённые обращения · {reports.length}</h4><div className="course-report-actions"><button type="button" disabled={loading || saving || readingFiles || !reports.length} onClick={() => void download()}>Скачать ZIP</button><button type="button" disabled={loading || saving || readingFiles || !reports.length} onClick={() => void clear()}>Очистить список</button></div></div>
      {loading ? <p>Загружаю обращения…</p> : <div className="course-report-list">{reports.map((item) => <article key={item.id}><strong>{labels[item.section]}</strong><small>{new Date(item.created_at).toLocaleString("ru-RU")}</small><p>{item.description}</p><div className="course-report-images">{item.screenshots?.map((image, index) => <a key={index} href={`data:${image.mime};base64,${image.data}`} download={image.name}><img src={`data:${image.mime};base64,${image.data}`} alt={`Скриншот: ${image.name}`} /></a>)}</div></article>)}</div>}
    </dialog>
  </>;
}
