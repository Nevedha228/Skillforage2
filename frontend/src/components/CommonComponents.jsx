export function PageHeader({ title, subtitle, action, breadcrumbs }) {
  return (
    <div className="page-header" style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "16px" }}>
      <div>
        {breadcrumbs && (
          <div style={{ fontSize: "12px", color: "var(--neutral-500)", marginBottom: "4px" }}>
            {breadcrumbs}
          </div>
        )}
        <h1 className="page-header-title">{title}</h1>
        {subtitle && <p className="page-header-subtitle">{subtitle}</p>}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}

export function StatCard({ title, value, subtext, icon, trend }) {
  return (
    <div className="card" style={{ padding: "20px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "8px" }}>
        <span style={{ fontSize: "13px", fontWeight: "600", color: "var(--neutral-500)", textTransform: "uppercase", letterSpacing: "0.5px" }}>
          {title}
        </span>
        {icon && <span style={{ fontSize: "20px" }}>{icon}</span>}
      </div>
      <div style={{ fontSize: "28px", fontWeight: "700", color: "var(--neutral-900)", marginBottom: "4px" }}>
        {value}
      </div>
      {(subtext || trend) && (
        <div style={{ fontSize: "12px", color: "var(--neutral-500)", display: "flex", alignItems: "center", gap: "6px" }}>
          {trend && <span style={{ fontWeight: "600", color: "var(--primary-600)" }}>{trend}</span>}
          <span>{subtext}</span>
        </div>
      )}
    </div>
  );
}

export function ProgressBar({ percentage = 0, color = "var(--primary-600)", height = 8 }) {
  const clamped = Math.max(0, Math.min(100, percentage));
  return (
    <div className="progress-bar-container" style={{ height: `${height}px` }}>
      <div
        className="progress-bar-fill"
        style={{ width: `${clamped}%`, backgroundColor: color }}
      />
    </div>
  );
}

export function SkillBadge({ name, status = "Not assessed" }) {
  let badgeClass = "badge-neutral";
  if (status === "Strong evidence") badgeClass = "badge-success";
  else if (status === "Demonstrated") badgeClass = "badge-primary";
  else if (status === "In progress") badgeClass = "badge-warning";
  else if (status === "Self-reported") badgeClass = "badge-neutral";

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "6px",
        background: "var(--neutral-100)",
        padding: "4px 10px",
        borderRadius: "var(--radius-sm)",
        fontSize: "13px",
        margin: "3px"
      }}
    >
      <span style={{ fontWeight: "500" }}>{name}</span>
      <span className={`badge ${badgeClass}`} style={{ fontSize: "10px", padding: "1px 6px" }}>
        {status}
      </span>
    </span>
  );
}

export function EmptyState({ title, description, icon = "📂", actionText, onAction }) {
  return (
    <div className="card" style={{ padding: "48px 24px", textAlign: "center", maxWidth: "600px", margin: "32px auto" }}>
      <div style={{ fontSize: "48px", marginBottom: "16px" }}>{icon}</div>
      <h3 style={{ fontSize: "18px", fontWeight: "600", color: "var(--neutral-900)", marginBottom: "8px" }}>
        {title}
      </h3>
      <p style={{ fontSize: "14px", color: "var(--neutral-500)", maxWidth: "420px", margin: "0 auto 24px" }}>
        {description}
      </p>
      {actionText && onAction && (
        <button onClick={onAction} className="btn btn-primary">
          {actionText}
        </button>
      )}
    </div>
  );
}

export function LoadingState({ message = "Loading..." }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "64px 16px" }}>
      <div
        style={{
          width: "36px",
          height: "36px",
          border: "3px solid var(--neutral-200)",
          borderTopColor: "var(--primary-600)",
          borderRadius: "50%",
          animation: "spin 0.8s linear infinite",
          marginBottom: "16px"
        }}
      />
      <p style={{ color: "var(--neutral-500)", fontSize: "14px" }}>{message}</p>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}

export function ErrorMessage({ message, onRetry }) {
  return (
    <div className="alert alert-danger" style={{ margin: "24px 0" }}>
      <div>⚠️</div>
      <div style={{ flex: 1 }}>
        <p style={{ fontWeight: "500" }}>{message || "An unexpected error occurred."}</p>
        {onRetry && (
          <button onClick={onRetry} className="btn btn-secondary btn-sm" style={{ marginTop: "8px" }}>
            Try Again
          </button>
        )}
      </div>
    </div>
  );
}

export function ConfirmationModal({ isOpen, title, message, confirmText = "Confirm", cancelText = "Cancel", onConfirm, onCancel, isDanger = false }) {
  if (!isOpen) return null;
  return (
    <div className="modal-backdrop">
      <div className="modal-dialog">
        <div className="card-header">
          <h3 className="card-title">{title}</h3>
        </div>
        <div className="card-body">
          <p style={{ fontSize: "14px", color: "var(--neutral-600)" }}>{message}</p>
        </div>
        <div className="card-footer" style={{ display: "flex", justifyContent: "flex-end", gap: "10px" }}>
          <button onClick={onCancel} className="btn btn-secondary">
            {cancelText}
          </button>
          <button onClick={onConfirm} className={`btn ${isDanger ? "btn-danger" : "btn-primary"}`}>
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}
