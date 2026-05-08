<script setup lang="ts">
import SidebarComponent from '../components/SidebarComponent.vue';
import { ref, onMounted } from 'vue';


</script>

<template>
<SidebarComponent/>
<div class="page">
  <div class="page-wrapper">
    <div class="page-header d-print-none">
      <div class="container-xl">
        <div class="row g-2 align-items-center">
          <div class="col">
            <h1 class="page-title">Home da Biblioteca Local</h1>
            <h4 class="page-subtitle"> Bem vindo à Biblioteca Local! um site desenvolvido com intuíto de estudos em djago. tutorial da Mozilla Developer Network! </h4>
          </div>
        </div>
      </div>
    </div>
    <div class="page-body">
      <div class="container-xl">
        <h2>Conteúdo Dinâmico</h2>
        <h4 class="page-subtitle">Essa biblioteca tem os seguintes contadores:</h4>
        <ul>
          <li>Livros:</li>
          <li>Cópias:</li>
          <li>Cópias disponíveis:</li>
          <li>Autores:</li>
          <li>Visitas:</li>
        </ul>
      </div>
    </div>  
  </div>
</div>
</template>

<style scoped></style>