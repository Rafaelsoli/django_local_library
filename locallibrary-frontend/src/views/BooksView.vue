<script setup lang="ts">
import SidebarComponent from '../components/SidebarComponent.vue';
import AddbookComp from '@/components/AddbookComp.vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';

const mostrarModal = ref(false)
const name = ref("");
const isAdmin = ref("");
const books = ref<Book[]>([]);
const loading = ref(true);
const erro = ref('');
const erroMensagem = ref<string | null>(null)

const getCookie = (name: string): string | null => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
    return null;
};

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

const estaAutenticado = async () => {
  try {
    const response = await axios.get('/me');
    if (response.data.authenticated) {
      name.value = response.data.username;
      isAdmin.value = response.data.is_admin;
    } else {
      name.value = "";
      isAdmin.value = "";
    }
  } catch (error) {
    name.value = "";
    isAdmin.value = "";
    console.error('Usuário não autenticado');
    erroMensagem.value = 'Erro ao verificar autenticação. Por favor, tente novamente.';
  }
}

const fetchBooks = async () => {
  try {
    loading.value = true;
    const response = await axios.get('books');
    books.value = response.data;
  } catch (e) {
    erro.value = 'Erro ao carregar a lista de livros.';
    console.error(e);
    erroMensagem.value = 'Erro ao carregar os livros. Por favor, tente novamente.';
  } finally {
    loading.value = false;
  }
};

const excluirLivros = async (book_id: number) => {
  if (!confirm("Tem certeza que deseja excluir este livro?")) return;
  try {
    const csrfToken = getCookie('csrftoken');
    const resposta = await axios.delete(`books/${book_id}`, {
      withCredentials: true,
      headers: {
        'X-CSRFToken': csrfToken || ''
      }
    });
    console.log("Livro excluído com sucesso:", resposta.data);
    await fetchBooks();
  }catch (e) {
    erroMensagem.value = 'Erro ao excluir o livro. Por favor, tente novamente.';
    console.log("erro em excluir livro");
  }
}
onMounted(fetchBooks);
onMounted(estaAutenticado);
</script>

<template>
  <SidebarComponent />
  <div class="page">
    <div class="page-wrapper">
      <div class="page-header d-print-none">
        <div class="container-xl">
          <div class="row g-2 align-items-center">
            <div class="col">
              <div class="alert alert-danger alert-dismissible" role="alert" v-if="erroMensagem">
                <div class="alert-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                    stroke-linecap="round" stroke-linejoin="round"
                    class="icon alert-icon icon-2">
                    <path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0" />
                    <path d="M12 8v4" />
                    <path d="M12 16h.01" />
                  </svg>
                </div>
                {{erroMensagem}}
                <a class="btn-close" data-bs-dismiss="alert" aria-label="close" @click="erroMensagem = ''"></a>
              </div>
              <h1 class="page-title">Livros</h1>
              <h4 class="page-subtitle text-muted">Livros existentes na biblioteca:</h4>
              <button class="btn btn-primary btn-ghost" @click="mostrarModal = true" v-if="isAdmin">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-square-plus">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                  <path d="M9 12h6" />
                  <path d="M12 9v6" />
                  <path d="M3 5a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-14" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
      <AddbookComp v-if="mostrarModal" 
      @fechar="mostrarModal = false" @salvar="fetchBooks"></AddbookComp>
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
                    <th class="w-1">Infos</th>
                    <th class="w-1" v-if="isAdmin">Excluir</th>
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
                    <td v-if="isAdmin">
                      <button class="btn btn-primary btn-ghost btn-hover-ghost" @click="excluirLivros(book.id)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-trash">
                          <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                          <path d="M4 7l16 0" />
                          <path d="M10 11l0 6" />
                          <path d="M14 11l0 6" />
                          <path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" />
                          <path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" />
                        </svg>
                      </button>
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