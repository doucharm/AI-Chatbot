export default function ResourceUsage() {
  if (!props || Object.keys(props).length === 0) {
    return (
      <div className="text-[10px] text-muted-foreground opacity-60 animate-pulse">
        Finalizing usage…
      </div>
    );
  }
  const {
    model = "unknown",
    "prompt-token": promptTokens = 0,
    completion_token: completionTokens = 0
  } = props;
  const total = promptTokens + completionTokens;
  return (
    <div className="text-[10px] text-muted-foreground opacity-70 mt-1">
      {model} · in {promptTokens} · out {completionTokens} · total {total}
    </div>
  );
}