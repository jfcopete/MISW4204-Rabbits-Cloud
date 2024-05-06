delete from public.piloto;
delete from public.tarea;
DROP TYPE ESTADO_VIDEO;

CREATE TABLE piloto (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    pais VARCHAR NULL,
    contrasena VARCHAR NOT NULL
);

CREATE TYPE ESTADO_VIDEO AS ENUM ('PROCESSED', 'UPLOADED', 'DELETED');

CREATE TABLE tarea (
    id SERIAL PRIMARY KEY,
    nombre_archivo VARCHAR NOT NULL,
    url VARCHAR NOT NULL,
    estado ESTADO_VIDEO NOT NULL DEFAULT 'UPLOADED',
    numero_votos INT NOT NULL DEFAULT 0,
    marca_de_carga DATE NOT NULL DEFAULT CURRENT_DATE,
    piloto_id INT NOT NULL,
    FOREIGN KEY (piloto_id) REFERENCES piloto(id) ON DELETE SET NULL
);