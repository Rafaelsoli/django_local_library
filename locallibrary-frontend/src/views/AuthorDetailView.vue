<script setup lang="ts">
import SidebarComponent from '../components/SidebarComponent.vue';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

interface Book {
  id: number;
  title: string;
  summary: string;
}

interface Author {
  id: number;
  first_name: string;
  last_name: string;
  date_of_birth: string | null;
  date_of_death: string | null;
  books: Book[];
}

const route = useRoute();
const author = ref<Author | null>(null);
const loading = ref(true);

const fetchAuthorDetails = async () => {
  try {
    loading.value = true;
    const authorId = route.params.id;
    const response = await axios.get(`authors/${authorId}`);
    author.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar detalhes do autor:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchAuthorDetails);
</script>

<template>
  <SidebarComponent />
  <div class="page" v-if="!loading && author">
    <div class="page-wrapper">
      <div class="page-header d-print-none">
        <div class="container-xl">
          <div class="row g-2 align-items-center">
            <div class="col">
              <h1 class="page-title">Nome: {{ author.first_name }} {{ author.last_name }}</h1>
              <h4 class="page-subtitle">
                Data de nascimento: {{ author.date_of_birth || 'Não informada' }}
              </h4>
              <h4 class="page-subtitle">
                Data de falecimento: {{ author.date_of_death || 'Vivo ou não informada' }}
              </h4>
            </div>
          </div>
        </div>
      </div>
      <div class="page-body">
        <div class="container-xl">
          <div class="card">
            <div class="card-body">
              <h2 class="mb-3">Livros</h2>
              
              <div v-if="author.books && author.books.length > 0">
                <div v-for="book in author.books" :key="book.id" class="card mb-2">
                    <div class="card-body">
                        <h3 class="card-title">{{ book.title }}</h3>
                        <p class="text-muted">{{ book.summary }}</p>
                    </div>
                </div>
              </div>
              
              <div v-else class="text-muted">
                Este autor ainda não possui livros cadastrados.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="loading" class="page-center text-center py-5">
    <div class="spinner-border text-primary"></div>
    <p class="mt-2">Carregando detalhes do autor...</p>
  </div>
</template>

<style scoped>
.page-subtitle {
  margin-top: 0.5rem;
  color: #666;
}
</style>