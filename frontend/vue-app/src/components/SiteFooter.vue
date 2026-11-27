<template>
  <footer class="site-footer">
    <div class="content-block-vertical">
      <div class="big-header-2" style="color: var(--charcoal)">CleanCar</div>

      <div class="aheader" style="color: var(--charcoal)">Юридический адрес</div>
      <div class="basic" style="color: var(--charcoal)">
        Челябинская обл., г. Челябинск, ул. Лесная, д. 88, офис 2, инд. 454017
      </div>

      <div class="aheader" style="color: var(--charcoal)">Контакты</div>
      <div class="basic" style="color: var(--charcoal)">Телефон горячей линии +7 676 767 67 67</div>
      <div class="basic" style="color: var(--charcoal)">Эл. почта: ooo_cleancar@gmail.com</div>
    </div>

    

      <div class="basic" style="color: var(--charcoal)">© Сеть автомоек «CleanCar» 2026</div>
  </footer>
</template>

<style scoped>
.site-footer {
  display: flex;
  flex-flow: row wrap;
  align-items: flex-start;
  justify-content: space-between;
  width: 100%;
  padding: 32px 80px;
  border-top: 2px solid #000;
  background-color: var(--alice-blue);
}
.site-footer > .content-block-vertical {
  flex: 1 1 240px;
  width: auto;
  min-width: 0;
}

.site-footer > .basic {
  flex: 0 1 auto;
}

@media (max-width: 767px) {
  .site-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
    padding: 16px 24px;
  }

  .site-footer > .content-block-vertical,
  .site-footer > .basic {
    flex: none;
    width: 100%;
  }
}
</style>
