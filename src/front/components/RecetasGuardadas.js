// RecetasGuardadas.js
import React from 'react';

const RecetasGuardadas = ({ recetas }) => {
  return (
    <div className="mt-4">
      <h3>Recetas Guardadas</h3>
      <ul className="list-group">
        {recetas?.map((receta, index) => (
          <li key={index} className="list-group-item">
            <h5>{receta.nombreMascota}</h5>
            <p><strong>Edad:</strong> {receta.edad} años</p>
            <p><strong>Peso:</strong> {receta.peso} kg</p>
            <p><strong>Raza:</strong> {receta.raza}</p>
            <p><strong>Sexo:</strong> {receta.sexo}</p>
            <p><strong>Propietario:</strong> {receta.propietario}</p>
            <p><strong>Fecha:</strong> {receta.fecha}</p>
            <p><strong>Diagnóstico:</strong> {receta.diagnostico}</p>
            <p><strong>Tratamiento:</strong> {receta.tratamiento}</p>
            <p><strong>Veterinario:</strong> {receta.veterinario}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RecetasGuardadas;
