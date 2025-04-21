import { ref, onMounted, onUnmounted } from 'vue';

export function useScreenSize() {
  const width = ref(window.innerWidth);
  const height = ref(window.innerHeight);

  const isMobile = ref(width.value < 768);
  const isTablet = ref(width.value >= 768 && width.value < 1024);
  const isDesktop = ref(width.value >= 1024);

  function onResize() {
    width.value = window.innerWidth;
    height.value = window.innerHeight;

    isMobile.value = width.value < 768;
    isTablet.value = width.value >= 768 && width.value < 1024;
    isDesktop.value = width.value >= 1024;
  }

  onMounted(() => {
    window.addEventListener('resize', onResize);
  });

  onUnmounted(() => {
    window.removeEventListener('resize', onResize);
  });

  return {
    width,
    height,
    isMobile,
    isTablet,
    isDesktop
  };
}
