<script setup lang="ts">
import SidebarComponent from '../components/SidebarComponent.vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';


interface Stats {
  books: number;
  copies: number;
  copies_available: number;
  authors: number;
}


const stats = ref<Stats | null>(null);
const loading = ref(true);
const erro = ref(false);


const fetchStats = async () => {
  try {
    loading.value = true;
    const response = await axios.get('stats');
    stats.value = response.data;
  } catch (error) {
    console.error("Erro ao carregar stats:", error);
    erro.value = true;
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchStats();
});
</script>

<template>
  <SidebarComponent />
  <div class="page">
    <div class="page-wrapper">
      <div class="page-header d-print-none">
        <div class="container-xl">
          <div class="row g-2 align-items-center">
            <div class="col">
              <h1 class="page-title">Home da Biblioteca Local</h1>
              <h4 class="page-subtitle text-muted">
                Bem vindo à Biblioteca Local! Um site desenvolvido com intuito de estudos em Django (Tutorial MDN).
              </h4>
            </div>
          </div>
        </div>
      </div>

      <div class="page-body">
        <div class="container-xl">
          <div class="card">
            <div class="card-body">
              <h2 class="card-title">Conteúdo Dinâmico</h2>
              <p class="text-muted">Essa biblioteca tem os seguintes contadores:</p>

              <div v-if="loading" class="progress progress-sm">
                <div class="progress-bar progress-bar-indeterminated"></div>
              </div>

              <div v-else-if="erro" class="alert alert-danger">
                Não foi possível carregar os dados da API. Verifique se o Django está rodando.
              </div>

              <ul v-else class="list-unstyled space-y-1">
                <li>
                  <strong>Livros:</strong> 
                  <span class="badge bg-blue-lt">{{ stats?.books }}</span>
                </li>
                <li>
                  <strong>Cópias no acervo:</strong> 
                  <span class="badge bg-blue-lt">{{ stats?.copies }}</span>
                </li>
                <li>
                  <strong>Cópias disponíveis:</strong> 
                  <span class="badge bg-green-lt">{{ stats?.copies_available }}</span>
                </li>
                <li>
                  <strong>Autores cadastrados:</strong> 
                  <span class="badge bg-blue-lt">{{ stats?.authors }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>  
    </div>
  </div>
</template>

<style scoped>
.space-y-1 li {
  margin-bottom: 0.5rem;
}
</style>