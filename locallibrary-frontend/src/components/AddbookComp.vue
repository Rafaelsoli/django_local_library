<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const getCookie = (name: string): string | null => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
    return null;
};

interface LivroForm {
  title: string
  author_id: string | number
  isbn: string
  summary: string
  genre_ids: string[]
}

interface Autor {
  id: number | string
  first_name: string
  last_name: string
}

interface Genre {
  name: string
}
const emit = defineEmits<{
  (e: 'fechar'): void
}>()

const form = ref<LivroForm>({
  title: '',
  author_id: '',
  isbn: '',
  summary: '',
  genre_ids: [],
})

const autores = ref<Autor[]>([])
const genres = ref<Genre[]>([])

const buscarAutores = async () => {
  try {
    const response = await axios.get('/authors')
    console.log('Autores buscados com sucesso:', response.data)
    autores.value = response.data
  } catch (error) {
    console.error('Erro ao buscar autores:', error)
  }
}

const buscarGeneros = async () => {
  try {
    const response = await axios.get('/genres')
    console.log('Gêneros buscados com sucesso:', response.data)
    genres.value = response.data
  } catch (error) {
    console.error('Erro ao buscar gêneros:', error)
  }
}

onMounted(() => {
  buscarAutores()
  buscarGeneros()
})

const salvar = async () => {
  try {
    const csrfToken = getCookie('csrftoken');
    console.log('Enviando dados do formulário:', form.value)
    const response = await axios.post('/books', form.value, {
      withCredentials: true,
      headers: {
        'X-CSRFToken': csrfToken || ''
      }
    }); 
    console.log('Livro criado com sucesso:', response.data)
    
    limparFormulario()
    emit('fechar')
  } catch (error) {
    console.error('agora deu o caraio', error)
  }
}

const limparFormulario = () => {
  form.value = {
    title: '',
    summary: '',
    isbn: '',
    author_id: '',
    genre_ids: [],
  }
}
</script>

<template>
<div class="modal modal-blur fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Adicionar Livro</h5>
          <button type="button" class="btn-close" @click="$emit('fechar')"></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-12 mb-3">
              <label class="form-label">Título</label>
              <input type="text" v-model="form.title" class="form-control" placeholder="Digite o título do livro">
            </div>
            <div class="col-12 mb-3">
              <label class="form-label">Autor</label>
              <select v-model="form.author_id" class="form-select">
                <option value="" disabled selected>Selecione um autor...</option>
                <option v-for="autor in autores" :key="autor.id" :value="autor.id">
                  {{ autor.first_name }} {{ autor.last_name }}
                </option>
              </select>
            </div>

            <div class="col-12 mb-3">
              <label class="form-label">ISBN</label>
              <input type="text" v-model="form.isbn" class="form-control" placeholder="Digite o ISBN">
            </div>

            <div class="col-12 mb-3">
              <label class="form-label">Gênero</label>
              <select v-model="form.genre_ids" class="form-select" multiple>
                <option value="" disabled selected>Selecione um gênero...</option>
                <option v-for="gen in genres" :key="gen.name" :value="gen.name">
                  {{ gen.name }}
                </option>
              </select>
            </div>

            <div class="col-12 mb-3">
              <label class="form-label">Descrição</label>
              <textarea v-model="form.summary" class="form-control" rows="3" placeholder="Digite uma descrição do livro"></textarea>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-link link-secondary" @click="$emit('fechar')">Cancelar</button>
          <button type="button" class="btn btn-primary" @click="salvar">Adicionar Livro</button>
        </div>
      </div>
    </div>
  </div>
</template>