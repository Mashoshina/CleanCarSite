<template>
  <section class="site-cover">
    <span class="big-header-2" style="color: var(--alice-blue)">
      Сеть автомоек CleanCar
    </span>

    <ul class="aheader" style="color: var(--alice-blue)">
      <div class="cover-block-horizontal"><li>На рынке 20 лет</li>
      <li>20 точек в Челябинске</li>
      <li>10 точек в области</li>
      <li>Демократичные цены</li>
      <li>Онлайн очередь</li></div>
      
    </ul>
  </section>
</template>

<style scoped>
.site-cover {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;
  width: 100%;
  padding: 64px 80px;
  overflow: hidden;
  background-image: url('/items/desk-cover.png');
  background-position: left center;
  background-size: auto 100%;
}

.cover-block-horizontal {
    display: flex;
    flex-flow: row wrap;
    align-items: stretch;
    justify-content: flex-start;
    gap: 48px;
    width: 100%;
    padding: 8px 0;
}

@media (max-width: 1100px) {
  .site-cover {
    gap: 8px;
    padding: 16px;
    background-image: url('/items/mobile-cover.png');
  }

  .cover-block-horizontal {
    gap: 24px;
  }
}
</style>