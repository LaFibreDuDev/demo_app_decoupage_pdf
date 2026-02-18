<template>
  <header class="h-16 border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md flex items-center justify-between px-4 md:px-6 sticky top-0 z-50">
    <div class="flex items-center gap-3">
      <!-- Hamburger (mobile only) -->
      <button
        class="md:hidden p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        @click="$emit('toggle-sidebar')"
        title="Ouvrir le menu"
      >
        <span class="material-symbols-outlined">menu</span>
      </button>
      <div class="w-10 h-10 bg-primary rounded-xl flex items-center justify-center text-white shrink-0">
        <span class="material-symbols-outlined">content_cut</span>
      </div>
      <h1 class="text-lg md:text-xl font-bold tracking-tight font-display whitespace-nowrap">
        Découpeur <span class="text-primary">PDF</span>
      </h1>
    </div>
    <div class="flex items-center gap-2 md:gap-4">
      <button
        class="p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        @click="$emit('toggle-dark-mode')"
        :title="isDark ? 'Passer en mode clair' : 'Passer en mode sombre'"
      >
        <span class="material-symbols-outlined dark:hidden">dark_mode</span>
        <span class="material-symbols-outlined hidden dark:block">light_mode</span>
      </button>
      <div class="h-8 w-px bg-slate-200 dark:bg-slate-800"></div>
      <button
        class="flex items-center gap-2 px-2 md:px-4 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors"
        @click="$emit('open-help')"
        title="Aide"
      >
        <span class="material-symbols-outlined text-[20px]">help</span>
        <span class="hidden md:inline">Aide</span>
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
defineProps<{
  isDark: boolean
}>()

defineEmits<{
  'toggle-dark-mode': []
  'toggle-sidebar': []
  'open-help': []
}>()
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
</style>
