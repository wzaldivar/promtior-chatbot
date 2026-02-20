interface Env {
  readonly VITE_API_HOST: string;
}

interface ImportMeta {
  readonly env: Env;
}
