<script setup lang="ts">
import SidebarComponent from '../components/SidebarComponent.vue';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const getCookie = (name: string): string | null => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
    return null;
};

interface Genre {
  name: string;
}

const route = useRoute();
const genres = ref<Genre[]>([]);
const loading = ref(true);
const erroMensagem = ref<string | null>(null);
const acertoMensagem = ref<string | null>(null);


const showModal = ref(false);
const newGenreName = ref('');

const fetchGenres = async () => {
  try {
    loading.value = true;
    const response = await axios.get('genres');
    genres.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar gêneros:", error);
  } finally {
    loading.value = false;
  }
};

const openModal = () => {
  newGenreName.value = ''; 
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const addGenre = async () => {
  if (!newGenreName.value.trim()) return;
  
  const csrfToken = getCookie('csrftoken');
  try {
    await axios.post('genres', { name: newGenreName.value }, {
      withCredentials: true,
      headers: {
        'X-CSRFToken': csrfToken || ''
      }
    });
    acertoMensagem.value = "Gênero adicionado com sucesso!";
    closeModal(); 
    await fetchGenres();
  } catch (error) {
    console.error("Erro ao adicionar gênero:", error);
    erroMensagem.value = "Erro ao adicionar o Gênero";
    closeModal();
  }
};

onMounted(fetchGenres);
</script>

<template>
    <SidebarComponent/>
    <div class="page" v-if="!loading">
        <div class="page-wrapper">
            <div class="page-header d-print-none">
                <div class="container-xl">
                    <div class="row g-2 align-items-center">
                        <div class="col">
                            <h1 class="page-title">Gêneros Literários</h1>
                            
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

                        <div class="col-auto ms-auto d-print-none">
                            <button class="btn btn-primary" @click="openModal">
                              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M12 5v14" /><path d="M5 12h14" /></svg>
                              Adicionar Gênero
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="page-body">     
                <div class="container-xl">
                    <div v-if="genres.length > 0" class="card">
                        <div class="list-group list-group-flush">
                            <div v-for="genre in genres" :key="genre.name" class="list-group-item">
                                {{ genre.name }}
                            </div>
                        </div>
                    </div>
                    <div v-else class="text-muted">
                        Nenhum gênero encontrado na biblioteca.
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="modal modal-blur fade" :class="{ 'show': showModal }" :style="{ display: showModal ? 'block' : 'none' }" tabindex="-1" role="dialog" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Novo Gênero Literário</h5>
            <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
          </div>
          <form @submit.prevent="addGenre">
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Nome do Gênero</label>
                <input type="text" class="form-control" v-model="newGenreName" placeholder="Ex: Ficção Científica, Romance..." autofocus required>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-link link-secondary me-auto" @click="closeModal">Cancelar</button>
              <button type="submit" class="btn btn-primary">Salvar Gênero</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade" :class="{ 'show': showModal }" v-if="showModal"></div>
</template>