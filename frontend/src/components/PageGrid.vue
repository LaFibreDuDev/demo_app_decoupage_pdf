<template>
  <div class="flex-1 overflow-y-auto p-8 custom-scrollbar">
    <div :class="gridClass">
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
import { ref, computed, watch } from 'vue'
import PageCard from './PageCard.vue'

const props = defineProps<{
  pageCount: number
  sessionId: string
  zoomLevel?: number
}>()

const emit = defineEmits<{
  'update:selected-pages': [pages: number[]]
}>()

const selectedPages = ref<number[]>([])
const thumbUrls = ref<string[]>([])

const ZOOM_COLS: Record<number, string> = {
  1: 'grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-8',
  2: 'grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-8',
  3: 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8',
  4: 'grid grid-cols-2 gap-8',
  5: 'grid grid-cols-1 gap-8',
}

const gridClass = computed(() => ZOOM_COLS[props.zoomLevel ?? 3] ?? ZOOM_COLS[3])

function togglePage(page: number): void {
  const idx = selectedPages.value.indexOf(page)
  if (idx === -1) {
    selectedPages.value = [...selectedPages.value, page].sort((a, b) => a - b)
  } else {
    selectedPages.value = selectedPages.value.filter((p) => p !== page)
  }
}

function selectAll(): void {
  selectedPages.value = Array.from({ length: props.pageCount }, (_, i) => i + 1)
}

function clearSelection(): void {
  selectedPages.value = []
}

function selectEven(): void {
  selectedPages.value = Array.from({ length: props.pageCount }, (_, i) => i + 1).filter((p) => p % 2 === 0)
}

function selectOdd(): void {
  selectedPages.value = Array.from({ length: props.pageCount }, (_, i) => i + 1).filter((p) => p % 2 !== 0)
}

watch(selectedPages, (val) => {
  emit('update:selected-pages', val)
})

watch(() => props.sessionId, async (sessionId) => {
  selectedPages.value = []
  thumbUrls.value = []
  if (!sessionId) return
  try {
    const response = await fetch(`/thumbs/${sessionId}`)
    if (response.ok) {
      const data = await response.json()
      thumbUrls.value = data.urls
    }
  } catch {
    // Miniatures indisponibles — dégradation gracieuse
  }
}, { immediate: true })

defineExpose({ selectAll, clearSelection, selectEven, selectOdd })
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #334155;
}
</style>
