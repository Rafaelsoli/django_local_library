<script setup lang="ts">
import SidebarComponent from '../components/SidebarComponent.vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';
import AddauthorComp from '@/components/AddauthorComp.vue';

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
  date_of_birth: string;
  date_of_death: string | null;
}

const authors = ref<Author[]>([]);
const loading = ref(true);
const erro = ref('');
const isAdmin = ref("");
const name = ref("");
const autordesejado = ref<number | null>(null);
const mostrarConfirmacao = ref(false);
const erroMensagem = ref<string | null>(null)
const acertoMensagem = ref<string | null>(null)
const mostrarModal = ref(false);

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

const prepararExclusaoAutor = (author_id: number) => {
  autordesejado.value = author_id;
  mostrarConfirmacao.value = true;
};

const excluirAutor = async () => {
  if (!autordesejado) return;
  try {
    const csrfToken = getCookie('csrftoken');
    await axios.delete(`authors/${autordesejado.value}`, {
      withCredentials: true,
      headers: {
        'X-CSRFToken': csrfToken
      }
    });
    mostrarConfirmacao.value = false; 
    acertoMensagem.value = 'Autor excluído com sucesso!';
    fetchAuthors(); 
  } catch (e) {
    erro.value = 'Erro ao excluir o autor.';
    erroMensagem.value = 'Erro ao excluir o autor, ainda existem livros associados.';
    mostrarConfirmacao.value = false; 
    console.error(e);
  }
};
onMounted(estaAutenticado);
onMounted( fetchAuthors);
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
                        <button class="btn btn-primary btn-ghost" @click="mostrarModal = true" v-if="isAdmin">
                          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-square-plus">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                            <path d="M9 12h6" />
                            <path d="M12 9v6" />
                            <path d="M3 5a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-14" />
                          </svg>
                        </button>
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
                        <div class="alert alert-success alert-dismissible" role="alert" v-if="acertoMensagem">
                        <div class="d-flex">
                          <div>
                            <svg xmlns="http://www.w3.org/2000/svg" class="icon alert-icon" width="24"
                              height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"
                              fill="none" stroke-linecap="round" stroke-linejoin="round">
                              <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                              <path d="M5 12l5 5l10 -10" />
                            </svg>
                          </div>
                          {{ acertoMensagem }}
                          <a class="btn-close" data-bs-dismiss="alert" aria-label="close" @click="acertoMensagem = ''"></a>
                        </div>
                      </div>
                    </div>
                </div>
            </div>
        </div>

        <AddauthorComp v-if="mostrarModal" @fechar="mostrarModal = false" @salvarAutor="fetchAuthors" />

        <div class="page-body">
        <div class="container-xl">
          
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
                      <button class="btn btn-primary btn-ghost btn-hover-ghost" v-if="isAdmin" @click="prepararExclusaoAutor(author.id)">
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
<div 
    class="modal modal-blur fade show d-block" 
    tabindex="-1" 
    role="dialog" 
    v-if="mostrarConfirmacao"
    style="background: rgba(0,0,0,0.4);"
  >
    <div class="modal-dialog modal-sm modal-dialog-centered" role="document">
      <div class="modal-content">
        <button type="button" class="btn-close" @click="mostrarConfirmacao = false"></button>
        <div class="modal-status bg-danger"></div>
        <div class="modal-body text-center py-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon mb-2 text-danger icon-lg" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
            <path d="M12 9v2m0 4v.01" />
            <path d="M5 19h14a2 2 0 0 0 1.84 -2.75l-7.1 -12.25a2 2 0 0 0 -3.5 0l-7.1 12.25a2 2 0 0 0 1.75 2.75" />
          </svg>
          <h3>Tem Certeza?</h3>
          <div class="text-secondary">
            Realmente deseja excluir este autor? Essa ação não pode ser desfeita.
          </div>
        </div>
        <div class="modal-footer">
          <div class="w-100">
            <div class="row">
              <div class="col">
                <button type="button" class="btn w-100" @click="mostrarConfirmacao = false"> Cancelar </button>
              </div>
              <div class="col">
                <button type="button" class="btn btn-danger w-100" @click="excluirAutor"> Excluir </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<style scoped></style>