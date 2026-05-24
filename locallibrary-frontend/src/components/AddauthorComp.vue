<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'


const getCookie = (name: string): string | null => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
    return null;
};

interface Autor {
  id: number | string
  first_name: string
  last_name: string
  date_of_birth: string
  date_of_death: string 
}


const emit = defineEmits<{
  (e: 'fechar'): void
  (e: 'salvarAutor'): void
}>()

const form = ref<Autor>({
  id: '',
  first_name: '',
  last_name: '',
  date_of_birth: '',
  date_of_death: '',
})

const adicionarAutor = async () => {
  try {
    const csrfToken = getCookie('csrftoken');
    const dadosLimpos = Object.fromEntries(
      Object.entries(form.value).filter(([_, v]) => v !== '')
    );
    const response = await axios.post('/authors', dadosLimpos, {
      withCredentials: true,
      headers: {
        'X-CSRFToken': csrfToken || ''
      }
    });
    console.log('Autor criado com sucesso:', response.data);
    limparFormulario();
    emit('fechar');
    emit('salvarAutor');
  } catch (error) {
    console.error('Erro ao criar autor:', error);
  }
};

const limparFormulario = () => {
  form.value = {
    id: '',
    first_name: '',
    last_name: '',
    date_of_birth: '',
    date_of_death: '',
  }
}
</script>

<template>
<div class="modal modal-blur fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Adicionar Autor</h5>
          <button type="button" class="btn-close" @click="$emit('fechar')"></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-12 mb-3">
              <label class="form-label">Primeiro Nome</label>
              <input type="text" v-model="form.first_name" class="form-control" placeholder="Digite o primeiro nome do autor">
            </div>
            <div class="col-12 mb-3">
              <label class="form-label">Sobrenome</label>
              <input type="text" v-model="form.last_name" class="form-control" placeholder="Digite o sobrenome do autor">
            </div>
            <div class="col-12 mb-3">
              <label class="form-label">Data de Nascimento</label>
              <input type="date" v-model="form.date_of_birth" class="form-control">
            </div>
            <div class="col-12 mb-3">
              <label class="form-label">Data de Falecimento</label>
              <input type="date" v-model="form.date_of_death" class="form-control">
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-link link-secondary" @click="$emit('fechar')">Cancelar</button>
          <button type="button" class="btn btn-primary" @click="adicionarAutor">Adicionar Autor</button>
        </div>
      </div>
    </div>
  </div>
</template>