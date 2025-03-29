import React from 'react'
import useGlobalReducer from '../hooks/useGlobalReducer'
import axios from "axios";
import { useState } from "react";
import RecetasGuardadas from './RecetasGuardadas';

const RecetarioPage = () => {
  const { store, dispatch } = useGlobalReducer();
  const [formData, setFormData] = useState({
        nombreMascota: "",
        edad: "",
        peso: "",
        raza: "",
        sexo: "",
        propietario: "",
        fecha: "",
        diagnostico: "",
        tratamiento: "",
        veterinario: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
      e.preventDefault();
      try {
        const response = await axios.post("https://literate-umbrella-rqpvjwqg6q9c57g5-3001.app.github.dev/recetario_page", formData);
        dispatch({ type: "add_receta", payload: response.data }); // Agregar receta al contexto
        setFormData({ 
            nombreMascota: "", edad: "", peso: "", raza: "", sexo: "", 
            propietario: "", fecha: "", diagnostico: "", tratamiento: "", veterinario: "" 
        }); // Limpiar el formulario
    } catch (error) {
        console.error("Error al guardar la receta", error);
    }
  }

  const toggleRecetasVisibility = () => {
    setShowRecetas(!setShowRecetas);
  }

  return (
    <div className="container mt-4">
      <h2 className="text-center">Recetario de Mascotas</h2>
      
      {/* Formulario */}
      <form onSubmit={handleSubmit} className="card p-3">
          <div className="row">
              <div className="col-md-6">
                  <label>Nombre de la Mascota</label>
                  <input type="text" className="form-control" name="nombreMascota" value={formData.nombreMascota} onChange={handleChange} required />
              </div>
              <div className="col-md-3">
                  <label>Edad</label>
                  <input type="number" className="form-control" name="edad" value={formData.edad} onChange={handleChange} required />
              </div>
              <div className="col-md-3">
                  <label>Peso (kg)</label>
                  <input type="number" className="form-control" name="peso" value={formData.peso} onChange={handleChange} required />
              </div>
          </div>

          <div className="row mt-2">
              <div className="col-md-4">
                  <label>Raza</label>
                  <input type="text" className="form-control" name="raza" value={formData.raza} onChange={handleChange} />
              </div>
              <div className="col-md-4">
                  <label>Sexo</label>
                  <select className="form-control" name="sexo" value={formData.sexo} onChange={handleChange} required>
                      <option value="">Seleccionar</option>
                      <option value="Macho">Macho</option>
                      <option value="Hembra">Hembra</option>
                  </select>
              </div>
              <div className="col-md-4">
                  <label>Propietario</label>
                  <input type="text" className="form-control" name="propietario" value={formData.propietario} onChange={handleChange} required />
              </div>
          </div>

          <div className="row mt-2">
              <div className="col-md-6">
                  <label>Fecha</label>
                  <input type="date" className="form-control" name="fecha" value={formData.fecha} onChange={handleChange} required />
              </div>
              <div className="col-md-6">
                  <label>Nombre del Veterinario</label>
                  <input type="text" className="form-control" name="veterinario" value={formData.veterinario} onChange={handleChange} required />
              </div>
          </div>

          <div className="row mt-2">
              <div className="col-md-6">
                  <label>Diagnóstico</label>
                  <textarea className="form-control" name="diagnostico" value={formData.diagnostico} onChange={handleChange} required></textarea>
              </div>
              <div className="col-md-6">
                  <label>Tratamiento</label>
                  <textarea className="form-control" name="tratamiento" value={formData.tratamiento} onChange={handleChange} required></textarea>
              </div>
          </div>

          <button type="submit" className="btn btn-primary mt-3">Guardar Receta</button>
      </form>

      {/* Lista de Recetas */}
      {/*<h3 className="mt-4">Recetas Guardadas</h3>
      <ul className="list-group">
          {store.recetas?.map((receta, index) => (
              <li key={index} className="list-group-item">
                  <strong>{receta.nombreMascota}</strong> - {receta.fecha}
                  <p><strong>Diagnóstico:</strong> {receta.diagnostico}</p>
                  <p><strong>Tratamiento:</strong> {receta.tratamiento}</p>
                  <p><strong>Veterinario:</strong> {receta.veterinario}</p>
              </li>
          ))}
      </ul>*/}

        {/* Botón para mostrar/ocultar recetas */}
        <button onClick={toggleRecetasVisibility} className="btn btn-info mt-4">
            {showRecetas ? 'Ocultar Recetas Guardadas' : 'Ver Recetas Guardadas'}
        </button>

        {/* Mostrar las recetas si showRecetas es true */}
        {showRecetas && <RecetasGuardadas recetas={store.recetas} />}
    </div>
  )
}

export default RecetarioPage
