<template>
  <div class="fixed bottom-8 left-1/2 -translate-x-1/2 flex items-center gap-4 bg-white dark:bg-slate-800 px-6 py-3 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-700 z-50">
    <div class="w-8 h-8 rounded-full bg-green-500/10 flex items-center justify-center text-green-600">
      <span class="material-symbols-outlined text-[20px]">check_circle</span>
    </div>
    <p class="text-sm font-medium text-slate-700 dark:text-slate-200">
      Document chargé avec succès ({{ fileSizeMo }} Mo)
    </p>
    <button
      @click="$emit('close')"
      class="p-1 hover:bg-slate-100 dark:hover:bg-slate-700 rounded text-slate-400 transition-colors"
    >
      <span class="material-symbols-outlined text-[18px]">close</span>
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  filename: string
  fileSizeMo: string
}>()

defineEmits<{
  close: []
}>()
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
</style>
