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
                        <h1 class="page-title">Autores</h1>
                        <div class="text-muted mt-1">Autores existentes na biblioteca</div>
                    </div>
                    <div class="col-auto ms-auto" v-if="isAdmin">
                        <button class="btn btn-primary" @click="mostrarModal = true">
                          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon me-2">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                            <path d="M12 5v14" />
                            <path d="M5 12h14" />
                          </svg>
                          Adicionar Autor
                        </button>
                    </div>
                </div>

                <div class="row mt-3" v-if="erroMensagem || acertoMensagem">
                    <div class="col-12">
                        <div class="alert alert-danger alert-dismissible" role="alert" v-if="erroMensagem">
                          <div class="alert-icon">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon alert-icon">
                              <path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0" />
                              <path d="M12 8v4" />
                              <path d="M12 16h.01" />
                            </svg>
                          </div>
                          {{erroMensagem}}
                          <a class="btn-close" @click="erroMensagem = null"></a>
                        </div>

                        <div class="alert alert-success alert-dismissible" role="alert" v-if="acertoMensagem">
                          <div class="d-flex">
                            <div class="alert-icon">
                              <svg xmlns="http://www.w3.org/2000/svg" class="icon alert-icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                <path d="M5 12l5 5l10 -10" />
                              </svg>
                            </div>
                            <div>{{ acertoMensagem }}</div>
                            <a class="btn-close" @click="acertoMensagem = null"></a>
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
                  <table class="table table-vcenter card-table table-striped">
                    <thead>
                      <tr>
                        <th>Nome / Nascimento</th>
                        <th>Status</th>
                        <th>Ações</th>
                        <th class="w-1" v-if="isAdmin"></th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-if="loading">
                        <td :colspan="isAdmin ? 4 : 3" class="text-center py-4">
                          <div class="spinner-border spinner-border-sm text-secondary me-2"></div>
                          Carregando acervo...
                        </td>
                      </tr>

                      <tr v-else v-for="author in authors" :key="author.id">
                        <td>
                          <div class="font-weight-medium text-heading">{{ author.first_name }} {{ author.last_name }}</div>
                          <div class="text-muted small mt-1">
                            <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-inline me-1" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M4 5m0 2a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2z" /><path d="M16 3l0 4" /><path d="M8 3l0 4" /><path d="M4 11l16 0" /><path d="M8 15h2v2h-2z" /></svg>
                            {{ author.date_of_birth }}
                          </div>
                        </td>
                        <td>
                          <span v-if="!author.date_of_death" class="badge bg-success-lt">Ainda Vivo</span>
                          <span v-else class="badge bg-secondary-lt">Faleceu em {{ author.date_of_death }}</span>
                        </td>
                        <td>
                          <router-link :to="`/authors/${author.id}`" class="btn btn-outline-primary btn-sm">
                            Ver Detalhes
                          </router-link>
                        </td>
                        <td v-if="isAdmin" class="text-end">
                          <button class="btn btn-icon btn-ghost-danger btn-sm" @click="prepararExclusaoAutor(author.id)" title="Excluir Autor">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon">
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

                      <tr v-if="!loading && authors.length === 0">
                        <td :colspan="isAdmin ? 4 : 3" class="text-center text-muted py-5">
                          <div class="text-muted mb-2">Nenhum autor cadastrado.</div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
        </div>
    </div>

    <div class="modal modal-blur fade show d-block" tabindex="-1" role="dialog" v-if="mostrarConfirmacao" style="background: rgba(0,0,0,0.4); z-index: 1050;">
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

<style scoped>
.table-responsive {
  overflow-x: auto;
}
</style>