<script setup lang="ts">
import SidebarComponent from '../components/SidebarComponent.vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';
interface Author {
  id: number;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  date_of_death: string | null;
}

const authors = ref<Author[]>([]);
const loading = ref(true);
const erro = ref('');
const isAdmin = ref("");
const name = ref("");

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
  }
}

const fetchAuthors = async () => {
  try {
    loading.value = true;
    const response = await axios.get('authors');
    authors.value = response.data;
  } catch (e) {
    erro.value = 'Erro ao carregar a lista de autores.';
    console.error(e);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchAuthors);
</script>

<template>
<SidebarComponent/>
<div class="page">
    <div class="page-wrapper">
        <div class="page-header d-print-none">
            <div class="container-xl">
                <div class="row g-2 align-items-center">
                    <div class="col">
                        <h1>Autores</h1>
                        <h3 class="page-subtitle text-muted">Autores existentes na biblioteca:</h3>
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
                    <th>Nome</th>
                    <th>Status</th>
                    <th>Detalhes</th>
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

                  <!-- Lista de Autores -->
                  <tr v-for="author in authors" :key="author.id">
                    <td>
                      <div class="font-weight-medium">{{ author.first_name }} {{ author.last_name }}</div>
                      <div class="text-muted small">{{ author.date_of_birth }}</div>
                    </td>
                    <td class="text-muted">
                      {{ author.date_of_death ? `Faleceu em ${author.date_of_death}` : 'Ainda vivo' }}
                    </td>
                    <td>
                      <router-link :to="`/authors/${author.id}`" class="btn btn-ghost-primary btn-sm">
                        Ver Detalhes
                      </router-link>
                    </td>
                    <td>
                      <button class="btn btn-primary btn-ghost btn-hover-ghost" v-if="isAdmin">
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
                  <tr v-if="!loading && authors.length === 0">
                    <td colspan="4" class="text-center text-muted py-4">
                      Nenhum autor cadastrado.
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

<style scoped></style>