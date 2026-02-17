/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_UPLOAD_MAX_SIZE_MB: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
