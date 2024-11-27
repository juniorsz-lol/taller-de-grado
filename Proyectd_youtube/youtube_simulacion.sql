-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 20-11-2024 a las 19:16:16
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `spotify_simulacion`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bibliotecas`
--

CREATE TABLE `bibliotecas` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `cancion_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `canciones`
--

CREATE TABLE `canciones` (
  `id` int(11) NOT NULL,
  `titulo` varchar(100) NOT NULL,
  `duracion` time NOT NULL,
  `artista` varchar(100) NOT NULL,
  `album` varchar(100) DEFAULT NULL,
  `URL` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `canciones`
--

INSERT INTO `canciones` (`id`, `titulo`, `duracion`, `artista`, `album`, `URL`) VALUES
(2, 'somewhere only we know', '00:03:00', 'keane', NULL, 'https://www.youtube.com/watch?v=Oextk-If8HQ&list=RDOextk-If8HQ&start_radio=1&rv=Oextk-If8HQ');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `listas_reproducciones`
--

CREATE TABLE `listas_reproducciones` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `listas_reproducciones`
--

INSERT INTO `listas_reproducciones` (`id`, `nombre`, `usuario_id`, `fecha_creacion`) VALUES
(1, 'milistabuena', 1, '2024-11-20 13:12:51');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lista_canciones`
--

CREATE TABLE `lista_canciones` (
  `id` int(11) NOT NULL,
  `lista_id` int(11) NOT NULL,
  `cancion_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Apellido` varchar(50) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Contraseña` varchar(255) NOT NULL,
  `es_admin` tinyint(1) NOT NULL DEFAULT 0,
  `Fecha_Creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `Nombre`, `Apellido`, `Email`, `Contraseña`, `es_admin`, `Fecha_Creacion`) VALUES
(1, 'jhurguen', 'ergueta', 'jhurguen@gmail.com', '$2b$12$fa74nklUIpVYzPAtxVVbZehCaNGlJdDMLAI/oQcTLRz4WTCgvvYaO', 0, '2024-11-20 13:07:28'),
(2, 'Admin', 'User', 'admin@example.com', '$2b$12$h4/gyp20aGTAQLJXnb0pS.lsBdGNye5UDXFxyTQ5HRvmvoyOMN8Xi', 1, '2024-11-20 13:22:06');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `bibliotecas`
--
ALTER TABLE `bibliotecas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `cancion_id` (`cancion_id`);

--
-- Indices de la tabla `canciones`
--
ALTER TABLE `canciones`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `listas_reproducciones`
--
ALTER TABLE `listas_reproducciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `lista_canciones`
--
ALTER TABLE `lista_canciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `lista_id` (`lista_id`),
  ADD KEY `cancion_id` (`cancion_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `bibliotecas`
--
ALTER TABLE `bibliotecas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `canciones`
--
ALTER TABLE `canciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `listas_reproducciones`
--
ALTER TABLE `listas_reproducciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `lista_canciones`
--
ALTER TABLE `lista_canciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `bibliotecas`
--
ALTER TABLE `bibliotecas`
  ADD CONSTRAINT `bibliotecas_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `bibliotecas_ibfk_2` FOREIGN KEY (`cancion_id`) REFERENCES `canciones` (`id`);

--
-- Filtros para la tabla `listas_reproducciones`
--
ALTER TABLE `listas_reproducciones`
  ADD CONSTRAINT `listas_reproducciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `lista_canciones`
--
ALTER TABLE `lista_canciones`
  ADD CONSTRAINT `lista_canciones_ibfk_1` FOREIGN KEY (`lista_id`) REFERENCES `listas_reproducciones` (`id`),
  ADD CONSTRAINT `lista_canciones_ibfk_2` FOREIGN KEY (`cancion_id`) REFERENCES `canciones` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
