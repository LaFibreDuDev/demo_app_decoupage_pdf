<template>
  <div class="w-full max-w-2xl">
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-sm font-medium text-gray-700">
        Sélectionnez les pages à extraire
        <span class="text-gray-400 font-normal">({{ selectedPages.length }} sélectionnée(s))</span>
      </h2>
      <button
        v-if="selectedPages.length > 0"
        @click="clearSelection"
        class="text-xs text-gray-400 hover:text-gray-600 underline"
      >
        Tout désélectionner
      </button>
    </div>

    <div class="flex flex-wrap gap-3">
      <PageCard
        v-for="n in pageCount"
        :key="n"
        :page="n"
        :selected="selectedPages.includes(n)"
        :thumb-url="thumbUrls[n - 1]"
        @toggle="togglePage(n)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import PageCard from './PageCard.vue'

const props = defineProps<{
  pageCount: number
  sessionId: string
}>()

const emit = defineEmits<{
  'update:selected-pages': [pages: number[]]
}>()

const selectedPages = ref<number[]>([])
const thumbUrls = ref<string[]>([])

function togglePage(page: number): void {
  const idx = selectedPages.value.indexOf(page)
  if (idx === -1) {
    selectedPages.value = [...selectedPages.value, page].sort((a, b) => a - b)
  } else {
    selectedPages.value = selectedPages.value.filter((p) => p !== page)
  }
}

function clearSelection(): void {
  selectedPages.value = []
}

watch(selectedPages, (val) => {
  emit('update:selected-pages', val)
})

watch(() => props.sessionId, async (sessionId) => {
  thumbUrls.value = []
  if (!sessionId) return
  try {
    const response = await fetch(`/thumbs/${sessionId}`)
    if (response.ok) {
      const data = await response.json()
      thumbUrls.value = data.urls
    }
  } catch {
    // Miniatures indisponibles — dégradation gracieuse vers affichage numérique
  }
}, { immediate: true })

defineExpose({ clearSelection })
</script>
