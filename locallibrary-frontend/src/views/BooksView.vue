<script setup lang="ts">
import SidebarComponent from '../components/SidebarComponent.vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';

interface Author {
  id: number;
  first_name: string;
  last_name: string;
}

interface Book {
  id: number;
  title: string;
  summary: string;
  isbn: string;
  author: Author; 
}

const books = ref<Book[]>([]);
const loading = ref(true);
const erro = ref('');

const fetchBooks = async () => {
  try {
    loading.value = true;
    const response = await axios.get('books');
    books.value = response.data;
  } catch (e) {
    erro.value = 'Erro ao carregar a lista de livros.';
    console.error(e);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchBooks);
</script>

<template>
  <SidebarComponent />
  <div class="page">
    <div class="page-wrapper">
      <div class="page-header d-print-none">
        <div class="container-xl">
          <div class="row g-2 align-items-center">
            <div class="col">
              <h1 class="page-title">Livros</h1>
              <h4 class="page-subtitle text-muted">Livros existentes na biblioteca:</h4>
            </div>
          </div>
        </div>
      </div>

      <div class="page-body">
        <div class="container-xl">
          <!-- Alerta de Erro -->
          <div v-if="erro" class="alert alert-danger">{{ erro }}</div>

          <div class="card">
            <div class="table-responsive">
              <table class="table table-vcenter card-table">
                <thead>
                  <tr>
                    <th>Título</th>
                    <th>Autor</th>
                    <th>ISBN</th>
                    <th class="w-1"></th>
                  </tr>
                </thead>
                <tbody>
                  <!-- Loader -->
                  <tr v-if="loading">
                    <td colspan="4" class="text-center py-4">
                      <div class="spinner-border spinner-border-sm text-secondary"></div>
                      Carregando acervo...
                    </td>
                  </tr>

                  <!-- Lista de Livros -->
                  <tr v-for="book in books" :key="book.id">
                    <td>
                      <div class="font-weight-medium">{{ book.title }}</div>
                      <div class="text-muted small">{{ book.summary.substring(0, 60) }}...</div>
                    </td>
                    <td class="text-muted">
                      {{ book.author.first_name }} {{ book.author.last_name }}
                    </td>
                    <td class="text-muted">
                      {{ book.isbn }}
                    </td>
                    <td>
                      <router-link :to="`/books/${book.id}`" class="btn btn-ghost-primary btn-sm">
                        Ver Detalhes
                      </router-link>
                    </td>
                  </tr>

                  <!-- Caso não existam livros -->
                  <tr v-if="!loading && books.length === 0">
                    <td colspan="4" class="text-center text-muted py-4">
                      Nenhum livro cadastrado.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.font-weight-medium {
  font-weight: 500;
}
</style>