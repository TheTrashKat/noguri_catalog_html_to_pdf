window.addEventListener("load", () => {
fetch('data.json')
  .then(response => response.json())
  .then(data => {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');
    const categoria = data.paginas[id];
    const preciosContainer = document.getElementById('precios');
    const header = document.querySelector('.header');
    const description = document.querySelector('.sub');
    const title = document.querySelector('.tag');
    const numero_pagina = document.querySelector('.number-paginator');

    // Actualizar cabecera y descripción
    header.style.backgroundImage = `url('${categoria.url_img_header}')`;
    description.textContent = categoria.description_categoria;
    title.textContent = categoria.nombre_categoria;
    numero_pagina.textContent = categoria.numero_pagina;

    // Crear artículos dinámicos
    categoria.elementos.forEach(item => {
      const article = document.createElement('article');
      article.classList.add('price-row');

      article.innerHTML = `
        <div class="imgbox"  fetchpriority="high" loading="eager" style="background-image: url('${item.url_img_categoria}');"></div>
        <div class="card">
          <div class="card-internal">
            <h3>${item.titulo_categoria}</h3>
            <ul class="prices">
              ${item.lista_precios
                .map(
                  (p, i) => `
                <li><span><span class="bullet"></span>${p.descripción}</span><strong>${p.precio}</strong></li>
                ${i < item.lista_precios.length - 1 ? '<div class="dash" aria-hidden="true"></div>' : ''}
              `
                )
                .join('')}
            </ul>
            <div class="note">${item.nota_extra}</div>
          </div>
        </div>
      `;

      preciosContainer.appendChild(article);
    });
  })
  .catch(err => console.error('Error cargando data.json:', err));

// Nuevo Agregado
let data = [];
let paginaActual = 0;

async function cargarJSON() {
  const response = await fetch("data.json");
  data = await response.json();
  renderPagina(0); // Carga la primera al inicio
}

function renderPagina(index) {
  const pagina = data[index];
  if (!pagina) return;

  // ejemplo de cómo reemplazar el contenido dinámicamente
  const header = document.querySelector(".header");
  header.style.backgroundImage = `url(${pagina.url_img_header})`;

  document.querySelector(".tag").textContent = pagina.nombre_categoria;
  document.querySelector(".sub").textContent = pagina.description_categoria;

  const contenedor = document.getElementById("precios");
  contenedor.innerHTML = ""; // Limpia antes de dibujar

  // Recorremos los elementos de la categoría
  Object.keys(pagina)
    .filter(k => k.startsWith("elementos_categoria"))
    .forEach(key => {
      const el = pagina[key];
      const fila = document.createElement("article");
      fila.classList.add("price-row");
      fila.innerHTML = `
        <div class="imgbox"  fetchpriority="high" loading="eager" style="background-image:url('${el.url_img_categoria}')"></div>
        <div class="card">
          <h3>${el.titulo_categoria}</h3>
          <ul class="prices">
            ${el.lista_precios.map(p => `
              <li><span><span class="bullet"></span>${p.descripcion}:</span><strong>${p.precio}</strong></li>
              <div class="dash"></div>
            `).join('')}
          </ul>
          <div class="note">${el.nota_extra}</div>
        </div>
      `;
      contenedor.appendChild(fila);
    });
}

window.addEventListener("DOMContentLoaded", cargarJSON);
});